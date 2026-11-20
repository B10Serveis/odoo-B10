from datetime import datetime, timedelta
from unittest.mock import patch

import pytz
from lxml import html

from odoo import Command, fields
from odoo.addons.point_of_sale.tests.common import TestPoSCommon
from odoo.exceptions import AccessError
from odoo.tests import new_test_user, tagged
from odoo.tools.convert import convert_file
from odoo.tools.misc import format_date


@tagged("post_install", "-at_install")
class TestPosClosingReport(TestPoSCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.create_product("Closing report product", cls.categ_basic, 10)
        cls.pos_user = new_test_user(
            cls.env,
            login="b10_closing_pos_user",
            groups="base.group_user,point_of_sale.group_pos_user",
            company_id=cls.company.id,
            company_ids=[Command.set(cls.company.ids)],
            tz="UTC",
        )
        cls.bank_pm1.journal_id.write({
            "profit_account_id": cls.company_data["default_account_revenue"].id,
            "loss_account_id": cls.company_data["default_account_expense"].id,
        })

    def setUp(self):
        super().setUp()
        self.config = self.basic_config
        self.report = self.env["report.b10_pos.report_pos_closing_report"].with_context(
            tz="UTC", lang="en_US"
        )

    def _order(self, quantity, payments):
        data = self.create_ui_order_data(
            [(self.product, quantity)], customer=self.customer, payments=payments
        )
        self.env["pos.order"].sync_from_ui([data])

    def _close(self, session, counted_cash=0, differences=None):
        session.post_closing_cash_details(counted_cash)
        result = session.close_session_from_ui(differences)
        self.assertTrue(result["successful"], result)
        self.assertEqual(session.state, "closed")

    def _values(self, session, report=None):
        date = fields.Date.to_string(session.stop_at.date())
        return (report if report is not None else self.report).get_session(
            date, date, session.config_id.id
        )

    def _payments(self, session, report=None):
        values = self._values(session, report=report)
        self.assertEqual([row["session"].id for row in values["sessions"]], session.ids)
        return {row["name"]: row for row in values["sessions"][0]["payments"]}

    def test_closing_date_totals_and_rendering(self):
        session = self.open_new_session(opening_cash=20)
        self._order(1.5, [(self.cash_pm1, 10), (self.pay_later_pm, 5)])
        session.try_cash_in_out("in", 3, "Cash added", {"translatedType": "Cash in"})
        self._close(session, counted_cash=33)
        session.write({
            "start_at": datetime(2026, 11, 19, 23),
            "stop_at": datetime(2026, 11, 20, 1),
        })
        payments = self._payments(session)
        self.assertEqual(payments[self.cash_pm1.name]["sold"], 10)
        self.assertEqual(payments[self.cash_pm1.name]["declared"], 33)
        self.assertEqual(payments[self.pay_later_pm.name]["sold"], 5)
        self.assertIsNone(payments[self.pay_later_pm.name]["declared"])
        self.assertFalse(
            self.report.get_session("2026-11-19", "2026-11-19", self.config.id)["sessions"]
        )

        wizard = self.env["pos.closing.wizard"].create({
            "start_date": "2026-11-20", "end_date": "2026-11-20",
            "pos_session_id": self.config.id,
        })
        action = wizard.with_context(discard_logo_check=True).generate_report()
        self.assertEqual(action["context"]["active_ids"], self.config.ids)
        self.assertEqual(action["data"]["config_id"], self.config.id)
        report_action = self.env["ir.actions.report"].with_user(self.pos_user)
        rendered, _ = report_action._render_qweb_html(
            "b10_pos.report_pos_closing_report", self.config.ids, data=action["data"]
        )
        self.assertIn(session.name.encode(), rendered)
        self.assertIn(self.cash_pm1.name.encode(), rendered)
        self.assertIn(self.pay_later_pm.name.encode(), rendered)
        self.assertIn("—".encode(), rendered)
        # TransactionCase does not serve HTTP assets to wkhtmltopdf. Keep the
        # real PDF conversion while avoiding requests to a running Odoo server.
        with patch.object(type(self.env["ir.qweb"]), "_get_asset_nodes", return_value=[]):
            pdf, _ = report_action.with_context(force_report_rendering=True)._render_qweb_pdf(
                "b10_pos.report_pos_closing_report", self.config.ids, data=action["data"]
            )
        self.assertTrue(pdf.startswith(b"%PDF"))

    def test_timezone_boundaries_and_daylight_saving(self):
        report = self.report.with_context(tz="Europe/Madrid")
        timezone = pytz.timezone("Europe/Madrid")
        for date, hours in (("2026-03-29", 23), ("2026-10-25", 25)):
            with self.subTest(date=date):
                start = report._date_to_utc(date, timezone)
                stop = report._date_to_utc(date, timezone, end=True)
                self.assertEqual(stop - start, timedelta(hours=hours))

        session = self.open_new_session()
        self._order(1, [(self.cash_pm1, 10)])
        self._close(session, counted_cash=10)
        start = datetime(2026, 11, 19, 23)  # Midnight in Madrid.
        session.write({"start_at": start - timedelta(days=1), "stop_at": start})
        self.assertTrue(report.get_session("2026-11-20", "2026-11-20", self.config.id)["sessions"])
        session.stop_at = start - timedelta(seconds=1)
        self.assertFalse(report.get_session("2026-11-20", "2026-11-20", self.config.id)["sessions"])
        session.stop_at = start + timedelta(days=1)
        self.assertFalse(report.get_session("2026-11-20", "2026-11-20", self.config.id)["sessions"])
        session.stop_at = start
        rendered, _ = self.env["ir.actions.report"].with_context(tz="Europe/Madrid")._render_qweb_html(
            "b10_pos.report_pos_closing_report", self.config.ids,
            data={"config_id": self.config.id, "date_start": "2026-11-20", "date_stop": "2026-11-20"},
        )
        cells = html.fromstring(rendered).xpath("//table[1]/tbody/tr/td")
        self.assertEqual(cells[2].text_content().strip(), format_date(self.env, "2026-11-20"))

    def test_bank_refunds_keep_their_sign(self):
        session = self.open_new_session()
        self._order(-1, [(self.bank_pm1, -10)])
        self._close(session)
        payment = session.bank_payment_ids
        for state in ("draft", "canceled"):
            payment.copy({"amount": 999, "state": state, "pos_session_id": session.id})
        payments = self._payments(session)
        self.assertEqual(payments[self.bank_pm1.name]["sold"], -10)
        self.assertEqual(payments[self.bank_pm1.name]["declared"], -10)

    def test_split_bank_difference_and_refunds(self):
        for difference in (2, -2):
            with self.subTest(difference=difference):
                session = self.open_new_session()
                self._order(2, [(self.bank_split_pm1, 20)])
                self._order(-0.5, [(self.bank_split_pm1, -5)])
                self._close(session, differences=[(self.bank_split_pm1.id, difference)])
                payments = self._payments(session)
                self.assertEqual(payments[self.bank_split_pm1.name]["sold"], 15)
                self.assertEqual(payments[self.bank_split_pm1.name]["declared"], 15 + difference)
                # Keep subsequent iterations on separate closing days.
                session.stop_at -= timedelta(days=1)

    def test_counting_difference_in_another_language(self):
        self.env["res.lang"]._activate_lang("es_ES")
        self.env["ir.module.module"]._load_module_terms(["point_of_sale"], ["es_ES"])
        session = self.open_new_session()
        self._order(1, [(self.bank_split_pm1, 10)])
        spanish_session = session.with_context(lang="es_ES")
        self._close(spanish_session, differences=[(self.bank_split_pm1.id, -2)])
        self.assertNotEqual(
            spanish_session._get_diff_account_move_ref(self.bank_split_pm1),
            session.with_context(lang="en_US")._get_diff_account_move_ref(self.bank_split_pm1),
        )
        self.assertEqual(self._payments(session)[self.bank_split_pm1.name]["declared"], 8)

    def test_pos_user_and_company_access(self):
        session = self.open_new_session()
        self._order(1, [(self.bank_pm1, 10)])
        self._close(session)
        self.assertFalse(
            self.env["account.payment"].with_user(self.pos_user).has_access("read")
        )
        report = self.report.with_user(self.pos_user)
        self.assertEqual(self._payments(session, report)[self.bank_pm1.name]["declared"], 10)
        user = new_test_user(self.env, login="b10_no_pos", groups="base.group_user")
        with self.assertRaises(AccessError):
            self._values(session, self.report.with_user(user))
        other_company = self.env["res.company"].create({"name": "Other POS company"})
        other_config = self.env["pos.config"].with_company(other_company).create(
            {"name": "Other company POS", "company_id": other_company.id,
             "payment_method_ids": [Command.clear()]}
        )
        with self.assertRaises(AccessError):
            report.get_session("2026-11-20", "2026-11-20", other_config.id)

    def test_empty_and_open_sessions(self):
        session = self.open_new_session()
        today = fields.Date.to_string(fields.Date.today())
        self.assertFalse(self.report.get_session(today, today, self.config.id)["sessions"])
        self._close(session)
        values = self._values(session)
        self.assertFalse(values["sessions"][0]["payments"])
        rendered, _ = self.env["ir.actions.report"]._render_qweb_html(
            "b10_pos.report_pos_closing_report", self.config.ids,
            data={"config_id": self.config.id, "date_start": today, "date_stop": today},
        )
        self.assertIn(b"No payments recorded for this session.", rendered)

    def test_report_translations(self):
        session = self.open_new_session()
        self._close(session)
        date = fields.Date.to_string(session.stop_at.date())
        for language, period, closing, empty in (
            ("ca_ES", "Període:", "Data de tancament", "No hi ha pagaments registrats"),
            ("es_ES", "Periodo:", "Fecha de cierre", "No hay pagos registrados"),
        ):
            with self.subTest(language=language):
                self.env["res.lang"]._activate_lang(language)
                self.env["ir.module.module"]._load_module_terms(["b10_pos"], [language])
                rendered, _ = self.env["ir.actions.report"].with_context(lang=language)._render_qweb_html(
                    "b10_pos.report_pos_closing_report", self.config.ids,
                    data={"config_id": self.config.id, "date_start": date, "date_stop": date},
                )
                for text in (period, closing, empty):
                    self.assertIn(text.encode(), rendered)

    def test_action_update_clears_old_binding(self):
        action = self.env.ref("b10_pos.action_pos_closing_report")
        action.write({
            "model": "report.b10_pos.pos_closing_report",
            "binding_model_id": self.env.ref("point_of_sale.model_pos_config").id,
        })
        convert_file(self.env, "b10_pos", "views/pos_closing.xml", {}, mode="update")
        self.assertEqual(action.model, "pos.config")
        self.assertFalse(action.binding_model_id)

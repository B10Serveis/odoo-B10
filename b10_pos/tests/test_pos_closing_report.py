from datetime import datetime, time, timedelta

import odoo
from odoo import fields
from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPosClosingReport(TestPoSCommon):
    def test_closing_date_payment_totals_and_rendering(self):
        self.config = self.basic_config
        product = self.create_product("Report test product", self.categ_basic, 15.0)
        session = self.open_new_session()
        order_data = self.create_ui_order_data(
            [(product, 1)],
            customer=self.customer,
            payments=[(self.cash_pm1, 10.0), (self.pay_later_pm, 5.0)],
            uid=self.create_random_uid(),
        )
        self.env["pos.order"].create_from_ui([order_data])
        session.post_closing_cash_details(10.0)
        session.close_session_from_ui()

        closing_date = fields.Datetime.to_datetime(session.stop_at).date()
        opening_at = datetime.combine(closing_date - timedelta(days=1), time(23, 0))
        closing_at = datetime.combine(closing_date, time(1, 0))
        session.write(
            {
                "start_at": fields.Datetime.to_string(opening_at),
                "stop_at": fields.Datetime.to_string(closing_at),
            }
        )

        report = self.env["report.b10_pos.report_pos_closing_report"].with_context(
            tz="UTC"
        )
        selected_date = fields.Date.to_string(closing_date)
        report_values = report.get_session(selected_date, selected_date, self.config.id)

        self.assertEqual([session], [row["session"] for row in report_values["sessions"]])
        payment_rows = {
            payment["name"]: payment
            for payment in report_values["sessions"][0]["payments"]
        }
        self.assertAlmostEqual(10.0, payment_rows[self.cash_pm1.name]["sold"])
        self.assertAlmostEqual(10.0, payment_rows[self.cash_pm1.name]["declared"])
        self.assertAlmostEqual(5.0, payment_rows[self.pay_later_pm.name]["sold"])
        self.assertIsNone(payment_rows[self.pay_later_pm.name]["declared"])

        opening_date = fields.Date.to_string(closing_date - timedelta(days=1))
        opening_date_values = report.get_session(
            opening_date, opening_date, self.config.id
        )
        self.assertFalse(opening_date_values["sessions"])

        report_data = {
            "date_start": selected_date,
            "date_stop": selected_date,
            "config_id": self.config.id,
        }
        rendered, _ = self.env["ir.actions.report"]._render_qweb_html(
            "b10_pos.report_pos_closing_report",
            self.config.ids,
            data=report_data,
        )
        self.assertIn(session.name.encode(), rendered)
        self.assertIn(self.cash_pm1.name.encode(), rendered)
        self.assertIn(self.pay_later_pm.name.encode(), rendered)
        self.assertIn("—".encode(), rendered)

        pdf, _ = self.env["ir.actions.report"].with_context(
            force_report_rendering=True
        )._render_qweb_pdf(
            "b10_pos.report_pos_closing_report", self.config.ids, data=report_data
        )
        self.assertTrue(pdf.startswith(b"%PDF"))

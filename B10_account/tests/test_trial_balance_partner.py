import io
import zipfile

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestTrialBalancePartner(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report = cls.env["report.b10_account.trial_balance_partner"]
        cls.income = cls.company_data["default_account_revenue"]
        cls.receivable = cls.company_data["default_account_receivable"]
        cls.wizard = cls.env["b10.trial.balance.partner.wizard"].create(
            {"date_from": "2024-02-01", "date_to": "2024-02-29"}
        )
        for date, partner, amount in [
            ("2023-12-01", cls.partner_a, 30),
            ("2024-01-01", cls.partner_a, 40),
            ("2024-02-01", cls.partner_a, 100),
            ("2024-02-02", cls.partner_b, 60),
            ("2024-02-03", cls.env["res.partner"], 20),
        ]:
            cls.env["account.move"].create(
                {
                    "date": date,
                    "journal_id": cls.company_data["default_journal_misc"].id,
                    "line_ids": [
                        (0, 0, {
                            "account_id": cls.receivable.id,
                            "partner_id": partner.id,
                            "debit": amount,
                            "date_maturity": date,
                        }),
                        (0, 0, {
                            "account_id": cls.income.id,
                            "partner_id": partner.id,
                            "credit": amount,
                        }),
                    ],
                }
            ).action_post()

    def test_partner_rows_and_fiscal_balances(self):
        values = self.report._get_report_values([], self.wizard._prepare_report_data())
        rows = {(row["id"], row["partner_id"]): row for row in values["partner_rows"]}
        income_a = rows[self.income.id, self.partner_a.id]
        self.assertEqual(income_a["initial_balance"], -40)
        self.assertEqual(income_a["credit"], 100)
        self.assertEqual(income_a["ending_balance"], -140)
        self.assertEqual(rows[self.income.id, 0]["credit"], 20)
        self.assertEqual(rows[self.income.id, self.partner_b.id]["credit"], 60)
        earnings = self.wizard.unaffected_earnings_account
        self.assertEqual(rows[earnings.id, self.partner_a.id]["initial_balance"], -30)
        self.assertAlmostEqual(values["partner_totals"]["ending_balance"], 0)

    def test_account_filter_and_hidden_options(self):
        self.wizard.write({
            "account_ids": [(6, 0, self.income.ids)],
            "partner_ids": [(6, 0, self.partner_a.ids)],
            "show_partner_details": True,
            "hide_account_at_end_0": True,
        })
        data = self.wizard._prepare_report_data()
        self.assertFalse(data["hide_account_at_end_0"])
        values = self.report._get_report_values([], data)
        self.assertEqual(len(values["partner_rows"]), 3)
        self.assertEqual({row["id"] for row in values["partner_rows"]}, {self.income.id})

    def test_html_and_xlsx(self):
        data = self.wizard._prepare_report_data()
        action = self.env.ref("B10_account.action_trial_balance_partner_html")
        html, _ = action._render_qweb_html(action.report_name, self.wizard.ids, data=data)
        self.assertIn(self.partner_a.name.encode(), html)
        for foreign_currency in (False, True):
            self.wizard.foreign_currency = foreign_currency
            data = self.wizard._prepare_report_data()
            xlsx_action = self.env.ref("B10_account.action_trial_balance_partner_xlsx")
            content, _ = xlsx_action._render_xlsx(
                xlsx_action.report_name, self.wizard.ids, data
            )
            with zipfile.ZipFile(io.BytesIO(content)) as archive:
                sheet = archive.read("xl/worksheets/sheet1.xml")
                self.assertIn(b"autoFilter", sheet)
                self.assertIn(self.partner_a.name.encode(), sheet)

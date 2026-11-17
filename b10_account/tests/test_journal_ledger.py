from io import BytesIO
from zipfile import ZipFile

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestJournalLedger(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({'name': 'Partner balance test'})
        cls.env = cls.env(context=dict(cls.env.context, allowed_company_ids=cls.company.ids))
        cls.partner_a, cls.partner_b = cls.env['res.partner'].create([
            {'name': 'Partner A'}, {'name': 'Partner B'},
        ])
        cls.accounts = cls.env['account.account'].create([
            {'name': name, 'code': code, 'account_type': kind,
             'company_ids': [Command.set(cls.company.ids)]}
            for name, code, kind in [
                ('Assets', '210000', 'asset_fixed'),
                ('Amortisation', '281000', 'asset_fixed'),
                ('Expense', '680000', 'expense'),
                ('Retained earnings', '120000', 'equity_unaffected'),
                ('Unused', '220000', 'asset_fixed'),
            ]
        ])
        cls.asset, cls.amortisation, cls.expense, cls.earnings, cls.unused = cls.accounts
        cls.journal = cls.env['account.journal'].create({
            'name': 'Partner test', 'code': 'PTST', 'type': 'general',
            'company_id': cls.company.id,
        })
        cls._move('2025-12-15', cls.asset, cls.expense, 30, cls.partner_a)
        cls._move('2026-01-15', cls.asset, cls.amortisation, 100, cls.partner_a)
        cls._move('2026-02-15', cls.asset, cls.amortisation, 200, cls.partner_b)
        cls._move('2026-02-16', cls.asset, cls.amortisation, 50)
        # Opposing partners must remain visible even when their account nets to zero.
        cls._move('2026-02-17', cls.unused, cls.unused, 25,
                  cls.partner_a, cls.partner_b)

    @classmethod
    def _move(cls, date, debit, credit, amount, partner=False, credit_partner=None):
        cls.env['account.move'].create({
            'company_id': cls.company.id, 'journal_id': cls.journal.id, 'date': date,
            'line_ids': [Command.create({
                'name': 'Test', 'account_id': account.id,
                'partner_id': selected.id if selected else False,
                'debit': dr, 'credit': cr,
            }) for account, selected, dr, cr in [
                (debit, partner, amount, 0),
                (credit, partner if credit_partner is None else credit_partner, 0, amount),
            ]],
        }).action_post()


    def _wizard(self, **values):
        return self.env["journal.ledger.report.wizard"].create({
            "company_id": self.company.id, "year": 2026, **values,
        })

    def _lines(self, wizard):
        return self.env["report.b10_account.journal_ledger"]._get_book_lines(
            wizard, wizard._prepare_b10_journal_ledger_data()
        )[1]

    def test_opening_and_sequence(self):
        lines = self._lines(self._wizard())
        opening = {line["account_code"]: line for line in lines
                   if line["sequence"] == "1"}
        self.assertEqual(opening[self.asset.code]["debit"], 30)
        self.assertEqual(opening["129"]["credit"], 30)
        self.assertNotIn(self.expense.code, opening)
        self.assertEqual([line["sequence"] for line in lines
                          if line["sequence"] != "1"],
                         [str(i) for i in range(2, 7) for _ in range(2)])
        self.assertAlmostEqual(sum(line["debit"] - line["credit"]
                                   for line in lines), 0)

    def test_result_account_and_archived_journal(self):
        self.env["account.account"].create({
            "name": "Result", "code": "129000", "account_type": "equity",
            "company_ids": [Command.set(self.company.ids)],
        })
        self.journal.active = False
        wizard = self._wizard()
        self.assertIn(self.journal.id,
                      wizard._prepare_b10_journal_ledger_data()["journal_ids"])
        opening = [line for line in self._lines(wizard)
                   if line["sequence"] == "1"]
        self.assertIn("129000", [line["account_code"] for line in opening])
        self.assertNotIn("129", [line["account_code"] for line in opening])

    def test_html_pdf_action_and_xlsx(self):
        wizard = self._wizard(with_account_name=True)
        data = wizard._prepare_b10_journal_ledger_data()
        action = self.env.ref("b10_account.action_b10_journal_ledger_html")
        html, _ = action._render_qweb_html(action.report_name, wizard.ids, data=data)
        self.assertIn(b"210000", html)
        self.assertIn(b"Partner A", html)
        self.assertEqual(wizard.action_export_b10_journal_ledger_pdf()["report_type"],
                         "qweb-pdf")
        action = self.env.ref("b10_account.action_b10_journal_ledger_xlsx")
        content, _ = action._render_xlsx(action.report_name, wizard.ids, data=data)
        with ZipFile(BytesIO(content)) as archive:
            self.assertIn("xl/worksheets/sheet1.xml", archive.namelist())

    def test_draft_and_other_year_excluded(self):
        self.env["account.move"].create({
            "company_id": self.company.id, "journal_id": self.journal.id,
            "date": "2026-03-01",
            "line_ids": [Command.create({
                "name": "Draft", "account_id": account.id,
                "debit": debit, "credit": credit,
            }) for account, debit, credit in [
                (self.asset, 999, 0), (self.amortisation, 0, 999),
            ]],
        })
        self._move("2027-01-01", self.asset, self.amortisation, 888)
        lines = self._lines(self._wizard())
        self.assertFalse(any(line["debit"] in (888, 999) for line in lines))

    def test_year_validation(self):
        for year in (0, 10000):
            with self.assertRaises(ValidationError):
                self._wizard(year=year)

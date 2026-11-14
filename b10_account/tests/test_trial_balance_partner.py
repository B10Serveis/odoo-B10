from collections import defaultdict
from io import BytesIO
from zipfile import ZipFile

from odoo import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestTrialBalancePartner(TransactionCase):
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
        return self.env['b10.trial.balance.partner.wizard'].create(dict({
            'company_id': self.company.id, 'date_from': '2026-02-01',
            'date_to': '2026-02-28', 'target_move': 'posted',
        }, **values))

    def _values(self, wizard):
        return self.env['report.b10_account.trial_balance_partner']._get_report_values(
            wizard.ids, wizard._prepare_report_data()
        )

    def test_all_accounts_partners_and_initial_balances(self):
        values = self._values(self._wizard())
        rows = {(r['id'], r['partner_id']): r for r in values['partner_rows']}
        self.assertEqual(rows[self.asset.id, self.partner_a.id]['initial_balance'], 130)
        self.assertEqual(rows[self.asset.id, self.partner_b.id]['debit'], 200)
        self.assertEqual(rows[self.asset.id, 0]['debit'], 50)
        self.assertEqual(rows[self.amortisation.id, self.partner_b.id]['credit'], 200)
        self.assertIn((self.unused.id, self.partner_a.id), rows)
        self.assertIn((self.unused.id, self.partner_b.id), rows)
        fields = ('initial_balance', 'debit', 'credit', 'balance', 'ending_balance')
        totals = defaultdict(lambda: defaultdict(float))
        for row in rows.values():
            for field in fields:
                totals[row['id']][field] += row[field]
        for account_id, original in values['total_amount'].items():
            for field in fields:
                self.assertAlmostEqual(totals[account_id][field], original[field], places=2)

    def test_partner_filter_is_ignored(self):
        wizard = self._wizard(partner_ids=[Command.set(self.partner_a.ids)])
        self.assertEqual(wizard._prepare_report_data()['partner_ids'], [])
        self.assertTrue(any(row['partner_id'] == self.partner_b.id
                            for row in self._values(wizard)['partner_rows']))

    def test_html_and_xlsx(self):
        wizard = self._wizard()
        data = wizard._prepare_report_data()
        action = self.env.ref('b10_account.action_trial_balance_partner_html')
        html, _ = action._render_qweb_html(action.report_name, wizard.ids, data=data)
        self.assertIn(b'Partner A', html)
        self.assertIn(b'Partner B', html)
        action = self.env.ref('b10_account.action_trial_balance_partner_xlsx')
        content, _ = action._render_xlsx(action.report_name, wizard.ids, data=data)
        with ZipFile(BytesIO(content)) as archive:
            self.assertIn('xl/worksheets/sheet1.xml', archive.namelist())

    def test_account_filter_and_foreign_currency_export(self):
        wizard = self._wizard(account_ids=[Command.set(self.asset.ids)],
                              foreign_currency=True)
        values = self._values(wizard)
        self.assertEqual({row['id'] for row in values['partner_rows']}, {self.asset.id})
        action = self.env.ref('b10_account.action_trial_balance_partner_xlsx')
        content, _ = action._render_xlsx(action.report_name, wizard.ids,
                                         data=wizard._prepare_report_data())
        self.assertTrue(content.startswith(b'PK'))

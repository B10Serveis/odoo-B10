from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _fill_bank_cash_dashboard_data(self, dashboard_data):
        super()._fill_bank_cash_dashboard_data(dashboard_data)

        journals = self.filtered(lambda journal: journal.type in ("bank", "cash"))
        accounts = journals.mapped("default_account_id")
        balances = {}
        if accounts:
            grouped_balances = self.env["account.move.line"]._read_group(
                domain=[
                    ("account_id", "in", accounts.ids),
                    ("company_id", "in", journals.company_id.ids),
                    ("parent_state", "=", "posted"),
                    ("date", "<=", fields.Date.context_today(self)),
                ],
                groupby=["account_id", "company_id"],
                aggregates=["balance:sum"],
            )
            balances = {
                (account.id, company.id): balance
                for account, company, balance in grouped_balances
            }

        for journal in journals:
            account = journal.default_account_id
            dashboard_data[journal.id]["has_ledger_account"] = bool(account)
            if account:
                amount = balances.get((account.id, journal.company_id.id), 0.0)
                dashboard_data[journal.id]["ledger_balance"] = (
                    journal.company_id.currency_id.format(amount)
                )

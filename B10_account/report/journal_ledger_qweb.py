from odoo import models


class B10JournalLedgerQWeb(models.AbstractModel):
    _name = "report.b10_account.journal_ledger_qweb"
    _description = "Mercantile Registry General Ledger Report"

    def _get_report_values(self, docids, data=None):
        wizard = self.env[data["wizard_name"]].browse(data["wizard_id"])
        _, lines = self.env[
            "report.b10_account.journal_ledger"
        ]._get_book_lines(wizard, data)
        return {
            "doc_ids": docids,
            "doc_model": wizard._name,
            "docs": wizard,
            "company": wizard.company_id,
            "company_currency": wizard.company_id.currency_id,
            "year": wizard.year,
            "lines": lines,
            "with_account_name": wizard.with_account_name,
        }

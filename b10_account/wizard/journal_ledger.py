from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class JournalLedgerReportWizard(models.TransientModel):
    _inherit = "journal.ledger.report.wizard"

    year = fields.Integer(
        string="Fiscal year",
        required=True,
        default=lambda self: fields.Date.context_today(self).year,
    )

    @api.constrains("year")
    def _check_year_b10(self):
        for wizard in self:
            if not 1 <= wizard.year <= 9999:
                raise ValidationError(_("Please enter a valid year."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            year = vals.get("year", fields.Date.context_today(self).year)
            if not 1 <= year <= 9999:
                raise ValidationError(_("Please enter a valid year."))
            vals.setdefault("year", year)
            vals.setdefault("date_from", date(year, 1, 1))
            vals.setdefault("date_to", date(year, 12, 31))
        return super().create(vals_list)

    @api.onchange("year")
    def _onchange_year_b10(self):
        for wizard in self:
            if 1 <= wizard.year <= 9999:
                wizard.date_from = date(wizard.year, 1, 1)
                wizard.date_to = date(wizard.year, 12, 31)

    def _prepare_b10_journal_ledger_data(self):
        self.ensure_one()
        data = super()._prepare_report_data()
        journals = self.env["account.journal"].with_context(active_test=False).search(
            [("company_id", "=", self.company_id.id)]
        )
        data.update(
            {
                "company_id": self.company_id.id,
                "date_from": date(self.year, 1, 1).isoformat(),
                "date_to": date(self.year, 12, 31).isoformat(),
                "journal_ids": journals.ids,
                "move_target": "posted",
                "sort_option": "date",
                "group_option": "none",
                "foreign_currency": False,
                "with_account_name": self.with_account_name,
                "with_auto_sequence": True,
            }
        )
        return data

    def _action_b10_journal_ledger(self, action_xmlid):
        self.ensure_one()
        return self.env.ref(action_xmlid).report_action(
            self, data=self._prepare_b10_journal_ledger_data()
        )

    def action_view_b10_journal_ledger(self):
        return self._action_b10_journal_ledger(
            "b10_account.action_b10_journal_ledger_html"
        )

    def action_export_b10_journal_ledger_pdf(self):
        return self._action_b10_journal_ledger(
            "b10_account.action_b10_journal_ledger_pdf"
        )

    def action_export_b10_journal_ledger(self):
        return self._action_b10_journal_ledger(
            "b10_account.action_b10_journal_ledger_xlsx"
        )

from odoo import models


class TrialBalancePartnerWizard(models.TransientModel):
    _name = "b10.trial.balance.partner.wizard"
    _inherit = "trial.balance.report.wizard"
    _description = "Balanç de sumes i saldos per partner"

    def _prepare_report_data(self):
        data = super()._prepare_report_data()
        # These options are deliberately unavailable in the flat report.
        data.update(
            partner_ids=[], show_partner_details=False, show_hierarchy=False,
            limit_hierarchy_level=False, hide_parent_hierarchy_level=False,
            grouped_by=False,
        )
        return data

    def _print_report(self, report_type):
        self.ensure_one()
        suffix = {"qweb-html": "html", "qweb-pdf": "pdf", "xlsx": "xlsx"}[report_type]
        return self.env.ref(
            "b10_account.action_trial_balance_partner_" + suffix
        ).report_action(self, data=self._prepare_report_data())

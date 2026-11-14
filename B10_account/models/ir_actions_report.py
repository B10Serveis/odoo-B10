from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _get_rendering_context_model(self, report):
        if report.report_name == "B10_account.trial_balance_partner":
            return self.env["report.b10_account.trial_balance_partner"]
        return super()._get_rendering_context_model(report)

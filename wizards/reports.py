# Copyright 2024, 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, models, fields


class DammReportsWizard(models.TransientModel):
    _name = "damm_integration.reports.wizard"
    _description = "Wizard to help create reports for Damm"

    report_type = fields.Selection(
        [
            ("customers", "Customers Data"),
            ("conditions", "Commercial Conditions"),
            ("sales", "Sales"),
        ],
        string="Report type",
        required=True,
        default="sales",
    )

    @api.model
    def create(self, values):
        company = self.env.user.company_id
        dealer_code = company.damm_dealer_code
        if not dealer_code:
            raise exceptions.UserError("Please configure your company's Damm dealer code")
        damm_partner = company.damm_partner_id
        if not damm_partner:
            raise exceptions.UserError("Please configure which partner is the Damm company")
        return super(DammReportsWizard, self).create(values)

    def generate_report(self):
        self.ensure_one()
        raise NotImplementedError("TODO")

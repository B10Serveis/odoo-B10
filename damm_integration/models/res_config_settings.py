# Copyright 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_damm_integration = fields.Boolean(
        string="Damm integration",
        implied_group="damm_integration.res_groups_damm_integration")
    damm_dealer_code = fields.Char(
        related="company_id.damm_dealer_code", readonly=False,
        groups="damm_integration.res_groups_damm_integration")
    damm_partner_id = fields.Many2one(
        related="company_id.damm_partner_id", readonly=False,
        groups="damm_integration.res_groups_damm_integration")

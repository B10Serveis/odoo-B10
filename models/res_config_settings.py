# Copyright 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_damm_integration = fields.Boolean(
        string="Damm integration",
        implied_group="damm_integration.res_groups_damm_integration")

# Copyright 2026 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    b10_so_confirm_cancel = fields.Boolean(
        string="Confirm SO Cancellation",
        related="company_id.b10_so_confirm_cancel",
        readonly=False,
    )

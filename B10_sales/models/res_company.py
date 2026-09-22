# Copyright 2026 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    b10_so_confirm_cancel = fields.Boolean(
        string="Confirm SO Cancellation",
        default=True,
    )

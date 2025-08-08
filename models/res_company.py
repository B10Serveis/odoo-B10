# Copyright 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    damm_partner_id = fields.Many2one("res.partner", string="Damm company",
                                      help=("Used to locate products and customers"
                                            " when generating reports for Damm"),
                                      domain=[("name", "ilike", "damm")],
                                      ondelete="set null")

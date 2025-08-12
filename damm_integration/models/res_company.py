# Copyright 2025 Batista10
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    damm_dealer_code = fields.Char(string="Damm dealer code",
                                   help=("The code used by Damm to identify your company"
                                         " as a dealer of its products"))
    damm_partner_id = fields.Many2one("res.partner", string="Damm company",
                                      help=("Used to locate products and customers"
                                            " when generating reports for Damm"),
                                      domain=[("name", "ilike", "damm")],
                                      ondelete="set null")

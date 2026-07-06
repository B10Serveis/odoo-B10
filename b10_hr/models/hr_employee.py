from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    naf = fields.Char(
        string="NAF",
        help="Social Security affiliation number.",
    )

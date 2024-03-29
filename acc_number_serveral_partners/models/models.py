from odoo import models, fields


class ResPartnerBank_inherit(models.Model):
    _inherit = "res.partner.bank"

    _sql_constraints = [
        (
            "unique_number",
            "unique(sanitized_acc_number, company_id, partner_id)",
            "Account Number must be unique for Partner",
        ),
    ]

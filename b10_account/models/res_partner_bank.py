from odoo import models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    _unique_number = models.Constraint(
        "unique(sanitized_acc_number, company_id, partner_id)",
        "Account Number must be unique for Partner",
    )

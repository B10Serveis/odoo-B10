from odoo import models, fields

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    price_total_with_tax = fields.Float(
        string="Total Price with Taxes",
        readonly=True,
        group_operator='sum',
    )

    def _select(self):
        return super()._select() + ", price_total AS price_total_with_tax"

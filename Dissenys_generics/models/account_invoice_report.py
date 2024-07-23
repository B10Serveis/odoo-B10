from odoo import fields, models, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    price_total_with_tax = fields.Float(string="Total Price with Taxes", readonly=True)

    def _select(self):
        res = super(AccountInvoiceReport, self)._select()
        select_str = res + """, price_total AS price_total_with_tax  """
        return select_str

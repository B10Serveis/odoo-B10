from odoo import models

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # Set invoice bank account if payment journal is set in sale order.
    def _prepare_down_payment_invoice_values(self, order, so_lines):
        invoice_vals = super()._prepare_down_payment_invoice_values(order, so_lines)
        order._add_payment_to_invoice_vals(invoice_vals)
        return invoice_vals

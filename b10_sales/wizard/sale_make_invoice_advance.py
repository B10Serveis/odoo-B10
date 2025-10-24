from odoo import models

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    # Set invoice bank account if payment journal is set in sale order.
    def _prepare_invoice_values(self, order, so_line):
        invoice_vals = super()._prepare_invoice_values(order, so_line)
        if payment_journal := order.payment_journal_id:
            invoice_vals["partner_bank_id"] = payment_journal.bank_account_id.id
        return invoice_vals

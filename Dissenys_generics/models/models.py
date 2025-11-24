from odoo import models, fields, api


class SaleOrderInherited(models.Model):
    _inherit = "sale.order"
    show_product_image = fields.Boolean("Show product image")


class PaymentTermInherited(models.Model):
    _inherit = "account.payment.term"
    display_on_invoice = fields.Boolean("Show the terms of the invoice")


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    # Fem disponible bank_transfer per a tots els diaris de tipus bancari.
    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res["bank_transfer"] = {
            "mode": "multi",
            "domain": [("type", "=", "bank")],
        }
        return res

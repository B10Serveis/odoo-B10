from odoo import models, fields, api


class SaleOrderInherited(models.Model):
    _inherit = "sale.order"
    show_product_image = fields.Boolean("Show product image")


class PaymentTermInherited(models.Model):
    _inherit = "account.payment.term"
    display_on_invoice = fields.Boolean("Show the terms of the invoice")

from odoo import models, fields, api


class SaleOrderInherited(models.Model):
    _inherit = "sale.order"
    show_product_image = fields.Boolean("Show product image", requiered=False)

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    auto_sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Source Sales Order",
        readonly=True,
        copy=False,
    )

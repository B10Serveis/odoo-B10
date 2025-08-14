from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    auto_sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Source Sales Order Line",
        readonly=True,
        copy=False,
    )

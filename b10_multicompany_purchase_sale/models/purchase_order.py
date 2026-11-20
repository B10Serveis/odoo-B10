from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _inter_company_create_sale_order(self, dest_company):
        self.ensure_one()
        if self.auto_sale_order_id:
            # This purchase is already the counterpart of a B10 sale.
            return self.auto_sale_order_id
        existing_sale = self.env["sale.order"].sudo().search(
            [("auto_purchase_order_id", "=", self.id), ("state", "!=", "cancel")],
            limit=1,
        )
        if existing_sale:
            return existing_sale
        return super()._inter_company_create_sale_order(dest_company)

    def button_cancel(self):
        cancelling_purchase_ids = self.env.context.get("b10_cancelling_purchase_ids", ())
        purchases = self.filtered(
            lambda purchase: purchase.id not in cancelling_purchase_ids
        )
        if not purchases:
            return True
        purchases = purchases.with_context(
            b10_cancelling_purchase_ids=list(cancelling_purchase_ids) + purchases.ids
        )
        return super(PurchaseOrder, purchases).button_cancel()

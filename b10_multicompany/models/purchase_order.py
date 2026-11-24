from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    _B10_OPTIONAL_INTERCOMPANY_METHODS = (
        "_inter_company_create_sale_order",
        "button_cancel",
    )

    auto_sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Source Sales Order",
        readonly=True,
        copy=False,
    )

    def _inter_company_create_sale_order(self, dest_company):
        """Avoid creating an OCA sale for a purchase already created by B10."""
        self.ensure_one()
        existing_sale = self._b10_find_intercompany_sale()
        if existing_sale:
            return existing_sale

        # OCA's optional purchase_sale_inter_company module provides this method.
        # Keep b10_multicompany installable when that module is absent.
        parent_method = getattr(
            super(), "_inter_company_create_sale_order", None
        )
        return parent_method(dest_company) if parent_method else False

    def _b10_find_intercompany_sale(self):
        self.ensure_one()
        if self.auto_sale_order_id:
            return self.auto_sale_order_id
        return self.env["sale.order"].sudo().search(
            [("auto_purchase_order_id", "=", self.id), ("state", "!=", "cancel")],
            limit=1,
        )

    def button_cancel(self):
        """Carry a recursion guard through OCA's linked-sale cancellation."""
        return self._b10_button_cancel_with_guard(
            lambda purchases: super(PurchaseOrder, purchases).button_cancel()
        )

    def _b10_button_cancel_with_guard(self, cancel_method):
        cancelling_purchase_ids = self.env.context.get(
            "b10_cancelling_purchase_ids", ()
        )
        purchases = self.filtered(
            lambda purchase: purchase.id not in cancelling_purchase_ids
        )
        if not purchases:
            return True
        purchases = purchases.with_context(
            b10_cancelling_purchase_ids=(
                list(cancelling_purchase_ids) + purchases.ids
            )
        )
        return cancel_method(purchases)

    def _register_hook(self):
        """Wrap optional OCA methods after all modules have extended the model.

        The OCA module is deliberately not a dependency. When it loads after
        this module, its overrides would otherwise sit ahead of B10's guards
        in the model method resolution order.
        """
        result = super()._register_hook()
        model_class = type(self)
        for method_name in self._B10_OPTIONAL_INTERCOMPANY_METHODS:
            current_method = getattr(model_class, method_name)
            if current_method.__module__.startswith(
                "odoo.addons.b10_multicompany."
            ):
                continue
            marker = f"_b10_original_{method_name.replace('.', '_')}"
            if marker in model_class.__dict__:
                continue

            setattr(model_class, marker, current_method)
            if method_name == "_inter_company_create_sale_order":

                def guarded_create(order, dest_company, original=current_method):
                    order.ensure_one()
                    existing_sale = order._b10_find_intercompany_sale()
                    if existing_sale:
                        return existing_sale
                    return original(order, dest_company)

                setattr(model_class, method_name, guarded_create)
            else:

                def guarded_cancel(order, original=current_method):
                    return order._b10_button_cancel_with_guard(original)

                setattr(model_class, method_name, guarded_cancel)
        return result

    def _unregister_hook(self):
        model_class = type(self)
        for method_name in self._B10_OPTIONAL_INTERCOMPANY_METHODS:
            marker = f"_b10_original_{method_name.replace('.', '_')}"
            original = model_class.__dict__.get(marker)
            if original:
                setattr(model_class, method_name, original)
                delattr(model_class, marker)
        return super()._unregister_hook()

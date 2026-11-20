from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    intercompany_purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        compute="_compute_intercompany_purchase_order_id",
        compute_sudo=True,
    )

    auto_purchase_order_id = fields.Many2one(  
        comodel_name="purchase.order",
        string="Linked Purchase Order",
        readonly=True,
        copy=False,
    )

    def _compute_intercompany_purchase_order_id(self):
        """Find the PO created automatically from this SO."""
        ids_dict_list = self.env["purchase.order"].search_read(
            [("auto_sale_order_id", "in", self.ids)],
            ["id", "auto_sale_order_id"],
        )
        ids_dict = {d["auto_sale_order_id"][0]: d["id"] for d in ids_dict_list}
        for order in self:
            order.intercompany_purchase_order_id = ids_dict.get(order.id, False)

    def _check_intercompany_product(self, dest_company):
        for sale_line in self.order_line:
            sale_line._check_intercompany_product(dest_company)

    def action_confirm(self):
        """When confirming a SO, if the customer is another company in the system
        and the destination company has po_from_so enabled, create the mirror PO."""
        res = super().action_confirm()
        for sale in self.sudo():
            # OCA-generated sales and sales with a mirror purchase are already linked.
            if sale.auto_purchase_order_id:
                continue
            dest_company = sale.partner_id.commercial_partner_id.ref_company_ids
            if dest_company and dest_company.po_from_so:
                sale.with_company(dest_company.id)._inter_company_create_purchase_order(
                    dest_company
                )

        return res

    def _inter_company_create_purchase_order(self, dest_company):
        """Create a Purchase Order in the destination company from this SO."""
        self.ensure_one()
        if self.auto_purchase_order_id:
            return self.auto_purchase_order_id
        existing_purchase = self.env["purchase.order"].sudo().search(
            [("auto_sale_order_id", "=", self.id), ("state", "!=", "cancel")],
            limit=1,
        )
        if existing_purchase:
            self.auto_purchase_order_id = existing_purchase
            return existing_purchase
        intercompany_user = dest_company.intercompany_purchase_user_id or self.env.user

        # Pre-checks
        self._check_intercompany_product(dest_company)

        # The vendor of the PO will be the partner of the source company
        vendor_partner = self.company_id.partner_id

        # Currency coherence between SO and price list/destination company
        if self.currency_id.id != (
            vendor_partner.property_purchase_currency_id.id or dest_company.currency_id.id
        ):
            # NB: property_purchase_currency_id is not always defined; it is compared with the company one if necessary
            raise UserError(
                _(
                    "You cannot create PO from SO because "
                    "purchase currency is different than sale order currency."
                )
            )

        # PO data
        po_vals = self._prepare_purchase_order_data(
            self.client_order_ref or self.name, vendor_partner, dest_company, self.partner_shipping_id
        )
        purchase = (
            self.env["purchase.order"]
            .with_user(intercompany_user.id)
            .sudo()
            .create(po_vals)
        )

        # Message in the PO chat
        purchase.sudo().message_post(
            body=_(
                "This purchase order has been automatically created "
                "from an intercompany sale order (%s)."
            ) % self.name,
            message_type="comment",
        )

        # PO lines
        for so_line in self.order_line:
            pol_vals = self._prepare_purchase_order_line_data(
                so_line, dest_company, purchase
            )
            pol = (
                self.env["purchase.order.line"]
                .with_user(intercompany_user.id)
                .sudo()
                .create(pol_vals)
            )
            # backlink to sales line
            so_line.auto_purchase_line_id = pol.id

        # Write vendor reference to SO
        if not self.client_order_ref:
            self.client_order_ref = purchase.name

        # Set the link before confirmation can trigger other intercompany rules.
        self.auto_purchase_order_id = purchase.id

        # PO validation if applicable
        if dest_company.purchase_auto_validation:
            purchase.with_user(intercompany_user.id).sudo().button_confirm()

        return purchase

    def _prepare_purchase_order_data(
        self, origin_ref, vendor_partner, dest_company, shipping_address
    ):
        """Generate the PO values from the SO."""
        self.ensure_one()
        new_order = self.env["purchase.order"].new(
            {
                "company_id": dest_company.id,
                "partner_id": vendor_partner.id,
                "date_order": self.date_order,
                "origin": origin_ref,
                "auto_sale_order_id": self.id,
                "dest_address_id": shipping_address.id if shipping_address else False,
                "notes": self.note or False,
                "partner_ref": self.name,
            }
        )
        for onchange in new_order._onchange_methods.get("partner_id", []):
            onchange(new_order)
        # dates
        if self.commitment_date:
            new_order.date_planned = self.commitment_date
        return new_order._convert_to_write(new_order._cache)


    def _prepare_purchase_order_line_data(self, sale_line, dest_company, purchase_order):
        # Create a line with essential information for onchange
        new_line = self.env["purchase.order.line"].new(
            {
                "order_id": purchase_order.id,
                "product_id": sale_line.product_id.id,
                "product_uom": sale_line.product_uom.id,
                "display_type": sale_line.display_type,
            }
        )

        # Execute onchanges so that Odoo calculates default values
        for onchange in new_line._onchange_methods.get("product_id", []):
            onchange(new_line)

        # Override the values we want from the SO
        new_line.update(
            {
                "product_uom": sale_line.product_uom.id,
                "product_qty": sale_line.product_uom_qty,
                "price_unit": sale_line.price_unit,
                "discount": sale_line.discount,
                "auto_sale_line_id": sale_line.id,
                "name": sale_line.name,
            }
        )

        return new_line._convert_to_write(new_line._cache)

    def _action_cancel(self):
        """Cancel mirror purchases after the user has confirmed cancellation."""
        cancelling_sale_ids = self.env.context.get("b10_cancelling_sale_ids", ())
        sales = self.filtered(lambda sale: sale.id not in cancelling_sale_ids)
        if not sales:
            return True
        sales = sales.with_context(
            b10_cancelling_sale_ids=list(cancelling_sale_ids) + sales.ids
        )
        purchase_orders = (
            sales.env["purchase.order"]
            .sudo()
            .search([("auto_sale_order_id", "in", sales.ids)])
        )
        cancelling_purchase_ids = self.env.context.get("b10_cancelling_purchase_ids", ())
        pending_purchases = purchase_orders.filtered(
            lambda purchase: purchase.id not in cancelling_purchase_ids
            and purchase.state != "cancel"
        )
        for po in pending_purchases:
            if po.state not in ["draft", "sent", "to approve", "cancel"]:
                raise UserError(_("You can't cancel an order that is %s") % po.state)
        pending_purchases.button_cancel()
        # Preserve OCA source links; only reset links to purchases generated by B10.
        target_sale_ids = purchase_orders.auto_sale_order_id.ids
        sales.filtered(lambda sale: sale.id in target_sale_ids).write(
            {"auto_purchase_order_id": False}
        )
        return super(SaleOrder, sales)._action_cancel()

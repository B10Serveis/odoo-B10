from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    intercompany_purchase_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        compute="_compute_intercompany_purchase_line_id",
        compute_sudo=True,
    )

    auto_purchase_line_id = fields.Many2one(  
        comodel_name="purchase.order.line",
        string="Linked Purchase Order Line",
        readonly=True,
        copy=False,
    )

    def _compute_intercompany_purchase_line_id(self):
        """Find the purchase lines generated from these sale lines in a batch."""
        purchase_lines = self.env["purchase.order.line"].search_read(
            [("auto_sale_line_id", "in", self.ids)],
            ["id", "auto_sale_line_id"],
        )
        purchase_by_sale = {
            line["auto_sale_line_id"][0]: line["id"] for line in purchase_lines
        }
        for line in self:
            line.intercompany_purchase_line_id = purchase_by_sale.get(line.id, False)

    def _check_intercompany_product(self, dest_company):
        for line in self:
            product_company = line.product_id.company_id
            if product_company and product_company != dest_company:
                raise UserError(
                    _(
                        "You cannot create PO from SO because product '%s' "
                        "is not intercompany"
                    )
                    % line.product_id.name
                )

    @api.onchange("product_uom_qty")
    def _onchange_product_uom_qty_warn_intercompany(self):
        """Warns the user that changing the quantity in the SO does not synchronize the PO."""
        for line in self:
            # Only warn if it's an intercompany sale and there's a linked PO line
            if line.order_id.auto_purchase_order_id and line.auto_purchase_line_id:
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _(
                            "Changing the quantity here does not update the linked purchase "
                            "order. Review its quantity separately and adjust it if needed."
                        ),
                    }
                }
    
    @api.onchange("price_unit", "discount")
    def _onchange_price_unit_warn_intercompany(self):
        """Warn that price and discount edits do not immediately update the purchase."""
        for line in self:
            # Only warn if it's an intercompany sale and there's a linked PO line
            if line.order_id.auto_purchase_order_id and line.auto_purchase_line_id:
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _(
                            "Changing the price or discount here does not immediately update "
                            "the linked purchase order. Review its net amount separately "
                            "and adjust it if needed."
                        ),
                    }
                }
            
    @api.onchange("tax_id")
    def _onchange_tax_id_warn_intercompany(self):
        """Warns the user that changing the tax_id in the SO does not synchronize the PO."""
        for line in self:
            # Only warn if it's an intercompany sale and there's a linked PO line
            if line.order_id.auto_purchase_order_id and line.auto_purchase_line_id:
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _(
                            "Changing the taxes here does not update the linked purchase "
                            "order. Review its taxes separately, according to that "
                            "company's fiscal rules."
                        ),
                    }
                }
            
    @api.onchange("product_id")
    def _onchange_product_added_warn_intercompany(self):
        """Warn when adding a product without a linked purchase line."""
        for line in self:
            # Ignore sections/notes
            if line.display_type in ("line_section", "line_note"):
                continue
            # SO intercompany and line NOT yet linked to PO
            if line.order_id.auto_purchase_order_id and not line.auto_purchase_line_id and line.product_id:
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _(
                            "Adding a product here does not create a line in the linked "
                            "purchase order. Review the linked order before adding "
                            "or changing its lines."
                        ),
                    }
                }

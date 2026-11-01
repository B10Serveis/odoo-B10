# Copyright (C) 2026 Batista10 (https://www.batista10.cat/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleSubscriptionLine(models.Model):
    _name = "sale.subscription.line"
    _inherit = ["sale.subscription.line", "analytic.mixin"]
    _order = "sale_subscription_id, sequence, id"

    sequence = fields.Integer(default=10, help="Display order on the subscription.")
    display_type = fields.Selection(
        selection=[("line_section", "Section"), ("line_note", "Note")],
        default=False,
        help="Technical field for sorting lines in the user interface.",
    )

    @api.onchange("product_id")
    def _onchange_product_id_analytic_distribution(self):
        for line in self:
            if not line.product_id or line.display_type:
                continue
            analytic_account = line.product_id.income_analytic_account_id
            if not analytic_account:
                analytic_account = (
                    line.product_id.categ_id.income_analytic_account_id
                )
            if analytic_account:
                line.analytic_distribution = {str(analytic_account.id): 100.0}

    @api.depends(
        "product_id",
        "price_unit",
        "product_uom_qty",
        "discount",
        "tax_ids",
        "display_type",
    )
    def _compute_subtotal(self):
        display_lines = self.filtered(lambda line: line.display_type)
        for line in display_lines:
            line.update(
                {
                    "amount_tax_line_amount": 0.0,
                    "price_total": 0.0,
                    "price_subtotal": 0.0,
                }
            )
        product_lines = self - display_lines
        if product_lines:
            super(SaleSubscriptionLine, product_lines)._compute_subtotal()

    @api.depends("product_id", "display_type")
    def _compute_name(self):
        product_lines = self.filtered(lambda line: not line.display_type)
        if product_lines:
            super(SaleSubscriptionLine, product_lines)._compute_name()

    @api.depends(
        "product_id",
        "display_type",
        "sale_subscription_id.fiscal_position_id",
    )
    def _compute_tax_ids(self):
        display_lines = self.filtered(lambda line: line.display_type)
        for line in display_lines:
            line.tax_ids = [fields.Command.clear()]
        product_lines = self - display_lines
        if product_lines:
            super(SaleSubscriptionLine, product_lines)._compute_tax_ids()

    @api.depends(
        "product_id",
        "sale_subscription_id.partner_id",
        "sale_subscription_id.pricelist_id",
        "display_type",
    )
    def _compute_price_unit(self):
        display_lines = self.filtered(lambda line: line.display_type)
        for line in display_lines:
            line.price_unit = 0.0
        product_lines = self - display_lines
        if product_lines:
            super(SaleSubscriptionLine, product_lines)._compute_price_unit()

    @api.depends(
        "product_id",
        "price_unit",
        "product_uom_qty",
        "tax_ids",
        "sale_subscription_id.partner_id",
        "sale_subscription_id.pricelist_id",
        "display_type",
    )
    def _compute_discount(self):
        display_lines = self.filtered(lambda line: line.display_type)
        for line in display_lines:
            line.discount = 0.0
        product_lines = self - display_lines
        if product_lines:
            super(SaleSubscriptionLine, product_lines)._compute_discount()

    def _prepare_sale_order_line(self):
        self.ensure_one()
        if self.display_type:
            return {
                "display_type": self.display_type,
                "name": self.name or "",
                "sequence": self.sequence,
            }
        values = super()._prepare_sale_order_line()
        values["sequence"] = self.sequence
        values["analytic_distribution"] = self.analytic_distribution
        return values

    def _prepare_account_move_line(self):
        self.ensure_one()
        if self.display_type:
            return {
                "display_type": self.display_type,
                "name": self.name or "",
                "sequence": self.sequence,
            }
        values = super()._prepare_account_move_line()
        values["sequence"] = self.sequence
        values["analytic_distribution"] = self.analytic_distribution
        return values

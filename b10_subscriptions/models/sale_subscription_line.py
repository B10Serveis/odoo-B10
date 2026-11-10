# Copyright (C) 2026 Batista10 (https://www.batista10.cat/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleSubscriptionLine(models.Model):
    _name = "sale.subscription.line"
    _inherit = ["sale.subscription.line", "analytic.mixin"]

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

    def _prepare_sale_order_line(self):
        values = super()._prepare_sale_order_line()
        if self.display_type:
            return values
        values["analytic_distribution"] = self.analytic_distribution
        return values

    def _prepare_account_move_line(self):
        values = super()._prepare_account_move_line()
        if self.display_type:
            return values
        values["analytic_distribution"] = self.analytic_distribution
        return values

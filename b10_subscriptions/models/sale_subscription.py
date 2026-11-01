# Copyright (C) 2026 Batista10 (https://www.batista10.cat/).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def create_sale_order(self):
        self.ensure_one()
        order = super().create_sale_order()
        if not order:
            return order

        subscription_lines = self.sale_subscription_line_ids.sorted(
            key=lambda line: (line.sequence, line.id)
        )
        order_lines = order.order_line.sorted(
            key=lambda line: (line.sequence, line.id)
        )
        for subscription_line, order_line in zip(subscription_lines, order_lines):
            if not subscription_line.display_type:
                # Sale order lines may compute a distribution from automatic rules.
                # The one entered on the subscription is the recurring source of truth.
                order_line.analytic_distribution = (
                    subscription_line.analytic_distribution
                )
        return order

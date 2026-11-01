# Copyright (C) 2025 Batista10 (https://www.batista10.cat/).
# @author: Joan Llimiñana <joan@batista10.cat>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, exceptions, api, _


class helpdeksB10Subscription(models.Model):
    _inherit = "helpdesk.ticket"
    related_subscription = fields.Many2one(
        "sale.subscription",
        string="Subscription",
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if (
            self.related_subscription
            and self.related_subscription.partner_id != self.partner_id
        ):
            self.related_subscription = False
        return result

    @api.constrains("partner_id", "related_subscription")
    def _check_subscription_partner(self):
        for ticket in self:
            if (
                ticket.related_subscription
                and ticket.related_subscription.partner_id != ticket.partner_id
            ):
                raise exceptions.ValidationError(
                    _("The subscription must belong to the ticket customer.")
                )

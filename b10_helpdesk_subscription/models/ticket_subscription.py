# Copyright (C) 2025 Batista10 (https://www.batista10.cat/).
# @author: Joan Llimiñana <joan@batista10.cat>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"
    related_subscription = fields.Many2one(
        "sale.subscription",
        string="Subscription",
    )

    subscription_current_date = fields.Date(
        string="Current date", compute="_compute_subscription_current_date"
    )

    @api.depends_context("tz")
    def _compute_subscription_current_date(self):
        for ticket in self:
            ticket.subscription_current_date = fields.Date.context_today(ticket)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if (
            self.related_subscription
            and self.related_subscription.partner_id != self.partner_id
        ):
            self.related_subscription = False
        return result

    @api.onchange("company_id")
    def _onchange_subscription_company(self):
        if (
            self.related_subscription
            and self.related_subscription.company_id != self.company_id
        ):
            self.related_subscription = False

    @api.constrains("company_id", "related_subscription")
    def _check_subscription_company(self):
        for ticket in self:
            if (
                ticket.related_subscription
                and ticket.related_subscription.company_id != ticket.company_id
            ):
                raise ValidationError(
                    _("The subscription must belong to the ticket company.")
                )

    @api.constrains("partner_id", "related_subscription")
    def _check_subscription_partner(self):
        for ticket in self:
            if (
                ticket.related_subscription
                and ticket.related_subscription.partner_id != ticket.partner_id
            ):
                raise ValidationError(
                    _("The subscription must belong to the ticket customer.")
                )

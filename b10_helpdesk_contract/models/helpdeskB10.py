from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    related_contract = fields.Many2one("contract.contract", string="Contract")

    @api.constrains("related_contract", "partner_id", "company_id")
    def _check_related_contract(self):
        for ticket in self:
            contract = ticket.related_contract
            if not contract:
                continue
            allowed_partners = ticket.partner_id | ticket.partner_id.commercial_partner_id
            if not ticket.partner_id or contract.partner_id not in allowed_partners:
                raise ValidationError(
                    _(
                        "The contract must belong to the ticket contact or its commercial entity."
                    )
                )
            if contract.company_id and contract.company_id != ticket.company_id:
                raise ValidationError(
                    _("The contract must belong to the same company as the ticket.")
                )

    current_date = fields.Date(string="Current date", compute="_compute_current_date")

    @api.depends_context("tz")
    def _compute_current_date(self):
        for ticket in self:
            ticket.current_date = fields.Date.context_today(ticket)

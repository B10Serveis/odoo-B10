from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
import logging


class helpdeksB10(models.Model):
    _inherit = "helpdesk.ticket"
    internal_note = fields.Html(
        string="Internal Note",
        required=False,
    )
    close_note = fields.Html(
        string="Closing Note",
        required=False,
    )
    ticket_company_id = fields.Many2one(
        comodel_name="res.company",
        related="company_id",
    )
    commercial_partner_id = fields.Many2one(
        string="Commercial Partner",
        related="partner_id.commercial_partner_id",
        store=True,
    )
    related_contract = fields.Many2one("contract.contract", string="Contract")

    @api.constrains("related_contract", "partner_id", "company_id")
    def _check_related_contract(self):
        for ticket in self:
            contract = ticket.related_contract
            if not contract:
                continue
            allowed_partners = ticket.partner_id | ticket.partner_id.commercial_partner_id
            if not ticket.partner_id or contract.partner_id not in allowed_partners:
                raise ValidationError(_(
                    "The contract must belong to the ticket contact or its commercial entity."
                ))
            if contract.company_id and contract.company_id != ticket.company_id:
                raise ValidationError(_(
                    "The contract must belong to the same company as the ticket."
                ))

    worked_hours = fields.Float(string="Worked Hours")
    stage_closed = fields.Boolean(string="Stage closed", related="stage_id.closed")

    # Fer servir per ticket de Contractes Caducats
    current_time = fields.Datetime(string="Current time", compute="_get_current_time")

    def _get_current_time(self):
        for li in self:
            li.current_time = fields.datetime.now()

    @api.onchange("close_note")
    def on_change_state(self):
        for rec in self:
            if rec.worked_hours == 0 and rec.stage_closed == 1:
                return {
                    "warning": {
                        "title": "Empty Worked Hours",
                        "message": "Value from Wroked Hours can't be 0",
                        "type": "notification",
                    },
                }

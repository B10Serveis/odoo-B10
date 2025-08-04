from odoo import api, models, fields, _
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
    email_ccs = fields.Many2many(
        "res.partner",
        "ticket_partner_rel",
        "ticket_ids",
        "partner_id",
        string="CC",
        domain=[("email", "=like", "%@%")],
    )
    related_contract = fields.Many2one("contract.contract", string="Contract")
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


class partner_helpdesk_B10(models.Model):
    _inherit = "res.partner"
    cc_email = fields.Many2many(
        "helpdesk.ticket", "ticket_partner_rel", "partner_id", "ticket_ids"
    )

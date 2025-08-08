from odoo import api, models, fields, _

class helpdeskB10(models.Model):
    _inherit = "helpdesk.ticket"
    internal_note = fields.Html(
        string="Internal Note",
        required=False,
    )
    close_note = fields.Html(
        string="Closing Note",
        required=False,
    )

    worked_hours = fields.Float(string="Worked Hours")
    stage_closed = fields.Boolean(string="Stage closed", related="stage_id.closed")

    @api.onchange("close_note")
    def on_change_state(self):
        for rec in self:
            if rec.worked_hours == 0 and rec.stage_closed == 1:
                return {
                    "warning": {
                        "title": "Empty Worked Hours",
                        "message": "Value from Worked Hours can't be 0",
                        "type": "notification",
                    },
                }

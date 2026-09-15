from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class model520_wizard(models.TransientModel):
    _name = 'model520.wizard'
    _description = 'Wizard Model 520 IBEE'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_start and wizard.date_end and wizard.date_end < wizard.date_start:
                raise ValidationError(_("The end date must be on or after the start date."))

    def get_report(self):
        self.ensure_one()
        return self.env.ref('IBEE.model520_report').report_action(self, data={
            'date_start': fields.Date.to_string(self.date_start),
            'date_end': fields.Date.to_string(self.date_end),
        })
        

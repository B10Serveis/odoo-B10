import datetime
import pytz
import time
from odoo import api, fields, models

class model520(models.AbstractModel):
  
    _name = 'report.model520_report'

    @api.model
    def report_values(self, date_start=False, date_end=False):  
        user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
        today = user_tz.localize(fields.Datetime.to_datetime(fields.Date.context_today(self)))
        today = today.astimezone(pytz.timezone('UTC'))
        if date_start:
            date_start = fields.Datetime.to_datetime(date_start)
        else:
            date_start = today

        if date_end:
            date_end = fields.Datetime.to_datetime(date_end)
        else:
            date_end = today + timedelta(days=1, seconds=-1)

        date_end = max(date_end, date_start)

        date_start = fields.Datetime.to_datetime(date_start)
        date_end = fields.Datetime.to_datetime(date_end)

        
        invoices = self.env['account.invoice'].search([
            ('date_invoice', '>=', date_start),
            ('date_invoice', '<=', date_end),
            ], order='name asc')
        
        return {
            'date_start': date_start,
            'date_end': date_end,
            'invoices': [{
                'invoice_id' : invoice.id,
                'invoice_name' : invoice.name,
                'invoice_data' : invoice.date_invoice,
                'invoice_partner' : invoice.partner_id.name,
                'invoice_total' : invoice.amount_total,              
                } for invoice in invoices],
            }
        
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
   
       
        invoices_linies = self.env['account.invoice.line'].search([
            ('invoice_id.date_invoice', '>=', date_start),
            ('invoice_id.date_invoice', '<=', date_end),
            ])
        
        IBEE8 = 0
        
        for invoice in invoices_linies:
            IBEE8 += invoice.IBEE_invoice
            
        
        return {
            'date_start': date_start,
            'date_end': date_end,
            'invoices_linies': [{
                'ID' : linies.id,
                'IBEE' : linies.IBEE_invoice,
                'name' : linies.partner_id.name,                         
                } for linies in invoices_linies],
            'IBEE8' : IBEE8,
            }
        
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
        
        company_id = self.env.user.company_id   
       
        invoices_linies = self.env['account.invoice.line'].search([
            ('invoice_id.date_invoice', '>=', date_start),
            ('invoice_id.date_invoice', '<=', date_end),
            ])
        
        IBEE8 = 0
        IBEE5 = 0
        
        for invoice in invoices_linies:
            if invoice.product_id.IBEE == '0.15':
                IBEE8 += invoice.product_id.litres_IBEE * invoice.quantity
            if invoice.product_id.IBEE == '0.1':
                IBEE5 += invoice.product_id.litres_IBEE * invoice.quantity
        
        quota_IBEE8 = IBEE8 * 0.15    
        quota_IBEE5 = IBEE5 * 0.1
        
        total = quota_IBEE5 + quota_IBEE8
        
        return {
            'NIF': company_id.vat,
            'name': company_id.name,
            'street': company_id.street,
            'codpostal': company_id.zip,
            'pais': company_id.country_id.name,
            'provincia': company_id.state_id.name,
            'municipi': company_id.city,
            'IBEE8' : round(IBEE8,2),
            'IBEE5' : round(IBEE5,2),
            'quota_IBEE8' : round(quota_IBEE8,2),
            'quota_IBEE5' : round(quota_IBEE5,2),
            'total' : total,                                 
            }
        
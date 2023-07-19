from odoo import models, fields

class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'
    
    total_ibee = fields.Float('Total IBEE', readonly=True)
    
    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.total_ibee as total_ibee "
 
    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ", SUM(ail.ibee_invoice) AS total_ibee "
  
    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", ail.ibee_invoice "
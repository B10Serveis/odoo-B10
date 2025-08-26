from odoo import models, fields

class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'
    
    total_ibee = fields.Float('Total IBEE', readonly=True)
    
    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.total_ibee as total_ibee "
 
    def _sub_select(self):
        group = self.env.ref('IBEE.tax_group_ibee', raise_if_not_found=False)
        group_id = group.id if group else 0
        # Suma el 'balance' de les línies d'impost del grup IBEE
        return super(AccountInvoiceReport, self)._sub_select() + f"""
            , SUM(
                CASE
                  WHEN ail.tax_line_id IS NOT NULL
                   AND EXISTS (SELECT 1 FROM account_tax at WHERE at.id = ail.tax_line_id AND at.tax_group_id = {group_id})
                  THEN ail.balance
                  ELSE 0
                END
            ) AS total_ibee
        """
  
    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by()
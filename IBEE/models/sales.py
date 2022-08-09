from odoo import models, fields, api

class sale_order_line_IBEE(models.Model):
    _inherit = 'sale.order.line'

    IBEE_sale = fields.Float(string='IBEE',compute='_compute_IBEE')

  
    @api.depends('product_id','product_uom_qty')
    def _compute_IBEE(self):
        Line_IBEE = 0.0
        for line in self:
            Line_IBEE = line.product_id.litres_IBEE * float(line.product_id.IBEE) * line.product_uom_qty
            line.IBEE_sale = Line_IBEE
            line.price_subtotal += Line_IBEE
            line.price_total += Line_IBEE
            
            
#class sale_ordre_IBEE(models.Model):
#    _inherit = 'sale.order'
    
#    IBEE_total = fields.Float(string='IBEE total',compute='_total_IBEE')
    
#    @api.depends('order_line.price_total')
#    def _total_IBEE(self):
#        Impost = 0.0
#        for order in self:        
#            for line in order.order_line:            
#                Impost += line.IBEE_sale
#            order.update({
#                'IBEE_total': (Impost),
#                'amount_untaxed': (Impost + order.amount_untaxed),
#                'amount_tax': (Impost + order.amount_tax)
                
#            })
        
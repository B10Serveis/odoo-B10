from odoo import models, fields


class product(models.Model):
    _inherit = 'product.template'

    IBEE = fields.Selection((('0','Exempt'),('0.1','0.1'),('0.15','0.15')),'IBEE', default='0')
    litres_IBEE = fields.Float('Liters IBEE', default=0)

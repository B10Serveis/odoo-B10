from odoo import models, fields


class product(models.Model):
    _inherit = 'product.template'

    PuntoVerde = fields.Float('PuntoVerde', default=0, digits=(12, 3))

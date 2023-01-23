from odoo import models, fields


class product(models.Model):
    _inherit = 'product.template'

    PuntoVerde = fields.Float('Punt Verd', default=0, digits=(12, 3))

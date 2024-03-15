from odoo import models, fields, api


class ccpae(models.Model):
    _inherit = "product.template"
    ccpae = fields.Boolean("Product CCPAE", required=False)

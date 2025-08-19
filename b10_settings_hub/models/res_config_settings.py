from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_b10_account  = fields.Boolean(string="b10_account")
    module_b10_contacts = fields.Boolean(string="b10_contacts")
    module_b10_contracts = fields.Boolean(string="b10_contracts")
    module_b10_crm     = fields.Boolean(string="b10_crm")
    module_b10_helpdesk = fields.Boolean(string="b10_helpdesk")
    module_b10_pos     = fields.Boolean(string="b10_pos")
    module_b10_purchases = fields.Boolean(string="b10_purchases")
    module_b10_sales    = fields.Boolean(string="b10_sales")
    module_b10_stock_picking = fields.Boolean(string="b10_stock_picking")


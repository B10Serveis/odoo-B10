from odoo import models, fields, api


class ProductInherited(models.Model):

    _inherit = "product.template"
    print_group = fields.Boolean(string="Agrupar productes", required=False)


class SaleOrderInherited(models.Model):

    _inherit = 'sale.order'
    print_group_description = fields.Text(
        string="Project Task Description", required=False, default="Materials varis")


class AccountMoveInherited(models.Model):

    _inherit = 'account.move'
    print_group_description = fields.Text(
        string="Project Task Description", required=False, default="Materials varis")

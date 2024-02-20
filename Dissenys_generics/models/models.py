from odoo import models, fields, api
from odoo.http import request


class SaleOrderInherited(models.Model):
    _inherit = "sale.order"
    show_product_image = fields.Boolean("Show product image", required=False)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_lines_by_origin = fields.Boolean(
        string="Group invoice lines by origin",
        config_parameter="dissenys_generics.invoice_lines_by_origin",
        help="Groups invoice lines by origin on the standard designs",
    )


class AccountMove(models.Model):
    _inherit = "account.move"

    group_by_origin = fields.Boolean(string="Group Invoice Lines by Origin")

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)

        res.group_by_origin = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("dissenys_generics.invoice_lines_by_origin")
        )
        return res

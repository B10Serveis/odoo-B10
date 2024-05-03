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

    # Modificacions per error de cron:
    # -Creem get_invoice_lines_by_origin() per poder obtenir el valor sense request.
    def get_invoice_lines_by_origin(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("dissenys_generics.invoice_lines_by_origin", False)
        )


class AccountMove(models.Model):
    _inherit = "account.move"

    group_by_origin = fields.Boolean(string="Group Invoice Lines by Origin")

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        # Modificacions error cron:
        # -Accedim a ResConfigSettings amb self.env["res.config.settings"].sudo() i cridem get_invoice_lines_by_origin() per obtenir el parametre.
        settings = self.env["res.config.settings"].sudo()  # Access settings model
        res.group_by_origin = settings.get_invoice_lines_by_origin()
        return res

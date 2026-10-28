from odoo import models, fields, api
from odoo.http import request
from odoo.tools.misc import str2bool


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
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("dissenys_generics.invoice_lines_by_origin", False)
        )
        return str2bool(value, default=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    group_by_origin = fields.Boolean(string="Group Invoice Lines by Origin")

    @api.model_create_multi
    def create(self, vals_list):
        if any("group_by_origin" not in vals for vals in vals_list):
            settings = self.env["res.config.settings"].sudo()
            default_group_by_origin = settings.get_invoice_lines_by_origin()
            vals_list = [
                dict(vals, group_by_origin=vals.get("group_by_origin", default_group_by_origin))
                for vals in vals_list
            ]
        return super().create(vals_list)


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    # Fem disponible bank_transfer per a tots els diaris de tipus bancari.
    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res["bank_transfer"] = {
            "mode": "multi",
            "domain": [("type", "=", "bank")],
        }
        return res

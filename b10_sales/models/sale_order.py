from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_product_image = fields.Boolean("Show product image", required=False)

    def _get_default_mail_template_id(self):
        self.ensure_one()
        # Proforma?
        if self.env.context.get("proforma"):
            return self.env.ref(
                "b10_sales.proforma_email_template",
                raise_if_not_found=False,
            ).id
        # Pressupost
        if self.state in ("draft", "sent"):
            return self.env.ref(
                "b10_sales.pressupost_email_template",
                raise_if_not_found=False,
            ).id
        # Comanda confirmada
        if self.state in ("sale", "done"):
            return self.env.ref(
                "b10_sales.comanda_email_template",
                raise_if_not_found=False,
            ).id
        # Caigui pel genèric
        return super()._get_default_mail_template_id()

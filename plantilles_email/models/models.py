from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Estableix la plantilla de correu electrònic per defecte de Comanda i Pressupost
    def _find_mail_template(self, force_confirmation_template=False):

        self.ensure_one()

        template_id = False
        template_ref = False

        if self.state in ["draft", "sent"]:  # Pressupost
            template_ref = "plantilles_email.pressupost_email_template"
        elif self.state in ["sale", "done"]:  # Comanda confirmada
            template_ref = "plantilles_email.comanda_email_template"

        if template_ref:
            template_id = self.env["ir.model.data"]._xmlid_to_res_id(
                template_ref, raise_if_not_found=False
            )

        return template_id


class AccountMove(models.Model):
    _inherit = "account.move"

    # Estableix la plantilla de correu electrònic per defecte de Factura
    def _get_mail_template(self):

        template_ref = "plantilles_email.factura_email_template"

        return template_ref

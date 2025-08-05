from odoo import models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _get_mail_template(self):
        self.ensure_one()
        if self.state == 'draft':
            tmpl = self.env.ref('b10_purchases.pressupost_email_template', raise_if_not_found=False)
            if tmpl:
                return tmpl.id

        return super(PurchaseOrder, self)._get_mail_template()


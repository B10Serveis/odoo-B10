from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Override to set B10 email templates depending on the state of the PO (RFQ vs purchase order).
    def action_rfq_send(self):
        """Open the standard Odoo composer with the matching B10 template."""
        self.ensure_one()
        action = super().action_rfq_send()
        template_xmlid = (
            "b10_purchases.pressupost_email_template"
            if self.state in ["draft", "sent"]
            else "b10_purchases.comanda_email_template"
        )
        template = self.env.ref(template_xmlid, raise_if_not_found=False)
        action["context"] = dict(
            action.get("context", {}),
            default_template_id=template.id if template else False,
        )
        return action

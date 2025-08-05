from odoo import _, models, fields

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_picking_send(self):
        self.ensure_one()

        # Estableix la plantilla de correu electrònic per defecte de Factura
        template_ref = "b10_stock_picking.entrega_email_template"
        template = self.env.ref(template_ref, raise_if_not_found=False)

        compose_form = self.env.ref(
            "mail.email_compose_message_wizard_form",
            False,
        )
        ctx = dict(
            default_model="stock.picking",
            default_res_ids=[self.id],
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
            user_id=self.env.user.id,
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

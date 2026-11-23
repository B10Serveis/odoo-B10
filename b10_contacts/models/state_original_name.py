from odoo import _, api, fields, models
from odoo.exceptions import AccessError


class StateOriginalName(models.Model):
    _inherit = "res.country.state"

    original_name = fields.Char("Original name", required=False)

    @api.model_create_multi
    def create(self, vals_list):
        # Només permetre crear a usuaris del grup Settings (administradors)
        if not self.env.user.has_group("base.group_system"):
            raise AccessError(_("Only administrators can create states."))
        return super().create(vals_list)

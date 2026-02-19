from odoo import models, fields, api, _
from odoo.exceptions import AccessError

class StateOriginalName(models.Model):
    _inherit = 'res.country.state'
    original_name = fields.Char("Original name", required=False)

    @api.model
    def create(self, vals):
        # Només permetre crear a usuaris del grup Settings (administradors)
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can create states."))
        return super(StateOriginalName, self).create(vals)
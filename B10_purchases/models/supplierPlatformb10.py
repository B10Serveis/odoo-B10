from odoo import models, fields, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Checkbox per activar la pestanya d'accés
    x_is_provider_access = fields.Boolean(
        string=_("Provider Access"),
        help=_("Enable the Access tab for supplier platform credentials")
    )
    # Camps per emmagatzemar les credencials
    # Camp encrypted per emmagatzemar la contrasenya
    x_provider_pwd_encrypted = fields.Encrypted(
        string="Encrypted Provider Password",
        readonly=True,
        copy=False,
    )

    x_provider_url = fields.Char(
        string=_("Platform URL"),
        help=_("URL of the supplier platform")
    )
    x_provider_user = fields.Char(
        string=_("Username"),
        help=_("User login for the supplier platform")
    )

    x_provider_pwd = fields.Char(
        string=_("Password"),
        widget='password',
        encrypt="x_provider_pwd_encrypted",
        help=_("Password for the supplier platform")
    )
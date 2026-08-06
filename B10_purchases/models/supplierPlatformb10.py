from odoo import fields, models, _


class B10ProviderCredential(models.Model):
    _name = "b10.provider.credential"
    _description = "Provider Website Credential"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    partner_id = fields.Many2one(
        "res.partner",
        string="Contact",
        required=True,
        ondelete="cascade",
        index=True,
    )
    name = fields.Char(
        string="Website",
        required=True,
        default=lambda self: _("Provider website"),
    )
    url = fields.Char(
        string="Platform URL",
        help="URL of the supplier platform",
    )
    user = fields.Char(
        string="Username",
        help="User login for the supplier platform",
    )
    password_encrypted = fields.Encrypted(
        string="Encrypted Provider Password",
        readonly=True,
        copy=False,
        groups="B10_purchases.group_b10_pwd_manager,B10_purchases.group_b10_pwd_reader",
    )
    password = fields.Char(
        string="Password",
        widget="password",
        encrypt="password_encrypted",
        help="Password for the supplier platform",
        groups="B10_purchases.group_b10_pwd_manager,B10_purchases.group_b10_pwd_reader",
    )


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Checkbox per activar la pestanya d'accés
    x_is_provider_access = fields.Boolean(
        string=_("Provider Access"),
        help=_("Enable the Access tab for supplier platform credentials"),
    )
    provider_credential_ids = fields.One2many(
        "b10.provider.credential",
        "partner_id",
        string="Provider Credentials",
    )

from odoo import SUPERUSER_ID, api
from odoo.addons.field_encryption.keyring import ensure_database_key


def migrate(cr, version):
    """Create the shared key file and persist its path before fields are used."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    ensure_database_key(env)

from odoo import SUPERUSER_ID, api

from odoo.addons.field_encryption.keyring import ensure_database_key


def migrate(cr, version):
    """Initialize the file keyring while retaining keys from prior versions."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    ensure_database_key(env)

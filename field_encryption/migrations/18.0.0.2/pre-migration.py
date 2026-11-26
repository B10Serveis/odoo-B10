from odoo import SUPERUSER_ID, api

from odoo.addons.field_encryption.keyring import ensure_database_key


def migrate(cr, version):
    """Initialize the keyring while retaining the key used by version 18.0.0.1."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    ensure_database_key(env)

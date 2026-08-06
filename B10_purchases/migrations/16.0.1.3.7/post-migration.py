import json
import logging

from odoo import SUPERUSER_ID, api

from odoo.addons.field_encryption.models.fields import fernet


_logger = logging.getLogger(__name__)


LEGACY_FIELDS = (
    "x_provider_url",
    "x_provider_user",
    "x_provider_pwd",
    "x_provider_pwd_encrypted",
)

LEGACY_COLUMNS = (
    "x_provider_url",
    "x_provider_user",
    "x_provider_pwd_encrypted",
)


def _column_exists(cr, table, column):
    cr.execute(
        """
        SELECT 1
          FROM information_schema.columns
         WHERE table_name = %s
           AND column_name = %s
        """,
        (table, column),
    )
    return bool(cr.fetchone())


def _get_legacy_password(encrypted_values):
    if not encrypted_values:
        return False
    values = json.loads(fernet.decrypt(bytes(encrypted_values)).decode())
    return values.get("x_provider_pwd")


def _migrate_credentials(env):
    cr = env.cr
    if not all(_column_exists(cr, "res_partner", field) for field in LEGACY_COLUMNS):
        return

    cr.execute(
        """
        SELECT id, x_provider_url, x_provider_user, x_provider_pwd_encrypted
          FROM res_partner
         WHERE x_provider_url IS NOT NULL
            OR x_provider_user IS NOT NULL
            OR x_provider_pwd_encrypted IS NOT NULL
        """
    )
    rows = cr.fetchall()
    credentials = env["b10.provider.credential"].sudo()
    partners = env["res.partner"].sudo()

    for partner_id, url, user, encrypted_password in rows:
        existing = credentials.search([
            ("partner_id", "=", partner_id),
            ("url", "=", url),
            ("user", "=", user),
        ], limit=1)
        if existing:
            continue

        credential = credentials.create({
            "partner_id": partner_id,
            "name": url or "Provider website",
            "url": url,
            "user": user,
        })
        password = _get_legacy_password(encrypted_password)
        if password:
            credential.write({"password": password})
        partners.browse(partner_id).write({"x_is_provider_access": True})

    _logger.info("Migrated %s legacy provider credential rows", len(rows))


def _drop_legacy_fields(env):
    cr = env.cr
    for field in LEGACY_COLUMNS:
        if _column_exists(cr, "res_partner", field):
            cr.execute('ALTER TABLE res_partner DROP COLUMN "%s"' % field)

    cr.execute(
        """
        SELECT id
          FROM ir_model_fields
         WHERE model IN ('res.partner', 'res.users')
           AND name IN %s
        """,
        (LEGACY_FIELDS,),
    )
    field_ids = [row[0] for row in cr.fetchall()]
    if not field_ids:
        return

    cr.execute(
        """
        DELETE FROM ir_model_data
         WHERE model = 'ir.model.fields'
           AND res_id IN %s
        """,
        (tuple(field_ids),),
    )
    cr.execute(
        """
        DELETE FROM ir_model_fields
         WHERE id IN %s
        """,
        (tuple(field_ids),),
    )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _migrate_credentials(env)
    _drop_legacy_fields(env)

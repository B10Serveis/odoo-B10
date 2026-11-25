from psycopg2 import sql

from odoo import SUPERUSER_ID, api
from odoo.tools import column_exists
from odoo.addons.field_encryption.keyring import get_fernet


def migrate(cr, version):
    """Rotate Encrypted columns to the active key without changing their values."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    fernet = get_fernet(env)
    seen_columns = set()

    for model in env.registry.models.values():
        if not model._auto or not model._table:
            continue

        for field in model._fields.values():
            if field.type != 'encrypted' or not field.store or not field.column_type:
                continue

            table = model._table
            column = field.name
            table_column = (table, column)
            if table_column in seen_columns or not column_exists(cr, table, column):
                continue
            seen_columns.add(table_column)

            last_id = 0
            while True:
                cr.execute(
                    sql.SQL(
                        "SELECT id, {} FROM {} WHERE id > %s AND {} IS NOT NULL "
                        "ORDER BY id LIMIT 1000"
                    ).format(
                        sql.Identifier(column),
                        sql.Identifier(table),
                        sql.Identifier(column),
                    ),
                    (last_id,),
                )
                rows = cr.fetchall()
                if not rows:
                    break

                for record_id, token in rows:
                    rotated = fernet.rotate(bytes(token))
                    cr.execute(
                        sql.SQL("UPDATE {} SET {} = %s WHERE id = %s").format(
                            sql.Identifier(table),
                            sql.Identifier(column),
                        ),
                        (rotated, record_id),
                    )
                last_id = rows[-1][0]

import logging

from odoo.tools import parse_version


_logger = logging.getLogger(__name__)

def migrate(cr, version):
    if not version:
        return

    if parse_version(version)[2:] >= parse_version('1.1'):
        # Aquestes versions ja empren el model de dades nou, res a fer
        return

    # Comprovar que el mòdul nou s’ha instal·lat
    cr.execute("""
        SELECT state FROM ir_module_module
        WHERE name = 'b10_helpdesk_contract'
    """)
    row = cr.fetchone()

    # llança un warning/log si no està 'installed'
    if not row or row[0] != 'installed':
        _logger.warning("El mòdul b10_helpdesk_contract no està instal·lat.")

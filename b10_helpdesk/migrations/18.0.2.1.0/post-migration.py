# b10_helpdesk/migrations/18.0.2.1.0/post-migration.py
import logging

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    if not version:
        return
    
    # Comprovar que el mòdul nou s’ha instal·lat
    cr.execute("""
        SELECT state FROM ir_module_module
        WHERE name = 'b10_helpdesk_contracts'
    """)
    row = cr.fetchone()

    # llança un warning/log si no està 'installed'
    if not row or row[0] != 'installed':
        _logger.warning("El mòdul b10_helpdesk_contracts no està instal·lat.")

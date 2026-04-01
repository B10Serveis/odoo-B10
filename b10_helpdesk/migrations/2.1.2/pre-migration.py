from odoo.tools import parse_version


def migrate(cr, version):
    # Només si s’està actualitzant el mòdul
    if not version:
        return

    # Comprovar si b10_helpdesk estava instal·lat
    cr.execute("""
        SELECT state FROM ir_module_module
        WHERE name = 'b10_helpdesk'
    """)
    row = cr.fetchone()
    if not row:
        return

    if parse_version(version)[2:] >= parse_version('1.1'):
        # Aquestes versions ja empren el model de dades nou, res a fer
        return

    # Assegurar que el nou mòdul existeix a la llista i marcar-lo per instal·lar
    cr.execute("""
        SELECT id, state FROM ir_module_module
        WHERE name = 'b10_helpdesk_contract'
    """)
    mod = cr.fetchone()
    if mod:  # TODO: fallar
        mod_id, state = mod
        if state in ('uninstalled', 'to remove'):
            cr.execute("""
                UPDATE ir_module_module
                   SET state='to install'
                 WHERE id=%s
            """, (mod_id,))


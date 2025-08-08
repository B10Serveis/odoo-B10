# b10_helpdesk/migrations/18.0.2.1.0/pre-migration.py
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

    # Assegurar que el nou mòdul existeix a la llista i marcar-lo per instal·lar
    cr.execute("""
        SELECT id, state FROM ir_module_module
        WHERE name = 'b10_helpdesk_contracts'
    """)
    mod = cr.fetchone()
    if mod:
        mod_id, state = mod
        if state in ('uninstalled', 'to remove'):
            cr.execute("""
                UPDATE ir_module_module
                   SET state='to install'
                 WHERE id=%s
            """, (mod_id,))


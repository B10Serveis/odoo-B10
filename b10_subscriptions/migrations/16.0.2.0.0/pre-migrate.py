from odoo.tools import parse_version


def migrate(cr, version):
    cr.execute("""
        SELECT state, latest_version FROM ir_module_module
        WHERE name = 'subscription_oca'
    """)
    submod = cr.fetchone()
    assert(submod)  # dependency
    submod_state, submod_latest_version = submod
    assert(submod_state in ['installed', 'to install'])  # dependency
    if parse_version(submod_latest_version)[2] < parse_version('2')[0]:
        raise RuntimeError("Module subscription_oca >= 2.0 is required for using"
                           " this version of this module.")

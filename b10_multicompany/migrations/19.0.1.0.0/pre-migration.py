"""Retire the compatibility module absorbed into b10_multicompany."""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE ir_module_module
           SET state = 'uninstalled'
         WHERE name = 'b10_multicompany_purchase_sale'
           AND state = 'installed'
        """
    )

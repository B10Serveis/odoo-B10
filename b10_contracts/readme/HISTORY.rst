18.0.1.0.0 (2025-08-06)
~~~~~~~~~~~~~~~~~~~~~~~
* [MIG] Adaptat a Odoo 18.  
* [ADD] Camp `contract_expiration` a `contract.contract`, computat de `date_end`.  
* [ADD] Camp `last_date_invoiced` a `contract.line`, computat des de `contract_id` si `line_recurrence=False`.  
* [ADD] Camp `is_canceled` visible i editable a les línies de contracte.  
* [ADD] Oculta botons de successor, aturar i renovar de la vista de línies.

18.0.1.1.0 (2026-04-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Elimina la dependència de ``b10_settings_hub``.

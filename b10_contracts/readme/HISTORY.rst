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

19.0.1.0.0 (2026-11-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Adaptat a Odoo 19 i a les vistes de ``contract`` 19.0.
* [FIX] Manté editables les dates de facturació i sincronitza les línies de recurrència global quan canvia la data del contracte.
* [IMP] La data de caducitat segueix directament la data de finalització.

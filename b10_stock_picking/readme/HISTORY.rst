18.0.1.0.0 (2025-08-06)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Migració a Odoo 18.  
* [ADD] `_get_mail_template` i `action_picking_send` per usar plantilla B10 en enviar per correu.  
* [ADD] Informe QWeb **report_entrega_batista** amb disseny B10 per a stock pickings.  
* [ADD] Plantilla HTML **entrega_email_template** amb report adjunt.

18.0.1.0.1 (2025-11-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Mostra la companyia del document en lloc de la de l'usuari en les plantilles de correu (per compatibilitat amb multiempresa). Les plantilles existents són reemplaçades en actualitzar.


18.0.1.1.0 (2026-04-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Elimina la dependència de ``b10_settings_hub``.

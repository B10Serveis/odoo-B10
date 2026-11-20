18.0.1.0.0 (2025-08-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Migració a Odoo 18.0

18.0.1.1.0 (2026-04-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Canvia la dependència de ``b10_settings_hub`` per ``b10_base``.

18.0.1.1.1 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Valida que els productes intercompany siguin compartits o pertanyin a
  l'empresa destinatària, independentment dels permisos dels usuaris de compres.

18.0.1.1.2 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Implementa el càlcul de la línia de compra intercompany vinculada a cada
  línia de venda, també quan l'usuari no té accés a l'empresa destinatària.

18.0.1.1.3 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Conserva la unitat de mesura de venda en crear les línies de compra
  intercompany, perquè la quantitat i el preu copiats mantinguin el seu significat.

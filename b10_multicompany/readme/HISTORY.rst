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

18.0.1.1.4 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Copia el descompte de venda a les línies de compra intercompany per
  conservar l'import net acordat, també si la tarifa del proveïdor és diferent.

18.0.1.1.5 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Evita generar compres duplicades per a vendes ja vinculades i conserva
  els enllaços d'origen de les vendes creades per l'OCA.
* [FIX] Propaga la cancel·lació després de confirmar-la, amb protecció contra
  reentrades entre les regles intercompany.
* [ADD] Compatibilitat opcional ``b10_multicompany_purchase_sale``, instal·lada
  automàticament quan també s'utilitza ``purchase_sale_inter_company`` de l'OCA.

18.0.1.1.6 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Corregeix els avisos de canvis a les vendes intercompany perquè no
  prometin sincronització automàtica entre les dues comandes.
* [IMP] Mostra també l'avís de preu en modificar el descompte i actualitza les
  traduccions i la documentació de configuració i sincronització.

19.0.1.0.0 (2026-11-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Migració a Odoo 19.0.
* [IMP] Integra la compatibilitat amb ``purchase_sale_inter_company``; el mòdul
  de l'OCA continua sent opcional.

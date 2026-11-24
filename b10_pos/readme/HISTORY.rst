19.0.1.0.0 (2026-11-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Adapta `get_product_info_pos` a `product.template` i a l'API d'Odoo 19.
* [FIX] Manté els identificadors de tarifes i l'estoc per ubicació del producte o variant seleccionat.

18.0.1.0.0 (2025-02-05)
~~~~~~~~~~~~~~~~~~~~~~~
* [MIG] Adaptat a Odoo 18.  
* [ADD] Modifica product.product perque el POS vegi les existencies per Ubicació enlloc de per Magatzem.
* [ADD] `get_product_info_pos`: mostra existències i previsions per ubicació interna.  
* [ADD] Desglossament d’impostos, tarifes, proveïdors i variants al POS.
* [ADD] Wizard **POS Closing Report** amb selecció de dates i configuració.  
* [ADD] QWeb PDF amb resum de sessions i detalls de pagaments.
* [FIX] Substituïda la classe Bootstrap `table-condensed` per `table-sm` en la plantilla `pos_closing_report.xml`.

18.0.1.1.0 (2026-04-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Elimina la dependència de ``b10_settings_hub``.

18.0.1.2.1 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Reutilitza la informació de producte estàndard d'Odoo 18 per aplicar els
  impostos de l'empresa del TPV i consultar els proveïdors amb dates de validesa.
* [FIX] Conserva els identificadors de tarifes i proveïdors que necessita el TPV.
* [FIX] Mostra les ubicacions internes de l'empresa del TPV i les compartides,
  amb el nom complet i l'identificador, prioritzant la ubicació d'origen del TPV.

18.0.1.3.0 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Trasllada l'informe de tancament de caixa de 17.0: selecciona les sessions
  tancades per data de tancament i zona horària i agrupa els pagaments per mètode.
* [IMP] Mostra els imports venuts i declarats, amb format monetari, dates locals,
  columnes alineades i missatges quan no hi ha sessions o pagaments.
* [FIX] Conserva el signe de les devolucions i incorpora les diferències de
  recompte dels pagaments bancaris separats, també si es van tancar en un altre idioma.
* [FIX] Permet imprimir als usuaris de TPV sense permisos comptables generals,
  limitant les consultes comptables a les sessions autoritzades.
* [FIX] Corregeix el model de l'acció d'impressió i elimina la vinculació antiga
  en actualitzar el mòdul. Incorpora traduccions al català i castellà i proves a 18.0.

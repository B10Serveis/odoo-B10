1. **Instal·lació**  

   - Des de **Apps**, instal·la **Batista10 – Stock**.  

2. **Enviar entrega per correu**  

   - Ves a **Inventory → Operations → Transfers** i obre una entrega (picking) de tipus **Delivery Order** o **Return**.  
   - Fes clic a **Send by Email**: s’obrirà el wizard de correu amb la plantilla carregada i el PDF adjunt.  

3. **Imprimir PDF de l’entrega**  

   - Des del mateix picking, fes **Print → Delivery Order (Batista10)**.

Correcció dels noms dels informes en instal·lacions existents
-----------------------------------------------------------

La versió 18.0.1.1.1 incorpora les traduccions corregides de l'informe d'entrega
en català i castellà, amb el prefix «B10 -». Si una instal·lació conserva
noms incorrectes, cal importar ``b10_stock/i18n/ca_ES.po`` i
``b10_stock/i18n/es.po`` per als idiomes corresponents, marcant
«Sobreescriure termes existents». Una actualització ordinària del mòdul pot
conservar les traduccions incorrectes ja desades a la base de dades.


Migració des d’Odoo 18
----------------------

El nom tècnic passa de ``b10_stock_picking`` a ``b10_stock``. En les
migracions d’OpenUpgrade d’Odoo 18 a 19, afegiu aquesta entrada a
``renamed_modules`` del fitxer ``openupgrade_scripts/apriori.py`` abans
d’executar la migració:

.. code-block:: python

   "b10_stock_picking": "b10_stock",

Això conserva els XMLID i l’estat d’instal·lació del mòdul amb el nom nou.

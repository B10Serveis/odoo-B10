B10: compatibilitat intercompany amb l'OCA
==========================================

Aquest mòdul s'instal·la automàticament quan estan instal·lats
``b10_multicompany`` i ``purchase_sale_inter_company``. No instal·la el mòdul
de l'OCA en entorns que només utilitzen B10.

* Una compra generada per una venda B10 no genera una altra venda amb l'OCA.
* Una venda generada per una compra OCA no genera una altra compra amb B10.
* Repetir la generació reutilitza la contrapartida existent, si no està cancel·lada.
* La cancel·lació dels documents vinculats no torna a entrar en el mateix circuit.

Els camps ``auto_purchase_order_id`` i ``auto_purchase_line_id`` mantenen els
enllaços existents. Identifiquen la compra vinculada, que pot ser l'origen d'una
venda OCA o la destinació d'una venda B10. Els camps ``auto_sale_order_id`` i
``auto_sale_line_id`` de les compres identifiquen les contrapartides generades
per B10 i permeten distingir els dos sentits.

Després de desplegar-lo, cal actualitzar la llista de mòduls i actualitzar
``b10_multicompany``. Si el mòdul de l'OCA ja està instal·lat, Odoo instal·la
també aquesta compatibilitat.

Llicència: AGPL-3.

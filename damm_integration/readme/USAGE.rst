Configuració
~~~~~~~~~~~~

Per a fer servir aquest mòdul cal acomplir els requeriments següents:

* A la vostra instància d'Odoo ha d'existir un *contacte* (partner) que represente la companyia S.A. Damm (el nom del contacte ha d'incloure la paraula «Damm»).
* La companyia actual (o la companyia de l'usuari actual) ha de tenir assignat un *codi de distribuïdor* de Damm.

Una volta instaŀlat aquest mòdul en la vostra instància d'Odoo, per a habilitar les seues funcions cal que seguiu aquests passos com a administrador:

1. Aneu a la pantalla de *Configuració/Configuració General*.
2. Sota la secció *Integració amb Damm*, marqueu la casella d'habilitació.
3. Deseu la configuració.
4. Sota la secció *Integració amb Damm*, entreu el vostre codi de distribuïdor i escolliu la companyia Damm.
5. Deseu la configuració de nou.

Açò permetrà a tots els usuaris emprar les funcions del mòdul.

Productes
~~~~~~~~~

La integració tindrà en compte com a productes de Damm aquells que tinguen entre els seus proveïdors la companyia que heu escollit com a Damm (vegeu la pestanya *Compra* en la pantalla del producte sota *Vendes/Productes/Productes*).

Clients
~~~~~~~

La integració tindrà en compte com a clients de Damm aquells tinguen factures ja validades que incloguen productes de Damm d'acord amb el punt anterior (vegeu la pestanya *Línies de factura* en la pantalla de la factura sota *Facturació/Clients/Factures*). Per a informes que cobreixen un rang de dates, només es tenen en compte les factures amb una data que cau dins del rang (vegeu el camp *Data de factura*).

Condicions comercials
~~~~~~~~~~~~~~~~~~~~~

La integració tindrà en compte com a condicions comercials de Damm aquelles tarifes de preus de clients de Damm que s'apliquen a productes de Damm, ambdós d'acord amb els punts anteriors (vegeu *Tarifa de venda* a la pestanya *Venda i compra* del client sota *Facturació/Clients/Factures*, i la pestanya *Regles de preus* de la tarifa sota *Vendes/Productes/Tarifes de preus*).

Informes
~~~~~~~~

El mòdul posa a la vostra disposició l'entrada de menú *Facturació/Informes/Damm/Nou informe per a Damm*, que vos permet generar i descarregar un fitxer d'informe per a enviar a Damm. El diàleg resultant vos permet crear i descarregar un informe del tipus desitjat per al rang de dades que indiqueu. Els tipus acceptats són:

* Vendes: fitxer amb format fix que inclou les línies de factures amb productes Damm (dades de *Línies de factura* de *Facturació/Clients/Factures*). Format Damm v6.
* Dades dels clients: fitxer amb format CSV que inclou informació dels clients de Damm (dades de *Facturació/Clients/Clients*). Format Damm v4.
* Condicions comercials: fitxer amb format CSV que inclou informació de les tarifes de venda dels clients de Damm (dades de *Vendes/Productes/Tarifes de preus*). Format Damm v4.

Tots els fitxers d'informe resultants empren la codificació UTF-8. Els fitxers CSV no inclouen capçalera i empren ``[`` com a caràcter separador de camp, sense caràcter delimitador de cadenes.

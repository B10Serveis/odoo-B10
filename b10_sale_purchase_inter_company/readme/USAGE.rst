Per a permetre que la creació d’una comanda de venda a la companyia A cree una comanda de compra associada a la companyia B, cal fer-ho a la configuració de la companyia B:

#. Escollir la companyia actual al menú superior d’Odoo (a la dreta, junt al nom d’usuari).
#. Anar al menú *Configuració > Configuració General*.
#. Sota la secció *Empreses*, apartat interempresa (*Inter Company*), sota *Venda / Compra* marcar l’opció primera, que habilita aquesta funció.
#. El selector següent vos permetrà escollir un usuari que apareixerà com a creador d’aquestes comandes de compra. Si no n’escolliu cap, s’emprarà l’usuari que ha creat la comanda de venda. En qualsevol cas, caldrà que l’usuari emprat tinga permisos de creació de compres en aquesta companyia.
#. Si marqueu l’opció de validació automàtica, quan valideu la comanda de venda a la companyia A amb la companyia B com a client, la comanda de compra es validarà automàticament a la companyia B.

Caldrà repetir aquestes passes per a cada companyia on vulgueu admetre la creació d’aquest tipus de comandes de compra.

**Important:** Habilitar per a una companyia l’opció de permetre la creació de comandes de compra associades a comandes de venda permetrà que açò es faça *des de qualsevol altra companyia* de l’Odoo (sempre que l’usuari creador tinga els permisos necessaris).

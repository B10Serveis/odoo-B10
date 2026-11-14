Per fer servir el mòdul:

#. Aneu a **Comptabilitat > Informes > MIS > Informes MIS** i creeu un informe.
#. Trieu la plantilla **Balance abreviado (PGCE 2008) - cuentas agrupadas por 3 dígitos**
   per al balanç o **Pérdidas y ganancias abreviado (PGCE 2008) - cuentas agrupadas
   por 3 dígitos** per al compte de pèrdues i guanys.
#. Les línies oficials de cada estat financer es mantenen; els grups de tres
   dígits apareixen sagnats sota la partida corresponent i els grups amb import
   zero s'amaguen.
#. La plantilla està basada en el quadre de comptes espanyol estàndard. Si feu
   servir prefixos personalitzats, comproveu que estiguin inclosos a la plantilla.

Balanç de sumes i saldos per partner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Després d'actualitzar ``B10_account``, accediu a **Comptabilitat > Informes >
Informes comptables OCA > Balanç de sumes i saldos per partner**.

Seleccioneu empresa, dates, diaris i comptes, i trieu **Veure**, **Exportar PDF**
o **Exportar XLSX**. Cada fila correspon a un compte i un partner, inclosos els
comptes d'actiu, passiu, ingressos i despeses. Els moviments sense partner es
mostren com a **Sense partner**. L'informe no filtra per partner.

Els saldos inicials segueixen les regles fiscals de l'informe OCA. Quan
correspon, els resultats d'exercicis anteriors s'incorporen al compte de
resultats pendents mantenint-ne el desglossament per partner. L'opció d'amagar
comptes a zero elimina les files sense saldo inicial, deure, haver ni saldo
final; si hi ha activitat, la fila es manté encara que el saldo final sigui
zero. La divisa segueix la configuració del compte.

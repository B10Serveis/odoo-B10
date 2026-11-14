Per fer servir els informes MIS de tres dígits:

#. Actualitzeu el mòdul ``B10_account`` amb les dependències
   ``l10n_es_mis_report`` i ``mis_builder`` disponibles.
#. Creeu un informe a MIS Builder i seleccioneu la plantilla
   ``Balance abreviado (PGCE 2008) - cuentas agrupadas por 3 dígitos``
   o ``Pérdidas y ganancias abreviado (PGCE 2008) - cuentas agrupadas por 3 dígitos``.
#. Configureu l'empresa i els períodes que voleu consultar.

Les plantilles agrupen els subcomptes pels tres primers dígits i amaguen
les línies de detall sense saldo. Els informes estàndard continuen disponibles.

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

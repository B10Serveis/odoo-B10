Per utilitzar aquest mòdul:

#. Vés a **Settings → B10** i, en el bloc Comptabilitat, activa **Group invoice lines by origin**.
#. Crea o obre una factura de venda; comprova que apareix el checkbox **Group Invoice Lines by Origin** sota el camp **Client/a**.
#. Desa la factura: si està marcat el checkbox, en generar el PDF la taula de línies sortirà agrupada per cada “Comanda de venda X”.
#. Des de la vista de factura, fes **(Accions) → Descarregar → Factura estàndard** per obtenir el PDF amb tots els elements (lots, IBAN, dades mercantils).

Informes MIS de 3 dígits
~~~~~~~~~~~~~~~~~~~~~~

Després d'actualitzar ``b10_account``, crea un informe MIS des de
**Comptabilitat → Informes → MIS Reporting** i selecciona una de les plantilles:

* **Balance abreviado (PGCE 2008) - cuentas agrupadas por 3 dígitos**.
* **Pérdidas y ganancias abreviado (PGCE 2008) - cuentas agrupadas por 3 dígitos**.

Configura la companyia i els períodes que vulguis comparar. Les línies de detall
agrupen els comptes pel prefix de 3 dígits del PGCE i s'oculten si el saldo és zero.

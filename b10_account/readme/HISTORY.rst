18.0.1.0.0 (2025-08-04)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Migració a V.18.
* [ADD] Assigna el 'Banc Receptor' automàticament si en una factura assignem una forma de pagament que te un diari bancari fix.

18.0.1.1.0 (2025-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] _sql_constraints_ a res.partner.bank per permetre usar un mateix Account Number a diversos partners però impedint duplicates dins del mateix partner.
* [ADD] Informe **Factura Estandard** amb:

  * Lots facturats (`_get_invoiced_lot_values`)
  * IBAN / SEPA a la capçalera
  * Dades mercantils al peu de pàgina
  * Agrupació de línies per ordre si s’activa

18.0.1.2.0 (2025-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Plantilles de correu per a factures:

  - Standard – Invoice Email Template (`factura_email_template`)
  - Standard – Pending Payment Email Template (`pending_payment_email_template`)

18.0.1.3.0 (2025-08-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Integració QR Veri*Factu al report: primera pàgina (dreta), textos i mides segons AEAT.
* [ADD] Dependència a l10n_es_edi_verifactu.
* [IMP] Capçalera en 3 columnes: logo + dades + QR.

18.0.1.4.0 (2025-08-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Invoice Analysis: afegida la mesura "Total Price with Taxes" a la vista pivot.

18.0.1.5.0 (2025-10-30)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Millor selecció i comprovació del banc destinatari de la factura en emprar un mode de pagament per transferència bancària (codi `bank_transfer`).

18.0.1.5.1 (2025-10-31)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Dependència mancant sobre `sale_stock`.
* [IMP] Separació de la documentació en components, correccions diverses.

18.0.1.5.2 (2025-11-10)
~~~~~~~~~~~~~~~~~~~~~~~

* [CHA] Canviem la dependència del mòdul l10n_es_edi_verifactu a l10n_es_verifactu_oca.

18.0.1.5.3 (2025-11-11)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No es comprova el banc destinatari de la factura en canviar a un mode de pagament que no és per transferència bancària.

18.0.1.6.3 (2025-11-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [CHA] Mida Header de Factura per QR Verifactu.

18.0.1.6.4 (2025-11-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Mostra la companyia del document en lloc de la de l'usuari en les plantilles de correu (per compatibilitat amb multiempresa). Les plantilles existents són reemplaçades en actualitzar.

18.0.1.6.5 (2025-11-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Ajustades mides de header a factura.

18.0.1.7.5 (2026-02-16)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Modifica el filtre de 'Compte a pagar' perque mostri tots els comptes de tipus 'liability%'.

18.0.1.7.6 (2026-02-19)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Correcció d'error al establir plantilla d'email de factura per defecte.

18.0.1.7.7 (2026-02-24)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Traducció de plantilles d'email de factura.

18.0.1.8.7 (2026-02-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Estableix document de Factura B10 com a document de factura per defecte.

18.0.1.8.8 (2026-02-27)
~~~~~~~~~~~~~~~~~~~~~~~

* [CHA] Afegit salt de linia entre telefon i email de company.

18.0.1.9.0 (2026-04-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Canvia la dependència de ``b10_settings_hub`` per ``b10_base``.

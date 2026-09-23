18.0.1.0.0 (2025-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Creat a V.18.
* [ADD] Afegit filtre “Caducats” per la vista de recerca de pressupostos.

18.0.1.1.0 (2025-08-05)
~~~~~~~~~~~~~~~~~~~~~~~

* [MIG] Migració a Odoo 18.  
* [ADD] Checkbox **Show product image** al formulari de comanda.  
* [ADD] Reports:  

  - **Pressupost Estandard** (`report/pressupost_batista.xml`)  
  - **Pressupost Estandard S/T** (`report/pressupost_st_batista.xml`)  
  - **Comanda Estandard** (`report/comanda_batista.xml`)  
  - **ProForma Estandard** (`report/proforma_batista.xml`)

18.0.1.2.0 (2025-08-05)
~~~~~~~~~~~~~~~~~~~~~~~
* [ADD] Email Templates i override de `_find_mail_template()`:  

  - **Standard - Quotation Email Template**  
  - **Standard - Sale Order Email Template**  
  - **Standard - Proforma Email Template**

18.0.1.3.0 (2025-08-08)
~~~~~~~~~~~~~~~~~~~~~~~
* [ADD] Classificacions de Marges.

18.0.1.4.0 (2025-10-13)
~~~~~~~~~~~~~~~~~~~~~~~
* [ADD] Selecció del diari de pagament al formulari de comanda, s'inclou IBAN de pagament a capçalera de pressupost, comanda i proforma.

18.0.1.4.1 (2025-10-14)
~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Establiment de diari de pagament durant creació de comanda de venda.

18.0.1.5.0 (2025-10-30)
~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Es comprova el diari de pagament en treure el mode de pagament de la comada de venda.
* [IMP] No es permet un diari de pagament buit si la comanda té un mode de pagament per transferència bancària amb comptes associats.
* [IMP] S'estableix a la factura creada des de la comanda de venda el mode i compte de pagament, si estan establerts a la comanda.

18.0.1.5.1 (2025-11-11)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No es comprova el diari de pagament de la comanda de venda en canviar a un mode de pagament que no és per transferència bancària.

18.0.1.6.1 (2025-11-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [CHA] Padding per separar contingut del header a tots els documents de venda.

18.0.1.6.2 (2025-11-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Mostra la companyia del document en lloc de la de l'usuari en les plantilles de correu (per compatibilitat amb multiempresa). Les plantilles existents són reemplaçades en actualitzar.

18.0.1.6.3 (2025-11-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [CHA] Ajustat padding per separar contingut del header a documents de venda.

18.0.1.6.4 (2025-11-28)
~~~~~~~~~~~~~~~~~~~~~~~

* [CHA] Ajustades mides header a documents de venda.

18.0.1.7.4 (2026-02-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Establir emails de venda per defecte.
* [FIX] Traducció de plantilles d'email de venda.

18.0.1.8.0 (2026-04-23)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Elimina la dependència de ``b10_settings_hub``.

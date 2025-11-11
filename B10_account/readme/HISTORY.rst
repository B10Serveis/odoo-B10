17.0.1.0.0 (2025-03-03)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Creat a V.17.
* [ADD] Assigna el 'Banc Receptor' automàticament si en una factura assignem una forma de pagament que te un diari bancari fix.

17.0.1.1.0 (2025-08-29)
~~~~~~~~~~~~~~~~~~~~~~~
* [IMP] Invoice Analysis: afegida la mesura "Total Price with Taxes" a la vista pivot reutilitzant el camp `price_total` d’Odoo 17.

17.0.1.2.0 (2025-10-30)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Millor selecció i comprovació del banc destinatari de la factura en emprar un mode de pagament per transferència bancària (codi `bank_transfer`).

17.0.1.2.1 (2025-10-31)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Dependència mancant sobre `sale_stock`.
* [IMP] Separació de la documentació en components, correccions diverses.

17.0.1.2.2 (2025-11-11)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] No es comprova el banc destinatari de la factura en canviar a un mode de pagament que no és per transferència bancària.


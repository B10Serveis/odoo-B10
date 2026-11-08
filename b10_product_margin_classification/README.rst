==========================================
B10 - Classificació del marge de productes
==========================================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: Llicència AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-B10Serveis%2Fodoo--B10-lightgray.png?logo=github
    :target: https://github.com/B10Serveis/odoo-B10/tree/17.0/b10_product_margin_classification
    :alt: B10Serveis/odoo-B10

|badge1| |badge2| |badge3|

Aquesta extensió reorganitza els camps de preu i classificació del marge al
formulari de plantilla de producte. Mostra el preu de venda, la informació
d'impostos, la classificació de marge i, quan cal, el preu teòric amb les
accions per ajustar el preu de venda.

**Taula de continguts**

.. contents::
   :local:

Dependències
============

Cal instal·lar el mòdul ``product_margin_classification``. Aquest mòdul depèn
de ``sale`` i aporta el càlcul del preu teòric, l'estat del marge i l'acció
per aplicar el preu teòric.

Ús
==

#. Obriu una plantilla de producte.
#. Seleccioneu-ne la classificació de marge.
#. El formulari mostrarà el preu teòric quan el marge sigui massa baix o massa
   alt, sempre que la plantilla tingui una sola variant.
#. Feu servir l'acció d'incrementar o reduir el preu per establir el preu de
   venda igual al preu teòric.

En plantilles amb més d'una variant, aquests camps de marge s'amaguen al
formulari de plantilla. La classificació i el preu s'han de gestionar des de
les variants.

El càlcul del mòdul base no admet impostos de venda que no siguin percentuals.

Registre de canvis
==================

17.0.1.1.1 (2026-11-08)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] S'afegeix la traducció catalana dels textos de la vista.
* [FIX] Es marca el mòdul com a extensió, no com a aplicació independent.
* [DOC] S'actualitzen les instruccions d'ús, les dependències i les metadades.

17.0.1.0.0 (2025-10-31)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Creació de la versió per a Odoo 17.
* [ADD] Reorganització dels camps de marge per fer-los més accessibles.

Seguiment d'errors
==================

Els errors es poden reportar a `GitHub Issues <https://github.com/B10Serveis/odoo-B10/issues>`_.

Crèdits
-------

Autors
------

* Batista10

Col·laboradors
--------------

* Joan Llimiñana i Sabaté <joan@batista10.cat> (https://www.batista10.cat)

El desenvolupament d'aquest mòdul ha estat finançat per Batista10.

================
Batista10 - PMS
================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-B10Serveis%2Fodoo--B10-lightgray.png?logo=github
    :target: https://github.com/B10Serveis/odoo-B10/tree/16.0/b10_pms
    :alt: B10Serveis/odoo-B10

|badge1| |badge2| |badge3|

Afegeix una plantilla de correu amb l'estil de Batista10 per confirmar reserves
d'hotel des del PMS. La plantilla està disponible en anglès, català, castellà i
francès, i selecciona automàticament l'idioma del client del foli.

Les dades de contacte, el lloc web i el logotip del correu provenen de la
propietat PMS del foli. Això permet que cada hotel tingui les seves pròpies dades
i imatge corporativa quan una mateixa empresa gestiona diverses propietats.

**Table of contents**

.. contents::
   :local:

Usage
=====

Per fer servir el mòdul:

#. Instal·leu el mòdul ``b10_pms``.
#. Configureu el correu electrònic, el telèfon, el lloc web i el logotip de cada
   propietat PMS.
#. Seleccioneu la plantilla «B10 - Hotel Reservation Confirmation» en enviar la
   confirmació d'un foli.

Changelog
=========

16.0.1.0.0 (2026-08-06)
~~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Creació de la plantilla multilingüe de confirmació de reserves.

16.0.1.0.1 (2026-09-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] El lloc web del peu del correu ara correspon a la propietat PMS del
  foli i no a l'empresa.
* [FIX] El logotip de la capçalera ara correspon a la propietat PMS del foli.

16.0.1.0.2 (2026-09-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] El logotip de l'hotel ara és accessible per als destinataris del
  correu que no tenen una sessió iniciada a Odoo.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/B10Serveis/odoo-B10/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/B10Serveis/odoo-B10/issues/new?body=module:%20b10_pms%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
========

Authors
~~~~~~~

* Batista10

Contributors
~~~~~~~~~~~~

* Joan Llimiñana i Sabaté <joan@batista10.cat> (https://www.batista10.cat)

Other credits
~~~~~~~~~~~~~

The development of this module has been financially supported by:

* Batista10

Maintainers
~~~~~~~~~~~

This module is part of the `B10Serveis/odoo-B10 <https://github.com/B10Serveis/odoo-B10/tree/16.0/b10_pms>`_ project on GitHub.

You are welcome to contribute.

===================
Batista10 - Website
===================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-B10Serveis%2Fodoo--B10-lightgray.png?logo=github
    :target: https://github.com/B10Serveis/odoo-B10/tree/17.0/b10_website
    :alt: B10Serveis/odoo-B10

|badge1| |badge2| |badge3|

Marca el camp «AEAT: Client anònim» dels contactes que no tenen NIF i no són
empreses, i el desmarca dels contactes amb NIF. Depèn de ``l10n_es_aeat``
i ``base_automation``.

**Table of contents**

.. contents::
   :local:

Usage
=====

En instal·lar el mòdul s'activa l'acció automatitzada «Marcar particulars
sense NIF com a anònims AEAT». S'executa immediatament en crear o actualitzar
el contacte, amb les condicions següents:

* Sense NIF (``vat``).
* No és una empresa (``is_company = False``).
* Encara no està marcat com a client anònim AEAT.

També s'activa l'acció automatitzada «Desmarcar clients anònims AEAT amb NIF»,
que desmarca ``aeat_anonymous_cash_customer`` quan el contacte té NIF i el
camp està marcat. S'aplica tant als particulars com a les empreses.

Les dues accions actuen en la creació i en les modificacions dels contactes.
Els contactes existents es comproven quan s'actualitzen; la instal·lació
no executa una revisió massiva.

Es poden consultar les accions des de Configuració > Tècnic > Automatització,
amb el mode desenvolupador.

Changelog
=========

17.0.1.0.0 (2026-10-15)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Creació del mòdul per marcar com a clients anònims AEAT els contactes
  sense NIF i que no són empreses.
* [ADD] Acció automatitzada que s'executa en crear i actualitzar contactes.
* [ADD] Acció automatitzada per desmarcar els clients anònims AEAT amb NIF,
  tant particulars com empreses, en crear i actualitzar contactes.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/B10Serveis/odoo-B10/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/B10Serveis/odoo-B10/issues/new?body=module:%20b10_website%0Aversion:%2017.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Batista10 (https://www.batista10.cat)

Contributors
~~~~~~~~~~~~

* Joan Llimiñana i Sabaté <joan@batista10.cat> (https://www.batista10.cat)

Other credits
~~~~~~~~~~~~~

El desenvolupament d'aquest mòdul ha estat impulsat i finançat per:

* Batista10 Serveis Informàtics (https://www.batista10.cat)

Maintainers
~~~~~~~~~~~

This module is maintained by Batista10.

This module is part of the `B10Serveis/odoo-B10 <https://github.com/B10Serveis/odoo-B10/tree/17.0/b10_website>`_ project on GitHub.

You are welcome to contribute.

Batista10 - Subscriptions
=========================

Extensió del mòdul OCA ``subscription_oca`` que permet afegir seccions i notes a
les línies d'una subscripció, conservar-ne l'ordre en les comandes i factures
recurrents i informar manualment la distribució analítica nativa d'Odoo a cada
línia de producte.

Usage
=====

#. Instal·lar ``subscription_oca`` i ``b10_subscriptions``.
#. A la pestanya de línies de la subscripció, afegir productes, seccions o notes.
#. Reordenar les línies amb el control d'arrossegament.
#. Si s'utilitza comptabilitat analítica, omplir la distribució de cada línia de
   producte. A Odoo 18, el mòdul OCA ``product_analytic`` permet configurar models
   de distribució analítica al producte o a la seva categoria. En afegir el
   producte, s'apliquen els models coincidents segons el producte, la categoria,
   el compte d'ingressos, el client i l'empresa. La distribució resultant es pot
   editar manualment. La distribució es conserva a les factures directes i a les
   factures generades a partir d'una comanda recurrent.
#. Seleccionar la forma de pagament de la subscripció; es trasllada a les
   comandes recurrents i a les factures, tant directes com generades des de la
   comanda. Si es deixa buida, els documents es generen sense forma de pagament.

La distribució de la línia de subscripció s'introdueix manualment. En generar una
comanda recurrent, aquest valor preval sobre qualsevol distribució calculada per
les regles automàtiques de la comanda.

Changelog
=========

18.0.1.0.0 (2026-11-20)
~~~~~~~~~~~~~~~~~~~~~~~

* Migració a Odoo 18.0 de les seccions, notes, ordre de les línies i forma de
  pagament.
* Adaptació de les vistes a ``list`` i reutilització del camp analític que ja
  incorpora ``subscription_oca``.
* Adaptació dels valors analítics inicials als models de distribució d'Odoo 18,
  en substitució dels camps de compte analític del producte i la categoria.

Batista10 - Subscriptions
=========================

Extensió del mòdul OCA ``subscription_oca`` que permet afegir seccions i notes a
les línies d'una subscripció, conservar-ne l'ordre en les comandes i factures
recurrents i informar manualment la distribució analítica nativa d'Odoo a cada
línia de producte. També permet seleccionar una forma de pagament pròpia per a
cada subscripció.

Usage
=====

#. Instal·lar ``subscription_oca`` i ``b10_subscriptions``.
#. A la pestanya de línies de la subscripció, afegir productes, seccions o notes.
#. Reordenar les línies amb el control d'arrossegament.
#. Seleccionar la forma de pagament a la subscripció. El valor triat es desa a
   la subscripció i es traspassa a les factures que es generen.
#. Si s'utilitza comptabilitat analítica, omplir la distribució de cada línia de
   producte. El mòdul OCA ``product_analytic`` defineix el compte analític
   d'ingressos del producte o de la seva categoria; en afegir el producte,
   s'emplena una distribució del 100% que després es pot editar manualment. La
   distribució es conserva a les factures directes i a les factures generades a
   partir d'una comanda recurrent.

La distribució de la línia de subscripció s'introdueix manualment. En generar una
comanda recurrent, aquest valor preval sobre qualsevol distribució calculada per
les regles automàtiques de la comanda.

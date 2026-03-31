1.0.0 (2022-01-09)
~~~~~~~~~~~~~~~~~~

* [ADD] Trasllat a V.12.
  (`#1 <https://gitlab.com/batista10/odoob10/-/issues/1>`_)

1.1.0 (2024-10-22)
~~~~~~~~~~~~~~~~~~

* [ADD] Migrat de 16.0.

1.2.0 (2025-03-05)
~~~~~~~~~~~~~~~~~~

* [ADD] Afegir disseny d'impressió de ticket.

1.3.0 (2026-03-24)
~~~~~~~~~~~~~~~~~~

* [IMP] Eliminats camps de còpia de correu. Feu servir els seguidors de l'objecte.

18.0.1.0.0 (2025-08-06)
~~~~~~~~~~~~~~~~~~~~~~~
* [MIG] Migració a Odoo 18.

18.0.1.1.0 (2025-08-08)
~~~~~~~~~~~~~~~~~~~~~~~
* [REM] Eliminat el camp `email_ccs` i la funcionalitat de còpies en CC als tiquets.
* [REM] Eliminat el camp `cc_email` al model `res.partner` (relació inversa de CC).
* [REM] Eliminats els camps `related_contract` i `current_time` per traslladar-los al nou mòdul `b10_helpdesk_contracts`, eliminant així la dependència amb el mòdul `contract`.
* [CLEAN] Neteja de vistes per eliminar referències als camps suprimits.

2.1.0 (2025-08-08)
~~~~~~~~~~~~~~~~~~

* [ADD] Scripts de migració (OpenUpgrade-style).

2.1.1 (2026-03-25)
~~~~~~~~~~~~~~~~~~

* [IMP] Codi sincronitzat amb altres versions d’Odoo.
* [FIX] Afegida dependència mancant de ``b10_contacts``.

2.1.2 (2026-04-01)
~~~~~~~~~~~~~~~~~~

* [FIX] Correccions a scripts de migració per a evitar perdre dades de contractes.

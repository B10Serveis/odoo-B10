.. image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: Llicència AGPL-3.0

================
Field Encryption
================

Fork de Batista10 del mòdul original ``field_encryption``, creat per Shah Alam
Sumon. Aquesta versió s’adapta i evoluciona de manera independent per cobrir els
requisits de les nostres instal·lacions d’Odoo.

El mòdul permet desar valors de camps xifrats a la base de dades. Els valors es
serialitzen abans de desar-los i es desxifren quan Odoo els llegeix. Diversos
camps es poden guardar dins d’un mateix camp ``Encrypted``.

Dependències
============

Cal instal·lar la biblioteca Python ``cryptography``:

.. code-block:: console

   pip install cryptography

Configuració
============

Aquest mòdul modifica ``odoo.fields`` i s’ha de carregar com a mòdul global del
servidor. Es pot fer amb l’opció:

.. code-block:: console

   --load="web,field_encryption"

O bé afegint aquesta línia a la configuració d’Odoo:

.. code-block:: ini

   server_wide_modules = web,field_encryption

Gestió de la clau
-----------------

Cada base de dades desa la ruta absoluta del fitxer de clau al paràmetre de
sistema ``field_encryption.key_path``. Per defecte, totes les bases de dades de
la mateixa instància d’Odoo apunten al fitxer compartit ``field_encryption.key``
del directori on hi ha el fitxer de configuració d’Odoo.

El mòdul crea el fitxer automàticament amb permisos només per al compte propietari.
Tots els processos d’Odoo han de poder llegir-lo. No l’esborris ni el regeneris:
les dades xifrades no es podran desxifrar sense la clau original.

En actualitzar una base de dades de la versió 18.0.0.1, el mòdul inicialitza el
fitxer i conserva com a claus de lectura la clau configurada amb
``encryption_key`` i la clau predeterminada de versions anteriors. No es
modifiquen les dades xifrades durant l’actualització; els valors existents
continuen desxifrant-se i els nous s’escriuen amb la clau activa del fitxer.

Si es restaura una base de dades en una instància amb un directori de configuració
diferent, cal actualitzar ``field_encryption.key_path`` perquè apunti a la ruta
absoluta nova, mantenint el mateix fitxer de clau. Inclou aquest fitxer a les
còpies de seguretat i conserva’l mentre hi hagi dades xifrades.

Ús i abast de la protecció
==========================

El xifrat protegeix les dades emmagatzemades davant d’algú que només tingui accés
a la base de dades o a una còpia seva. Odoo necessita llegir el fitxer de clau per
desxifrar els valors quan els usuaris autoritzats hi accedeixen des de l’aplicació.

Changelog
=========

18.0.0.2 (2026-11-26)
~~~~~~~~~~~~~~~~~~~~~

* Desa a cada base de dades la ruta del fitxer de clau compartit de la instància
  i el genera automàticament amb permisos restringits.
* Conserva les claus anteriors per poder llegir les dades xifrades existents,
  sense reescriure-les durant l’actualització.
* Rebutja valors en clar als camps ``Encrypted`` i corregeix l’opció de prefetch.

Crèdits
=======

Mòdul original: Shah Alam Sumon <sacsesumon@gmail.com>.

Fork i manteniment
==================

Batista10 manté aquest fork i n’evoluciona el codi de manera independent.

Autor: Marc Tormo i Bochaca <marc@batista10.cat>

Projecte original: https://github.com/ShahAlamSumon/field_encryption

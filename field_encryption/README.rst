.. image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png
   :target: https://www.gnu.org/licenses/agpl-3.0.html
   :alt: License: LGPL-v3

================
Field Encryption
================

With this module user can store encrypted field value in database.
So no one can see the value from database.
Multiple fields can be stored inside single Encrypted Field.
Just before storing to database, fields gets serialized, and encrypted.
On the other hand, after reading, encrypted field gets decrypted and
deserialized and values are available in each field in original form.

Requirements
============

    pip install cryptography

Configuration
=============
Because this module extends odoo.fields module, it needs to be loaded as server wide module.
This can be achieved by passing

    --load="web,field_encryption"

or by adding following line to the server config file:

    server_wide_modules = web,field_encryption

For compatibility with databases encrypted by earlier versions, you can keep
the previous key in the server configuration:

    encryption_key=<YOUR_KEY>

You can generate a Fernet key with the Python ``cryptography`` module:

    from cryptography.fernet import Fernet

    Fernet.generate_key().decode()

Key file
========

On installation or upgrade, the module creates a key file named
``field_encryption.key`` next to the active Odoo configuration file. Each
database stores its absolute path in the system parameter
``field_encryption.key_path``. Databases on the same Odoo instance therefore
share the same key file by default.

The file is created with owner-only permissions and contains the active key
plus previous keys needed to decrypt existing values. New values are encrypted
with the active key. Keep the file in your backups and do not delete or replace
it while encrypted values still exist. All Odoo processes must be able to read
it.

When upgrading a database that used ``encryption_key`` or the previous default
key, the module retains that key for reading existing values. It does not
rewrite encrypted data during the upgrade. If you restore a database on an
instance with a different configuration directory, update
``field_encryption.key_path`` to the absolute path of the original key file.

Usage
=====

Data encryption is using for protect sensitive data. If any outsiders get the access of
database or can get backup database then sensitive data can be protected by encryption.
Without key there is no way to access that field value.

Credits
=======

Shah Alam Sumon

Contributors
------------
* Shah Alam Sumon <sacsesumon@gmail.com>

Maintainer
----------

   :alt: Shah Alam Sumon
   :target: https://github.com/ShahAlamSumon/field_encryption

This module is maintained by Shah Alam Sumon.

Modifier
--------

   :alt: Shah Alam Sumon
   :target: https://github.com/ShahAlamSumon/field_encryption

This module is modified by Shah Alam Sumon.

To contribute to this module, please visit https://github.com/ShahAlamSumon/field_encryption

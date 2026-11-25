import json
from odoo import models, fields, _
from odoo.exceptions import ValidationError
from cryptography.fernet import InvalidToken
from ..keyring import get_fernet


def monkey_patch(cls):

    def decorate(func):
        name = func.__name__
        func.super = getattr(cls, name, None)
        setattr(cls, name, func)
        return func

    return decorate


fields.Field.__doc__ += """

        .. _field-encrypted:

        .. rubric:: Encrypted fields

        ...

        :param encrypt: the name of the field where encrypted the value of this
         field must be stored.
"""


@monkey_patch(fields.Field)
def _get_attrs(self, model, name):
    attrs = _get_attrs.super(self, model, name)
    if attrs.get('encrypt'):
        # by default, encrypt fields are not stored and not copied
        attrs['store'] = False
        attrs['copy'] = attrs.get('copy', False)
        attrs['compute'] = self._compute_encrypt
        if not attrs.get('readonly'):
            attrs['inverse'] = self._inverse_encrypt
    return attrs


@monkey_patch(fields.Field)
def _compute_encrypt(self, records):
    for record in records:
        values = record[self.encrypt] or {}
        record[self.name] = values.get(self.name)
    if self.relational:
        for record in records:
            record[self.name] = record[self.name].exists()


@monkey_patch(fields.Field)
def _inverse_encrypt(self, records):
    for record in records:
        values = record[self.encrypt] or {}
        value = self.convert_to_read(record[self.name], record)
        if value:
            if values.get(self.name) != value:
                values[self.name] = value
                record[self.encrypt] = values
        else:
            if self.name in values:
                values.pop(self.name)
                record[self.encrypt] = values


class Encrypted(fields.Field):
    """ Encrypted fields provide the storage for encrypt fields. """
    type = 'encrypted'
    column_type = ('bytea', 'bytea')

    prefetch = False

    def convert_to_column(self, value, record, values=None, validate=True):
        return self.convert_to_cache(value, record, validate=validate)

    def convert_to_cache(self, value, record, validate=True):
        fernet = get_fernet(record.env)
        if value is None or value is False:
            value = {}
        if isinstance(value, dict):
            return fernet.encrypt(json.dumps(value).encode())
        if isinstance(value, (bytes, bytearray, memoryview)):
            token = bytes(value)
            try:
                fernet.decrypt(token)
            except InvalidToken as error:
                raise ValidationError(_("Encrypted field accepts only encrypted data.")) from error
            return token
        raise ValidationError(_("Encrypted field value must be a dictionary."))

    def convert_to_record(self, value, record):
        if value:
            return json.loads(get_fernet(record.env).decrypt(bytes(value)).decode())


fields.Encrypted = Encrypted


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    ttype = fields.Selection(selection_add=[('encrypted', 'encrypted')], ondelete={'encrypted': 'cascade'})

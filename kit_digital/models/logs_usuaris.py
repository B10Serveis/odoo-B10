from odoo import models, fields


class logs_usuaris(models.Model):

    _name = 'kit_digital.logs_usuaris'

    ip_origin = fields.Char(string='IP de Origen') 
    user_name = fields.Char(string='Nombre Usuario')
    database_name = fields.Char(string='Base de datos')
    data_log = fields.Datetime(string='Fecha de acceso')
    status = fields.Char(string='Estado login')
    
    
    
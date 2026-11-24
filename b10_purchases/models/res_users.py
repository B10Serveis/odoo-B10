from odoo import api, models

# Estén el model 'res.users' per afegir lògica personalitzada per als grups d'usuaris.
class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)
        self._ensure_exclusive_groups(user)
        return user

    def write(self, vals):
        res = super(ResUsers, self).write(vals)
        # Odoo 19 uses ``group_ids`` for explicitly assigned groups.
        if 'group_ids' in vals:
            # Itera sobre cada usuari i s'assegura que els grups siguin exclusius per a cada usuari
            for u in self:
                self._ensure_exclusive_groups(u)
        return res

    # Mètode auxiliar per assegurar que un usuari no tingui els grups 'Manager' i 'Reader' alhora.
    def _ensure_exclusive_groups(self, user):
        GroupManager = self.env.ref('b10_purchases.group_b10_pwd_manager')
        GroupReader  = self.env.ref('b10_purchases.group_b10_pwd_reader')

        if GroupManager in user.all_group_ids and GroupReader in user.all_group_ids:
            user.sudo().write({
                'group_ids': [(3, GroupReader.id)]
            })

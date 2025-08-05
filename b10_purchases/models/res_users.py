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
        # Si s'està modificant el camp per als grups d'usuaris
        if 'groups_id' in vals:
            # Itera sobre cada usuari i s'assegura que els grups siguin exclusius per a cada usuari
            for u in self:
                self._ensure_exclusive_groups(u)
        return res

    # Mètode auxiliar per assegurar que un usuari no tingui els grups 'Manager' i 'Reader' alhora.
    def _ensure_exclusive_groups(self, user):
        GroupManager = self.env.ref('b10_purchases.group_b10_pwd_manager')
        GroupReader  = self.env.ref('b10_purchases.group_b10_pwd_reader')

        if GroupManager in user.groups_id and GroupReader in user.groups_id:
            user.sudo().write({
                'groups_id': [(3, GroupReader.id)]
            })

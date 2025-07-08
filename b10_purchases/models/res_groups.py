from odoo import api, models

# Estén el model 'res.groups' per afegir lògica personalitzada per a les modificacions de grups.
class ResGroups(models.Model):
    _inherit = 'res.groups'

    def write(self, vals):
        res = super().write(vals)
        GroupMgr  = self.env.ref('b10_purchases.group_provider_password_view')
        GroupRead = self.env.ref('b10_purchases.group_b10_pwd_reader')

        # Només ens interessa si modifiquen la many2many 'users'
        if 'users' in vals:
            # Extraiem els IDs d'usuaris que s'estan AFEGINT
            add_ids = []
            for cmd in vals['users']:
                if cmd[0] == 4:      # (4, user_id, 0)
                    add_ids.append(cmd[1])
                elif cmd[0] == 6:    # (6, 0, [ids])
                    add_ids += cmd[2]

            # Si estem escrivint sobre el grup Manager, traiem aquests usuaris del Reader
            if self.filtered(lambda g: g.id == GroupMgr.id) and add_ids:
                conflicte = GroupRead.users.filtered(lambda u: u.id in add_ids)
                if conflicte:
                    GroupRead.sudo().write({
                        'users': [(3, u.id) for u in conflicte]
                    })

            # Si estem escrivint sobre el grup Reader, traiem aquests usuaris del Manager
            if self.filtered(lambda g: g.id == GroupRead.id) and add_ids:
                conflicte = GroupMgr.users.filtered(lambda u: u.id in add_ids)
                if conflicte:
                    GroupMgr.sudo().write({
                        'users': [(3, u.id) for u in conflicte]
                    })

        return res
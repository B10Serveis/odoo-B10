from odoo import models


CATALAN_PROVINCES = frozenset({'B', 'GI', 'L', 'T'})


def delivery_partner(document):
    return document.partner_shipping_id or document.partner_id


def is_catalan_delivery(partner):
    state = partner.state_id if partner else False
    return bool(state and state.country_id.code == 'ES' and state.code in CATALAN_PROVINCES)


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _compute_amount(
        self, base_amount, price_unit, quantity=1.0, product=None,
        partner=None, fixed_multiplicator=1,
    ):
        self.ensure_one()
        group = self.env.ref('IBEE.tax_group_ibee', raise_if_not_found=False)
        if group and self.tax_group_id == group and not is_catalan_delivery(partner):
            return 0.0
        return super()._compute_amount(
            base_amount, price_unit, quantity, product, partner, fixed_multiplicator,
        )

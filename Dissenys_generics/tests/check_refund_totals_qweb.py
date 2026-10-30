"""Test the source refund summary through Odoo QWeb, with real currencies.

Uses accounting fixtures, not posted invoices. No database records are created.
Run with Odoo's Python and Odoo on PYTHONPATH:
    python check_refund_totals_qweb.py --config /path/odoo.conf --database test_db
"""
import argparse
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import unittest

from lxml import etree
import odoo
from odoo import api, SUPERUSER_ID


class TestRefundTotalsQWeb(unittest.TestCase):
    def render_summary(self, subtotals, groups, total, currency='base.USD'):
        # Deliberately different: company-currency amount must never be printed.
        invoice = SimpleNamespace(
            amount_total_signed=-999,
            amount_total_in_currency_signed=-total,
            currency_id=self.env.ref(currency),
            tax_totals={'subtotals': subtotals, 'groups_by_subtotal': groups},
        )
        source = etree.parse(str(
            Path(__file__).resolve().parents[1] / 'report/report_factura_batista.xml'
        ))
        table = source.xpath("//div[@id='total']/table")[0]
        fragment = etree.Element('table')
        for node in table:
            if (node.get('t-set') == 'tax_totals'
                    or node.get('t-as') == 'subtotal'
                    or node.tag == 'tr'):
                fragment.append(deepcopy(node))
        html = self.env['ir.qweb']._render(fragment, {'o': invoice})
        return etree.HTML(str(html))

    @staticmethod
    def group(name, amount, base):
        return {'tax_group_name': name, 'tax_group_amount': amount,
                'tax_group_base_amount': base}

    def amounts(self, html):
        return [Decimal(''.join(node.itertext()).replace('\ufeff', '').replace(',', ''))
                for node in html.xpath("//span[@class='oe_currency_value']")]

    def test_multiple_groups_do_not_drop_surcharge_or_duplicate_base(self):
        html = self.render_summary(
            [{'name': 'Untaxed', 'amount': 100}],
            {'Untaxed': [self.group('VAT 21%', 21, 100),
                         self.group('Surcharge 5.2%', 5.2, 100)]}, 126.2,
        )
        text = ''.join(html.itertext())
        self.assertIn('VAT 21%', text)
        self.assertIn('Surcharge 5.2%', text)
        self.assertEqual(self.amounts(html),
                         [Decimal('-100'), Decimal('-21'), Decimal('-5.2'), Decimal('-126.2')])

    def test_subtotal_is_not_the_first_tax_group_base(self):
        html = self.render_summary(
            [{'name': 'Untaxed', 'amount': 200}],
            {'Untaxed': [self.group('VAT 21%', 21, 100),
                         self.group('VAT 10%', 10, 100)]}, 231,
        )
        self.assertEqual(self.amounts(html),
                         [Decimal('-200'), Decimal('-21'), Decimal('-10'), Decimal('-231')])

    def test_total_uses_invoice_currency_for_foreign_and_local_currency(self):
        for currency, symbol in (('base.USD', '$'), ('base.EUR', '€')):
            with self.subTest(currency=currency):
                html = self.render_summary(
                    [{'name': 'Untaxed', 'amount': 120}], {'Untaxed': []}, 120, currency,
                )
                self.assertEqual(self.amounts(html), [Decimal('-120'), Decimal('-120')])
                self.assertIn(symbol, ''.join(html.itertext()))

    def test_all_subtotals_and_their_groups_are_rendered(self):
        html = self.render_summary(
            [{'name': 'First', 'amount': 100}, {'name': 'Second', 'amount': 121}],
            {'First': [self.group('VAT', 21, 100)],
             'Second': [self.group('Other tax', 5, 100)]}, 126,
        )
        self.assertEqual(self.amounts(html),
                         [Decimal('-100'), Decimal('-21'), Decimal('-121'),
                          Decimal('-5'), Decimal('-126')])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True)
    parser.add_argument('--database', required=True)
    args = parser.parse_args()
    odoo.tools.config.parse_config([
        '-c', args.config, '-d', args.database, '--no-http',
        '--logfile=/tmp/refund-totals-qweb-test.log',
    ])
    with odoo.registry(args.database).cursor() as cr:
        try:
            TestRefundTotalsQWeb.env = api.Environment(
                cr, SUPERUSER_ID, {'lang': 'en_US'}
            )
            result = unittest.TextTestRunner(verbosity=2).run(
                unittest.defaultTestLoader.loadTestsFromTestCase(TestRefundTotalsQWeb)
            )
        finally:
            cr.rollback()
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()

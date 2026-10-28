"""Render the real report table with Odoo records in a rolled-back transaction.

Run with Odoo on PYTHONPATH, using its Python environment:
    python check_delivery_qweb.py --config /path/odoo.conf --database test_database

No module update is required. All test records are rolled back.
"""
import argparse
from copy import deepcopy
from pathlib import Path

from lxml import etree
import odoo
from odoo import api, SUPERUSER_ID


def check_report(env):
    report = Path(__file__).resolve().parents[1] / 'report/report_entrega_batista.xml'
    table = etree.parse(str(report)).xpath("//table[@id='b10_linetable']")[0]
    unit = env.ref('uom.product_uom_unit')
    dozen = env.ref('uom.product_uom_dozen')
    product = env['product.product'].create({
        'name': 'Delivery quantity regression', 'type': 'product',
        'tracking': 'lot', 'uom_id': unit.id, 'uom_po_id': unit.id,
    })
    lots = env['stock.lot'].create([
        {'name': name, 'product_id': product.id, 'company_id': env.company.id}
        for name in ('QWEB-LOT-A', 'QWEB-LOT-B')
    ])
    source = env.ref('stock.stock_location_stock')
    destination = env.ref('stock.stock_location_customers')
    for direction, quantities, line_unit in (
        ('outgoing', (3, 7), unit),
        ('incoming', (3, 7), unit),
        ('outgoing', (1, 2), dozen),
        ('incoming', (1, 2), dozen),
    ):
        picking_type = env['stock.picking.type'].search([
            ('code', '=', direction), ('company_id', '=', env.company.id),
        ], limit=1)
        assert picking_type, 'Missing picking type: ' + direction
        src, dst = (source, destination) if direction == 'outgoing' else (destination, source)
        picking = env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': src.id, 'location_dest_id': dst.id,
        })
        move = env['stock.move'].create({
            'name': product.name, 'product_id': product.id,
            'product_uom': unit.id,
            'product_uom_qty': line_unit._compute_quantity(sum(quantities), unit),
            'picking_id': picking.id,
            'location_id': src.id, 'location_dest_id': dst.id,
        })
        env['stock.move.line'].create([
            {'move_id': move.id, 'picking_id': picking.id,
             'product_id': product.id, 'product_uom_id': line_unit.id,
             'quantity': qty, 'lot_id': lot.id,
             'location_id': src.id, 'location_dest_id': dst.id}
            for qty, lot in zip(quantities, lots)
        ])
        # Render the table taken directly from the current source, through Odoo QWeb.
        html = env['ir.qweb']._render(deepcopy(table), {'doc': picking})
        rows = etree.HTML(str(html)).xpath("//tbody/tr")
        assert len(rows) == 2, html
        actual = []
        for row, lot in zip(rows, lots):
            assert lot.name in ''.join(row.itertext()), html
            spans = row.xpath('./td[last()]/span')
            value = ''.join(spans[0].itertext()).strip().replace(',', '.')
            actual.append(float(value))
            assert ''.join(spans[1].itertext()).strip() == line_unit.display_name, html
        expected = [qty * (-1 if direction == 'incoming' else 1) for qty in quantities]
        assert actual == expected, (direction, actual, expected)
        print('PASS:', direction, line_unit.display_name, actual,
              '(move total:', move.quantity, unit.display_name + ')')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True)
    parser.add_argument('--database', required=True)
    args = parser.parse_args()
    odoo.tools.config.parse_config(['-c', args.config, '-d', args.database,
                                   '--no-http', '--logfile=/tmp/delivery-qweb-test.log'])
    registry = odoo.registry(args.database)
    with registry.cursor() as cr:
        try:
            check_report(api.Environment(cr, SUPERUSER_ID, {}))
        finally:
            cr.rollback()
    print('All QWeb checks passed; test records rolled back.')


if __name__ == '__main__':
    main()

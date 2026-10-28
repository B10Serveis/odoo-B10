"""Regression checks for the delivery report's quantity expressions.

Run without a database:
    python3 -m unittest discover -s Dissenys_generics/tests -v

These checks evaluate the expressions in the real template against split move
lines; they do not replace an Odoo HTML/PDF rendering test.
"""
from pathlib import Path
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET


class TestDeliveryQuantities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = ET.parse(
            Path(__file__).resolve().parents[1]
            / "report/report_entrega_batista.xml"
        )

    def quantity_cells(self, picking_type, lines):
        row = self.template.find(".//tr[@t-foreach='doc.move_line_ids']")
        self.assertIsNotNone(row)
        doc = SimpleNamespace(picking_type_code=picking_type)
        result = []
        for line in lines:
            context = {"doc": doc, "l": line}
            cells = [
                cell for cell in row.findall("td")
                if "t-if" in cell.attrib
                and eval(cell.attrib["t-if"], {"__builtins__": {}}, context)
            ]
            self.assertEqual(len(cells), 1)
            expressions = [
                span.attrib.get("t-field", span.attrib.get("t-esc"))
                for span in cells[0].findall("span")
            ]
            result.append(tuple(
                eval(expr, {"__builtins__": {}}, context)
                for expr in expressions
            ))
        return result

    def test_outgoing_split_lots(self):
        move = SimpleNamespace(quantity=10, product_uom="Units")
        lines = [
            SimpleNamespace(quantity=qty, product_uom_id="Units", move_id=move)
            for qty in (3, 7)
        ]
        self.assertEqual(
            self.quantity_cells("outgoing", lines), [(3, "Units"), (7, "Units")]
        )

    def test_incoming_split_lots_keep_negative_sign(self):
        move = SimpleNamespace(quantity=10, product_uom="Units")
        lines = [
            SimpleNamespace(quantity=qty, product_uom_id="Units", move_id=move)
            for qty in (3, 7)
        ]
        self.assertEqual(
            self.quantity_cells("incoming", lines), [(-3, "Units"), (-7, "Units")]
        )

    def test_quantity_uses_the_move_line_unit(self):
        move = SimpleNamespace(quantity=24, product_uom="Units")
        line = SimpleNamespace(quantity=2, product_uom_id="Dozens", move_id=move)
        for picking_type, expected in (("outgoing", 2), ("incoming", -2)):
            with self.subTest(picking_type=picking_type):
                self.assertEqual(
                    self.quantity_cells(picking_type, [line]), [(expected, "Dozens")]
                )

"""Exercise the actual create override with a fake ORM parent, without a DB.

Run: python3 -m unittest discover -s Dissenys_generics/tests -v
"""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class TestInvoiceGroupByOrigin(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / 'models/models.py'
        tree = ast.parse(source.read_text())
        model = next(node for node in tree.body
                     if isinstance(node, ast.ClassDef) and node.name == 'AccountMove')
        method = next(node for node in model.body
                      if isinstance(node, ast.FunctionDef) and node.name == 'create')
        method.decorator_list = []
        model.body = [method]
        model.bases = [ast.Name(id='Parent', ctx=ast.Load())]
        model.decorator_list = []

        class Parent:
            def create(self, values):
                return [SimpleNamespace(**vals) for vals in values]

        namespace = {'Parent': Parent}
        exec(compile(ast.fix_missing_locations(ast.Module(
            body=[model], type_ignores=[])), str(source), 'exec'), namespace)
        self.settings = Mock()
        self.settings.sudo.return_value = self.settings
        self.model = namespace['AccountMove']()
        self.model.env = {'res.config.settings': self.settings}

    def test_explicit_values_override_both_global_defaults(self):
        for default in (True, False):
            with self.subTest(default=default):
                self.settings.get_invoice_lines_by_origin.return_value = default
                records = self.model.create([
                    {'group_by_origin': True}, {'group_by_origin': False}, {},
                ])
                self.assertEqual([r.group_by_origin for r in records],
                                 [True, False, default])

    def test_all_explicit_does_not_read_global_setting(self):
        records = self.model.create([
            {'group_by_origin': False}, {'group_by_origin': True},
        ])
        self.assertEqual([r.group_by_origin for r in records], [False, True])
        self.settings.get_invoice_lines_by_origin.assert_not_called()

    def test_input_values_are_not_mutated(self):
        self.settings.get_invoice_lines_by_origin.return_value = True
        values = [{}, {'group_by_origin': False}]
        self.model.create(values)
        self.assertEqual(values, [{}, {'group_by_origin': False}])

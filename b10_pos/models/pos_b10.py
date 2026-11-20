from odoo import models


class ProductProductInherit(models.Model):
    _inherit = "product.product"

    def get_product_info_pos(self, price, quantity, pos_config_id):
        info = super().get_product_info_pos(price, quantity, pos_config_id)
        config = self.env["pos.config"].browse(pos_config_id)
        locations = self.env["stock.location"].search(
            [
                ("usage", "=", "internal"),
                ("company_id", "in", [False, config.company_id.id]),
            ],
            order="complete_name, id",
        )
        # The POS banner uses the first entry as its main stock quantity.
        source_location = config.picking_type_id.default_location_src_id
        locations = locations.sorted(lambda location: location != source_location)

        info["warehouses"] = []
        for location in locations:
            product = self.with_company(config.company_id).with_context(
                location=location.id, warehouse_id=False
            )
            info["warehouses"].append(
                {
                    "id": location.id,
                    "name": location.complete_name,
                    "available_quantity": product.qty_available,
                    "forecasted_quantity": product.virtual_available,
                    "uom": self.uom_name,
                }
            )
        return info

from odoo import models


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    def get_product_info_pos(
        self, price, quantity, pos_config_id, product_variant_id=False
    ):
        info = super().get_product_info_pos(
            price, quantity, pos_config_id, product_variant_id
        )
        config = self.env["pos.config"].browse(pos_config_id)
        product = self.env["product.product"].browse(product_variant_id) or self
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
            location_product = product.with_company(config.company_id).with_context(
                location=location.id, warehouse_id=False
            )
            info["warehouses"].append(
                {
                    "id": location.id,
                    "name": location.complete_name,
                    "available_quantity": location_product.qty_available,
                    "forecasted_quantity": location_product.virtual_available,
                    "uom": self.uom_name,
                }
            )

        pricelists = (
            config.available_pricelist_ids
            if config.use_pricelist
            else config.pricelist_id
        )
        for row, pricelist in zip(info["pricelists"], pricelists):
            row["id"] = pricelist.id
        return info

/*
    Copyright 2025 Batista10
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
*/

import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {patch} from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    async addProductToOrder(product) {
        await super.addProductToOrder(product);
        document.querySelector('.pos-topheader .fa-search +input[type="text"]').focus();
    },
});

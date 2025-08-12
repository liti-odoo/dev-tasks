import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    getProductName(product) {
        let result = super.getProductName(product)

        const productTmplValIds = product.attribute_line_ids
            .map((l) => l.product_template_value_ids)
            .flat();
        let productReference = productTmplValIds.length > 1 ? product.default_code : "";

        result = [result, productReference].join(" ")

        return result
    }
});
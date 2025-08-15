from odoo import api,models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    # @api.depends('product_id', 'product_uom', 'product_uom_qty')
    # def _compute_price_unit(self):
    #     price = super()._compute_price_unit()
    #     print("DEBUG DEBUG DEBUG")

    #     for line in self:
    #         test = line._get_sale_order_line_multiline_description_variants()
    #         print(test)

    #     self.price_unit = 0.222

    #     return price

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        amount = super()._compute_amount()
        print("DEBUG DEBUG DEBUG")

        for line in amount:
            line.price_tax = 10

        return amount
from odoo import api,fields,models,_
from odoo.exceptions import ValidationError

import re

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    code = fields.Char("Code", compute="_compute_product_code")
    custom_length = fields.Char(required=False)

    @api.depends('product_template_attribute_value_ids','product_template_attribute_value_ids.product_attribute_value_id.code','product_template_attribute_value_ids.attribute_id.name')
    def _compute_product_code(self):
            for line in self:
                keys = ["1", "2", "3", "4", "5"]
                codes = {key: "" for key in keys}
                
                for value in line.product_template_attribute_value_ids:
                    attribute_code = value.product_attribute_value_id.code
                    attribute_name = value.attribute_id.name
                    
                    if attribute_code:
                        if attribute_name in ['Family', 'Connector Capability', 'Fiber Type', 'Fiber Count']:
                            codes['1'] += attribute_code
                        elif attribute_name == 'Connector A':
                            codes['2'] += attribute_code
                        elif attribute_name == 'Connector B':
                            codes['3'] += attribute_code
                        elif attribute_name in ['Jacket Type', 'Cable Color', 'Construction']:
                            codes['4'] += attribute_code
                        elif attribute_name in ['Polarity', 'Breakout Length (in)']:
                            codes['5'] += attribute_code #Units
                        elif attribute_name in ['Length']:
                            self.custom_length = self.format_length(line.product_custom_attribute_value_ids.custom_value)
                            codes['6'] = self.custom_length + attribute_code

    
                line.code = "-".join(codes.values())
    
    def format_length(self, custom_length):
        number = float(custom_length)
        formatted_length = f"{number:05.1f}"

        return formatted_length

    # @api.depends('product_id', 'product_uom', 'product_uom_qty')
    # def _compute_price_unit(self):
    #     super()._compute_price_unit()
    #     for line in self:
    #         if line.product_id.name == 'Cable':
    #             for attribute in line.product_id.product_template_attribute_value_ids:
    #                 if attribute.attribute_id.name == 'Length':
    #                     price_extra = attribute.price_extra *  float(self.custom_length) - attribute.price_extra
    #                     # line.price_unit += price_extra
    #                     line.write({"price_unit": price_extra})


 






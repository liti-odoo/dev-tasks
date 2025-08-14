from odoo import api,models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.constrains('quantity', 'product_uom_qty')
    def _check_quantity(self):
        if self.quantity > self.product_uom_qty:
             raise ValidationError (
                    _("You can't receive more than the ordered quantity. Please, enter another quantity.")
                )
           
    

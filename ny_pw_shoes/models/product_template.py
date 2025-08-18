from odoo import api,fields,models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pair_per_case = fields.Integer('Pair per Case')
    price_per_pair = fields.Monetary('Price per Pair')
    list_price = fields.Float(
        'Sales Price',
        help="Price at which the product is sold to customers.",
        compute="_compute_list_price",
        store=True,
        readonly=False
    )

    @api.depends('pair_per_case', 'price_per_pair')
    def _compute_list_price(self):
        if self.pair_per_case and self.price_per_pair:
            self.list_price = self.pair_per_case * self.price_per_pair

from odoo import fields,models, _


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    code = fields.Char("Code", required=False)
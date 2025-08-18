{
    'name': "Product Price Customization",
    'summary': "Auto-calculated price based on custom inputs.",
    'version': '1.0',
    'author': "liti-odoo",
    'category': 'Purchase',
    "license": "OPL-1",
    'description': """
    task- NY P&W Shoes : Auto-calculated price
    """,
    'depends': [
        "product"
    ],
    'data': {
        "models/views/product_template_views.xml"
    }
}
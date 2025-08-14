{
    'name': "Purchase Validation Customization",
    'summary': "Added an error not allowing user to enter a quantity greater than demand.",
    'version': '1.0',
    'author': "liti-odoo",
    'category': 'Purchase',
    "license": "OPL-1",
    'description': """
    task- Materiales Castelar: Warehouse shouldn't receive more than ordered quantity
    """,
    'depends': [
        "stock"
    ],
}
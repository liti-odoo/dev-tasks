{
    'name': "Custom Product Variant",
    'summary': "Calculate part numbers and price based on a set of inputs.",
    'version': '1.0',
    'author': "liti-odoo",
    'category': 'Sale',
    "license": "OPL-1",
    'description': """
    FiberMountain : Product Configuration with Variants
    task-4926589
    """,
    'depends': [
        "sale",
    ],
    'data': [
        "models/views/product_attribute_views.xml",
        "models/views/sale_order_views.xml"
    ]
}
{
    "name": "Point of Sale Customization",
    "summary": "Adds a product reference to the POS product card",
    "category": "Customization",
    "version": "18.0.0.0.1",
    "author": "liti-odoo",
    "website": "https://github.com/liti-odoo/dev-tasks.git",
    "license": "OPL-1",
    'application':False,
    'data': [
        #SECURITY
    

        #DATA
        

        #VIEWS
       

    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'point_of_sale_2/static/src/**/*',
        ],
    },
    'demo': [
        
    ],
    'depends':[
        "point_of_sale",
        "product"
    ]
}
import pandas as pd
import xmlrpc.client

# api key: a20c2d972a8842473a1edf61a75b85d655d4b6f3
# odoo api
url = 'http://localhost:8069'
db = 'productquality'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none = True)


def setup():
    df = pd.read_excel("~/onboarding/dev-tasks/product_quality/Product_Import_Sample.xlsx")

    #Field mapping
    fields = {
        'Product Name': 'name',
        'Can be Sold':'sale_ok',
        'Can be Purchased':'purchase_ok',
        'Product Type':'type',
        'Product Category':'categ_name',
        'Internal Reference': 'default_code',
        'Barcode':'barcode',
        'Sales Price':'list_price',
        'Cost':'standard_price',
        'Internal Notes':'description',
        'Description for Customers':'description_sale',
        'seller_ids/name':'seller_name',
        'seller_ids/product_name': 'product_name',
        'seller_ids/product_code':'product_code',
        'seller_ids/delay':'delay',
        'seller_ids/min_qty':'min_qty',
        'seller_ids/price':'price',
        'Description for Vendors':'description_purchase',
        'Description for Delivery Orders':'description_pickingout',
        'Description for Receipts':'description_pickingin',
        'Weight':'weight',
        'Volume':'volume',
        'Customer Lead Time':'sale_delay'
    }
    #  'Manufacturing Lead Time':'produce_delay',
    df = clean_data(df,fields)

    # Create vendors and add partner_id
    partner_list = list(set(df['seller_name'].to_list()))
    create_vendor_or_categ('res.partner', partner_list)
    df = find_ids(df, 'res.partner',['name', 'in', partner_list], ['name'], False)

    # Create and update vendor info
    partner_ids_list = df['partner_id'].to_list()
    create_vendor_df, update_vendor_df, update_vendor_ids = find_ids(df, "product.supplierinfo", ['id', 'in', partner_ids_list], ['partner_id'], True)
    create_update_vendor_info(create_vendor_df,update_vendor_df,update_vendor_ids)

    # Create and add categ_id
    category_list = list(set(df['categ_name'].to_list()))
    create_vendor_or_categ('product.category', category_list)
    df = find_ids(df, 'product.category',['name', 'in', category_list], ['name'], False)

    # Create and update products
    product_default_code_list = df['default_code'].to_list()
    create_product_df, update_product_df, update_product_ids = find_ids(df, "product.template", ['default_code', 'in', product_default_code_list], ['default_code'], True)
    create_update_products(create_product_df,update_product_df,update_product_ids)

def clean_data(df,fields):
    df.drop(['External ID', 'Version', 'Company', 'Vendor Taxes', 'TaxCloud Category', 'Manufacturing Lead Time', 'Customer Taxes', 'Routes', 'Invoicing Policy', "Control Policy"], axis=1, inplace=True)
    df.rename(columns=fields, inplace=True)
    df.loc[df['type'] == 'Storable Product', 'type'] = 'consu'
    df[["min_qty", 'delay', 'weight', 'volume', 'sale_delay']] = df[['min_qty', 'delay', 'weight', 'volume', 'sale_delay']].fillna(0)

    return df

def find_ids(df, model, search_domain, search_fields, create):
    """
    Finds all ids that exist current database.

    Parameters:
        df (dataframe): Cleaned data that needs to be imported
        model (string): Model the fields that are being searched
        search_domain (list): Domain being searched
        search_fields (list): Fields being searched
        create (bool): True if finding existing ones, False when finding all after creating

    Returns:
        create_df (dataframe): IDs that do not exist in model
        update_df (dataframe): IDs that do exist in model
        update_ids (list): Existing fields used in search
        ids (list): Existing Odoo internal IDs
        

        df (dataframe): Modified df with new column

    """
    existing_ids = models.execute_kw(db, uid, password, model, 'search_read', [[search_domain]], {'fields': search_fields})
    if create:
        if model == 'product.template':
            ids = [x['id'] for x in existing_ids]
            existing_ids = [x['default_code'] for x in existing_ids]
            create_df = df[~df['default_code'].isin(existing_ids)]
            update_df = df[df['default_code'].isin(existing_ids)]
    
            if ids:
                return create_df, update_df, ids
            else:
                return create_df, False, False
        elif model == 'product.supplierinfo':
            ids = [x['id'] for x in existing_ids]
            existing_ids = [x['partner_id'] for x in existing_ids]
            create_df = df[~df['partner_id'].isin(existing_ids)]
            update_df = df[df['partner_id'].isin(existing_ids)]

            if ids:
                return create_df, update_df, ids
            else:
                return create_df, False, False
        
    else:
        if model == 'res.partner':
            partner_ids = [(x['id'], x['name']) for x in existing_ids]
            partner_ids = pd.DataFrame(partner_ids, columns=['partner_id', 'seller_name'])
            df = df.merge(partner_ids, left_on="seller_name", right_on="seller_name")
            return df
        elif model == 'product.category':
            category_ids = [(x['id'], x['name']) for x in existing_ids]
            category_ids = pd.DataFrame(category_ids, columns=['categ_id', 'categ_name'])
            df = df.merge(category_ids, left_on="categ_name", right_on="categ_name")
            return df
def create_vendor_or_categ(model, check_list): 
    existing = models.execute_kw(db, uid, password, model, 'search_read', [[['name', 'in', check_list]]], {'fields': ['name']})
    existing = [x['name'] for x in existing]
    create_list = [name for name in check_list if name not in existing]
    data={}

    if model == 'res.partner':
        for name in create_list:
            data = {
                'name': name,
                'is_company': True
            }
            models.execute_kw(db, uid, password, model, 'create', [data])
    elif model == 'product.category':
        for name in create_list:
            data = {
                'name': name,
            }
            models.execute_kw(db, uid, password, model, 'create', [data])

def create_update_vendor_info(create_df, update_df, ids):

    data={}

    for index, row in create_df.iterrows():
        data = {
            'partner_id': row.get('partner_id'),
            'product_code': row.get('product_code'),
            'delay':row.get('delay'),
            'min_qty':row.get('min_qty'),
            'price':row.get('price')
        }

    models.execute_kw(db, uid, password, 'product.supplierinfo', 'create', [data])
    
    if update_df:
        for index, row in update_df.iterrows():
            data = {
                'product_code': row.get('product_code'),
                'delay':row.get('delay'),
                'min_qty':row.get('min_qty'),
                'price':row.get('price')
            }

        models.execute_kw(db, uid, password, 'product.supplierinfo', 'write', [ids, data])
    
def create_update_products(create_df, update_df, ids):
    data={}
    print(create_df.head())
    for index, row in create_df.iterrows():
        data = {
                'name': row.get('name'),
                'sale_ok': row.get('sale_ok'),
                'purchase_ok': row.get('purchase_ok'),
                'type': row.get('type'),
                'categ_id': row.get('categ_id'),
                'default_code': row.get('default_code'),
                'barcode': row.get('barcode'),
                'list_price': row.get('list_price'),
                'standard_price': row.get('standard_price'),
                'description': row.get('description'),
                'description_sale': row.get('description_sale'),
                'description_purchase': row.get('description_purchase'),
                'description_pickingout': row.get('description_pickingout'),
                'description_pickingin': row.get('description_pickingin'),
                'weight': row.get('weight'),
                'volume': row.get('volume'),
                'sale_delay': row.get('sale_delay')
            }

        models.execute_kw(db, uid, password, 'product.template', 'create', [data])
    
    if not update_df.empty:
        print(update_df.head())
        for index, row in update_df.iterrows():
            data = {
                     'name': row.get('name'),
                    'sale_ok': row.get('sale_ok'),
                    'purchase_ok': row.get('purchase_ok'),
                    'type': row.get('type'),
                    'categ_id': row.get('categ_id'),
                    'default_code': row.get('default_code'),
                    'barcode': row.get('barcode'),
                    'list_price': row.get('list_price'),
                    'standard_price': row.get('standard_price'),
                    'description': row.get('description'),
                    'description_sale': row.get('description_sale'),
                    'description_purchase': row.get('description_purchase'),
                    'description_pickingout': row.get('description_pickingout'),
                    'description_pickingin': row.get('description_pickingin'),
                    'weight': row.get('weight'),
                    'volume': row.get('volume'),
                    'sale_delay': row.get('sale_delay')
                }
            models.execute_kw(db, uid, password, 'product.template', 'write', [ids, data])
    

if __name__ == "__main__":
    setup()

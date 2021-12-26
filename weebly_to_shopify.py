import argparse
import pandas as pd

def main(weebly_path='weebly_product.csv',shopify_path='shopify_products.csv'):

    weebly = pd.read_csv(weebly_path)
    shopify = pd.DataFrame(columns = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Standard Product Type',
       'Custom Product Type', 'Tags', 'Published', 'Option1 Name',
       'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name',
       'Option3 Value', 'Variant SKU', 'Variant Grams',
       'Variant Inventory Tracker', 'Variant Inventory Policy',
       'Variant Fulfillment Service', 'Variant Price',
       'Variant Compare At Price', 'Variant Requires Shipping',
       'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
       'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
       'Google Shopping / Google Product Category', 'Google Shopping / Gender',
       'Google Shopping / Age Group', 'Google Shopping / MPN',
       'Google Shopping / AdWords Grouping',
       'Google Shopping / AdWords Labels', 'Google Shopping / Condition',
       'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0',
       'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2',
       'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4',
       'Variant Image', 'Variant Weight Unit', 'Variant Tax Code',
       'Cost per item', 'Status'])

    in_df = []

    print('Converting ...')

    for i in range(len(weebly)):
        print(f'Product {i}/{len(weebly)}',end='\r')
            
        title = weebly.loc[i,'TITLE']
        handle = weebly.loc[i,'PRODUCT ID']
    
        # alternatively, use title to create a handle
        # handle = title.lower().replace(' ','_')

        beschrijving = weebly.loc[i,'DESCRIPTION']
        image = weebly.loc[i,'IMAGE']
        categories = weebly.loc[i,'CATEGORIES']
        
        # in shopify the first product variant has an image source and image_position 1, the rest have the image stored in image_variant
        if handle not in in_df:
            image_src = image
            image_variant = None
            image_position = 1
            status = 'active'

            # shopify requires an image, currently a way to deal with items without img is to skip them. Alternative solution might be better
            # if not image_src:
                # continue
            
        else:
            image_src = None
            image_variant = image
            image_position = None
            status = None
            
        in_df.append(handle)
            
        price = weebly.loc[i ,'PRICE']
        one_name = weebly.loc[i,'OPTION1 NAME']
        one_value = weebly.loc[i,'OPTION1 VALUE']
        two_name = weebly.loc[i,'OPTION2 NAME']
        two_value = weebly.loc[i,'OPTION2 VALUE']
        
        shopify.loc[i, ['Handle','Title','SEO Title','SEO Description','Body (HTML)','Image Src',
                            'Image Position','Variant Image','Variant Price','Tags','Option1 Name','Option1 Value',
                        'Option2 Name','Option2 Value','Status']] = (handle,title,
                            title,beschrijving,beschrijving,image_src,image_position,image_variant,
                            price,categories,one_name,one_value,two_name,two_value,status)

    shopify['Vendor'] = 'myVendor'
    shopify['Published'] = True
    shopify['Variant Inventory Tracker'] = 'shopify'
    shopify['Variant Inventory Policy'] = 'deny'
    shopify['Variant Fulfillment Service'] = 'manual'
    shopify['Variant Requires Shipping'] = True
    shopify['Variant Taxable'] = True
    shopify.to_csv(shopify_path, index=False)

    print('Complete!         ')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
	    description="please provide a folder path for weebly and destination shopify files"
	)

    parser.add_argument("--weebly", type=str, help="weebly .csv file")
    parser.add_argument("--shopify", type=str, help="shopify .csv destination file")

    arguments = parser.parse_args()
    main(arguments.weebly, arguments.shopify)
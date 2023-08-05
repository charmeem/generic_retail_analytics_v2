#--------------------------------------------------------------------------
#    This is config file where Business related hardcode values are defined
# I have mapped the actual names to the one prenented to the external Audience
#--------------------------------------------------------------------------

# category folder- later will be added in the gui
fold='csd'

# Customer defined dict of heirarchies 
# For example for Retail audit
heirarchies={'Size':'siz','Brand':'bra','Vendor':'ven','Flavor':'fla','Sub Brand':'sub','SKU':'sku','Product_code':'pro'}

# FACTS list for Retail Survey
# facts = ['Sales Volume','Sales Value','Purchase Volume', 'Stock Volume', 'Forward stock volume',
#          'Sales volume share', 'Sales Value Share','Purchase Volume Share', 'Stock Volume Share', 'Forward stock volume Share',
#          'Numeric Handling','Weighted Handling', 'OOS Numeric handling','OOS Weighted Handling','Handling in handlers','SISH',
#          'Sales Items','Retail selling Price packs','Retail selling Price units','OOS Cost','Stock Cover']

facts = {
         'vol_abs':'Sales Volume','val_abs':'Sales Value','vol_share':'Volume share','num_hand':'Numeric Distribution',
         'oos_hand':'O-O-S','purvol_abs':'P-V',
         'fwdstockvol_abs':'F-V','val_share':'V-S','purvol_share':'PV-S','stockvol_share':'SV-S',
         'fwdstockvol_share':'FSV-S','sales_items':'S-I','wt_hand':'W-D','stock_cover':'S-C', 
         'stockvol_abs':'S-V','ooswt':'O-W','sale_price':'S-P','hih':'H-H','sish':'SI-S','ooscost':'O-C','price_stick':'P-S'
         }


# Using hardcoded insted in this generic version
market_list = ['MKt segment3','MKt segment4','MKt segment5','MKt segment2','MKt segment6', 'MKt segment7', 'MKt segment9','Urbanity']     

# Selecting Hardcoded columns instead
heircols = {
            'Vendor':'Vendor', 'Brand':'Brand', 'Flavor':'Flavor', 'Size':'Size', 'Sub_brand':'Sub-brand', 'SKU':'SKU','Packing_type':'Packing Type',
            'shop_type':'Shop Type','Product_code':'Product Code'
            }






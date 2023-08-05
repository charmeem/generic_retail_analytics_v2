import pandas as pd


# Read log files to compare
dirpath = 'C:/my_drive/python/access_retail/qtopy/desktop/logs/'
fold1 = 'csd'
fold2 = 'csd_benchmark'
# heirarchy = [1,2,3,4,5,6,7,8,9,10,11,12]
facts = ['Sales_Volume','Sales_Value','Purchase_Volume','Stocks_Volume','Forward_Stocks_Volume','Volume_Share','Value_Share',\
         'Purchase_Volume_Share','Stock_Value_Share','Forward_stock_volume_share','Sales_Items','Numeric_handling',\
         'Weighted_handling','OOS_Numerical','OOS_weighted','Handling_in_handlers','SISH','COOS',\
         'Retail_SP_Per_pack','Retail_SP_Per_unit','Stocks_Cover_days']

heirarchy = [1]

# facts = ['Numeric_handling',\
#          'OOS_Numerical','OOS_weighted','Handling_in_handlers','SISH','COOS',\
#          ]

# facts = ['Sales_Volume','Numeric_handling','Weighted_handling','OOS_Numerical','OOS_weighted','Handling_in_handlers','SISH','COOS','Retail_SP_Per_pack','Retail_SP_Per_unit','Stocks_Cover_days']

for hr in heirarchy:
    try:
        for fact in facts:
            df1 = pd.read_csv(dirpath + fold1 + '/'+ str(hr) + '_'+ fact + '.csv')
            df2 = pd.read_csv(dirpath + fold2 + '/'+ str(hr) +  '_'+ fact + '.csv')
            result = df1.merge(df2,indicator=True,how='outer').loc[lambda v:v['_merge'] != 'both']
            result.to_csv(fact+'.csv')
            print(hr,fact)
            print(result)
            print("----------------------------------------------")
    except:
        continue

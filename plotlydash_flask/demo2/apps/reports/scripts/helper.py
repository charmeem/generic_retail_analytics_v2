#---------------------------------
# Different Helper Functions
#--------------------------------

import pandas as pd
import numpy as np
import sys
import csv

# dir_name = os.path.dirname(__file__)

# Function #1. Genererate contactenaded DB based on the Selected Months
def db_concater(months,cmon,nd,dirname,fold):
    dir_name=dirname

    # A routine to automaticaly detect the concetened file in the data directory
    # try:
    #     # linux command
    #     call('ls', shell=True)
    #
    #     print("cmon from helper:",cmon)
    #     concatfile = dir_name+'/data/month_'+ cmon +'.csv'
    #     print( "concetenated file:",concatfile)
    #     print( "concetenated file exist")
    # except:
    #     print("cfile does not exist")
    #     sys.exit()
    # Only run if requested
    if nd == 'true':
        try:
            db_all=(pd.read_csv(dir_name+ '/data/'+fold+'/month_'+str(i)+'.csv',engine='python' ) for i in months)
            concat_df = pd.concat(db_all,ignore_index=True)
            print('concat done')
            concat_df.to_csv(dir_name+'/data/'+fold+'/month_'+ cmon +'.csv')
            print('csv stored')
        except FileNotFoundError:
            print("Seems desired montly file does not exist in data folder, please check")
            sys.exit()

    # Read db
    try:
        print(dir_name,fold)
        db = pd.read_csv(dir_name+'/data/'+fold+'/month_'+ cmon +'.csv')
        #removed engine='python' as it caused store column name corrupted
        print('concatenated file read successfuly')
        return db

    except FileNotFoundError:
        print("Seems concetenated file does not exist in data folder, please check")
        sys.exit()



# Function #2. Creation of a new Table with selected Items and Rounded Volumes

def rounded_vol_db(db,d,kpi,hlist,market_array):

    #As shares are calculted from absolutes we have to rename share kpi to absolutes
    if (kpi == 'vol_share')|(kpi == 'saleleg')|(kpi == 'shareleg')|(kpi == 'sish')|(kpi == 'stock_cover'):
        kpi='vol_abs'
    elif kpi == 'val_share':
        kpi='val_abs'
    elif kpi == 'purvol_share':
        kpi='purvol_abs'
    elif kpi == 'stockvol_share':
        kpi='stockvol_abs'
    elif kpi == 'fwdstockvol_share':
        kpi='fwdstockvol_abs'
    elif (kpi == 'num_hand')|(kpi == 'oos_hand'):
        kpi='Num Proj Factor'
    elif (kpi == 'wt_hand')|(kpi == 'ooswt'):
        kpi='Volume'
    elif kpi == 'price_stick':
        kpi='sale_price'

    Client='generic'
    # Client='Tobacco'

    if Client=='Tobacco':
        indexf = [*hlist,'WAVE','Month', 'shop_code','PTC_REGION', 'PROVINCE', 'PTC_AREA_M','shop_type2',
    'shop_type', 'City', 'City_Code', 'RC_Total_Urban_Rural', 'RC_Top_10_Cities_ROU_Rural',
    'RC_Four_Metroe', 'RC_Trade_Channels', 'Product_code','Sale_new']

    elif Client=='generic':
        if 'Product_code' in hlist:
            indexf=[*hlist,'Month', 'shop_code', *market_array, 'Sale_new','Weights']
        else:
            indexf=[*hlist,'Month', 'shop_code', *market_array,'Product_code', 'Sale_new','Weights']
        
    new_db= pd.pivot_table(
                # db[(db['SKU']!=0)],
                db,
                index= indexf,
                values=[
                    kpi
                ],
                columns=[],
                aggfunc={
                    kpi:np.sum,
                },
            fill_value=0,
                )
    # Rounding only the KPI column
    new_db[kpi] = new_db[kpi].round(decimals=d)



    # print('rounded file prepared')

#     This step is now not needed and redundent- Exists here only for historical reason
#     # Storing new table as csv
#     new_db.to_csv(dir_name+'/data/rounded_vol_m_'+ cmon +'_d_{}.csv'.format(d))
#     print('rounded file stored')

#     # Reading from new_rounded_db
#     new_db = pd.read_csv(dir_name+'/data/rounded_vol_m_'+ cmon +'_d_{}.csv'.format(d))
#     print('rounded file read')

    return new_db

# Rounding for sish
def rounded_sish(db,d):

    new_db= pd.pivot_table(
                db[(db['SKU']!=0)],
                index=[
                    'WAVE',
                    'Month',
                    'shop_code',
                    'PTC_REGION',
                     'PROVINCE',
                    'PTC_AREA_M',
                    'shop_type2',
                    'shop_type',
                    'City',
                    'City_Code',
                    'RC_Total_Urban_Rural',
                    'RC_Top_10_Cities_ROU_Rural',
                    'RC_Four_Metroe',
                    'RC_Trade_Channels',
                    'SM',
                    'Product_code',
                    'Vendor',
                    'Brand',
                    'PS',
                    'SKU',
                    'Sale_new',

                 ],
                values=[
                  'SISH_Volume'
                ],
                columns=[],
                aggfunc={
                    'SISH_Volume':np.sum,
                },
            fill_value=0,
                )

    # Rounding only the KPI column
    new_db['SISH_Volume'] = new_db['SISH_Volume'].round(decimals=d)
    # new_db.to_csv('newdb.csv')

    return new_db

# Function #3. Filter out last row and concat it with the final table on the top
def add_tot_h2_nat_vol(py_h2,indexf):

    py_h2 = py_h2.loc[py_h2.index[-1]].to_frame().T
    py_h2['tmp']='Category'
    # py_h2.to_csv('pyh2.csv')

    # Fetch grand total row ( renamed as Category) as table
    h2_tot_row = py_h2[py_h2['tmp']=='Category']
    # h2_tot_row.to_csv('totrow.csv')
    # rename column SM to H2 to align with h2 table
    h2_tot_row = h2_tot_row.rename(columns={'tmp':'H2'})
    # drop useless columns to align with h2 table
    h2_tot_row=h2_tot_row.drop(indexf,axis=1)

    return h2_tot_row


#-------------------------------------------------------------------
#   Function #4.
#  Filter out last row and concat it with the final table on the top
#-------------------------------------------------------------------
def add_tot_h4_nat_vol(py_h4):

    # Give Category name to last cell of SM column
    # py_h4.loc[py_h4.index[-1],'SM']='Category'

    py_h4 = py_h4.loc[py_h4.index[-1]].to_frame().T
    py_h4['SM']='Category'


    # DRop indeces
#     py_h4 = py_h4.reset_index(drop=True)

    # Fetch grand total row ( renamed as Category) as table
    h4_tot_row = py_h4[py_h4['SM']=='Category']

    # rename column SM to H2 to align with h2 table
    h4_tot_row = h4_tot_row.rename(columns={'SM':'H4'})

    # drop useless columns to align with h2 table
    h4_tot_row=h4_tot_row.drop(['PS'],axis=1)

    return h4_tot_row

#------------------------------------
# Function to calculte:
# Projected volume ( Total store Volume)
# for weighted handling numerator calculations
#--------------------------------------
def proj_vol(db):
    # db.to_csv('dbprojvol.csv')
    proj_vol_t = pd.pivot_table(
            db,
            index=[
                'Month',
                'shop_code',
             ],
            values=[
                'Volume',
            ],
            aggfunc={
                'Volume':np.sum,
            },
            )
    
    proj_vol_t.rename(columns={'Volume':'proj_vol'},inplace=True)
    
    # Converting to data frame
    projo = proj_vol_t['proj_vol'].to_frame().reset_index()
    
    # Merging multilevel newly created proj_vol dataframe with the main db
    if 'proj_vol' in db.columns:
        db.drop(['proj_vol'], axis=1, inplace=True)
        db = db.merge(projo, on=['Month','shop_code'], how='left')
    else:
        db = db.merge(projo, on=['Month','shop_code'], how='left')
    
    return db




#----------------------------------------------------------
# Varaibles type transformation
# 1. Converting strings (received from js/html) to list
# 2. Coverting from string to decimal
#-----------------------------------------------------------
def convert(text):
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text

    
#-----------------------------------------------------]
# FUNCTION:
# - to create market_array from input 'mbd_file'
#
# - Also Varifying clean Market columns
#
# - Find and generate alert if there are 'NaN' or ' ' in any MBD columns
#   This is in order to handle program keyerror
#-----------------------------------------------------

def marrayf(dbm,fold):
    # Read CSV file into list
    a_csv_file = open('data/'+ fold + '/mbd_file.csv','r')
    list_reader= csv.reader(a_csv_file)
    # Read first row of the csv file
    list_from_csv = list(list_reader)[0]

    # Remove empty list elements if any
    # market_array = [string for string in list_from_csv if(string !=' ')]
    market_array = [el for el in list_from_csv if el.strip()]
    
    # Find and generate alert if there are 'NaN' or ' ' in any MBD columns
    for m in market_array[1:]:
        not_num = dbm[m].unique()
        if pd.isna(not_num).any() or ' ' in not_num:
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning('alert title', 'There are blanks in MBD: ' + m)
            print( " Program terminated, re-run after filling the blanks!")
            sys.exit()

    return market_array


# --------------------------------------------
# FUNCTION to Fetch scale fsctor for 
#volume and price from "scale_file.csv"
#----------------------------------------
def scalef(fold):
    # Read CSV file into list
    a_csv_file = open('data/'+ fold + '/scale_file.csv','r')
    list_reader= csv.reader(a_csv_file)
    # Read first row of the csv file
    list_from_csv = list(list_reader)
    # Extracting scale value from row
    s_volume = list_from_csv[0][0]
    s_value = list_from_csv[1][0]

    # Sometimes values entered as digits in csv appear as string
    # To handle this isdigit() and int() functions are used
    if s_volume.isdigit():
        s_volume = int(list_from_csv[0][0])
    if s_value.isdigit():
        s_value = int(list_from_csv[1][0])


    # Check if values are empty or are non integer then generate error
    if s_volume==' ':
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('alert title', 'Please enter valid volume scale factor in scale file')
        print('scale value is not entered')
        sys.exit()
    elif not isinstance(s_volume,int):
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('alert title', 'Please enter Volume scale factor as integer in scale file')
        print('scale value is not entered in integer form')
        sys.exit()
    elif s_value==' ':
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('alert title', 'Please enter valid Value scale factor in scale file')
        print('scale value is not entered')
        sys.exit()
    elif not isinstance(s_value,int):
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('alert title', 'Please enter Value scale factor as integer in scale file')
        print('scale value is not entered in integer form')
        sys.exit()

    return s_volume,s_value


#----------------------------------------------------
# FUNCTION to create a list, hlist, from a file heir_list.csv in data folder
# This function also gives the print order to the Heirarchy that fetched from above file
#------------------------------------------------------
def hlistf(fold,hr):
    # Read CSV file into list
    a_csv_file = open('data/'+ fold +'/heir_file.csv','r')
    list_reader= csv.reader(a_csv_file)
    # Read slected heirarchy 'heir' row of the csv file
    list_from_csv = list(list_reader)[hr]

    # remove first 2 elements , "client" and "Name" from the list
    nlist=list_from_csv[2:]

    # Strip all the emty or spaces elements from the list
    hlist = [el for el in nlist if el.strip()]

    # some columns like variant has 0 or blanks in it so
    # Convert Heirarchy level columns to 'nan'
    # This to avaoid index error

    # We donot need it for all the columns thats why i commente it Out
    # for i in range(len(hlist)):
    #     db[hlist[i]] = db[hlist[i]].apply(str)

    return hlist

#-----------------------------------------------
# FOR DASH application
# GENERIC FUNCTION TO EXTRACT Heirarchy level from
# hlistmain which is list of list 
#--------------------------------------------------
def hlistg(hr,hlistmain):
    # for s in hr:
    #     if s.isdigit():
    #         n=int(s)
    # print("nnnnnn1",n)        
    # print("lennnn",len(hlistmain))        
    # # for i,c in enumerate(hlistmain):
    # if n in range(len(hlistmain)+1):
    #     # print("iiiiii",i)
    #     print("nnnnn2",n)
    #     # if (n-1)==i:
    #     hlist=hlistmain[n-1]
    #     print("hlist9999",hlist)    
    # # if n<=len(hlistmain):
    # #     hr == 'combo'+str(n)
    # #     hlist=hlistmain[n-1]
    # #     print("hlist99",hlist)
    #     return hlist
    
    
    
    if hr == 'combo1':
        hlist = hlistmain[0]
    elif hr == 'combo2':
        hlist = hlistmain[1] 
    elif hr == 'combo3':
        hlist = hlistmain[2]
    elif hr == 'combo4':
        hlist = hlistmain[3]
    elif hr == 'combo5':
        hlist = hlistmain[4]   
    elif hr == 'combo6':
        hlist = hlistmain[5] 
    elif hr == 'combo7':
        hlist = hlistmain[6]
    elif hr == 'combo8':
        hlist = hlistmain[7]
    elif hr == 'combo9':
        hlist = hlistmain[8]
    elif hr == 'combo10':
        hlist = hlistmain[9] 
    
    return hlist    
        
    
    
    

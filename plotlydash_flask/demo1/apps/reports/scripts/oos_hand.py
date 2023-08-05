import pandas as pd
import numpy as np
import importlib
import oos_hand2 
importlib.reload(oos_hand2)
import level_format 
importlib.reload(level_format)

# Generic function for NUmeric Handling
def oos_handling(db,dbf,hlevel,gid,g):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    
    gid2='dummy'
    columnf = ['Month']

    #CAlling External Denominator Function
    # if geog == 'irmarket' or geog == 'tenkc' or geog == 'fourmetros' or geog == 'kpajk':
    #     deno = oos_hand2.denomin_cat(db,gid,gid2,dbf,columnf)
    # else:
    deno = oos_hand2.denomin(db,gid,gid2,dbf,columnf,g)
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)

    # NUMERATOR generating function based on input level
    indexf1= ['Month',gid,*hlevel,'shop_code']
    # if level=='SKU':
    #     hlevel=['SM','Vendor','Brand','PS','SKU']
    #     indexf1= ['Month',gid,'SM','Vendor','Brand','PS','SKU','shop_code']
    #
    # if level=='SM':
    #     hlevel = ['SM']
    #     indexf1= ['Month',gid,'SM','shop_code']
    #
    # if level=='Manu':
    #     hlevel=['SM','Vendor']
    #     indexf1= ['Month',gid,'SM','Vendor','shop_code']
    #
    # if level=='Brand':
    #     hlevel=['SM','Vendor','Brand']
    #     indexf1= ['Month',gid,'SM','Vendor','Brand','shop_code']
    #
    # if level=='PS':
    #     hlevel=['SM','Vendor','Brand','PS']
    #     indexf1= ['Month',gid,'SM','Vendor','Brand','PS','shop_code']

    indexf2 = [gid]

    # if geog == 'irmarket' or geog == 'tenkc' or geog == 'fourmetros' or geog == 'kpajk':
    #     columnf = ['Month',*hlevel]
    #     numero = oos_hand2.numerator_cat(db,dbf,indexf1,columnf)
    # else:
    columnf = [*hlevel,'Month']
    numero = oos_hand2.numerator(db,dbf,indexf1,indexf2,columnf,hlevel)
    
    #Converting dataframe to series to avoid error while dividing below
    # GENERTING ERROR FOR THE EMPTY Dataframe in NUERO ABOVE HENCE I AM REMOVING THAT CODE!!
    # numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    return hkpi

# Function For calculating National Geoghraphy
def oos_handling_nat(db,dbf,hlevel):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table

    columnf = ['Month']
#         dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #CAlling External Denominator Function
    deno = oos_hand2.denomin_nat(db,columnf)

    # Calling External NUMERATOR handling function for EACH level
    indexf1= ['Month',*hlevel,'shop_code']
    # if level=='SKU':
    #     hlevel=['SM','Vendor','Brand','PS','SKU']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf1= ['Month','SM','Vendor','Brand','PS','SKU','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand','PS','SKU']
    #
    # if level=='SM':
    #     hlevel=['SM']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf1= ['Month','SM','shop_code']
    #     # indexf2 = ['SM']
    #
    # if level=='Manu':
    #     hlevel=['SM','Vendor']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf1= ['Month','SM','Vendor','shop_code']
    #     # indexf2 = ['SM','Vendor']
    #
    # if level=='Brand':
    #     hlevel=['SM','Vendor','Brand']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf1= ['Month','SM','Vendor','Brand','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand']
    #
    # if level=='PS':
    #     hlevel=['SM','Vendor','Brand','PS']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf1= ['Month','SM','Vendor','Brand','PS','shop_code']

    columnf = [*hlevel,'Month']
    # print("hleveeel",hlevel)
    # if 'SKU' in hlevel:
    #     dbf = dbf&(db.CS_Stock == 0)
    #     #Numerator function call
    #     smch1 = pd.pivot_table(
    #                 db[dbf],
    #                 index=indexf1,
    #                 values=['Num Proj Factor'],
    #                 aggfunc={'Num Proj Factor':np.max},
    #                 )
    #     # smch1.to_csv('smch1.csv')
    #     # Redefining dbf to get stores with no CS_Stock
    #
    #     numero = pd.pivot_table(
    #                 smch1,
    #                 values=['Num Proj Factor'],
    #                 columns=columnf,
    #                     aggfunc={'Num Proj Factor':np.sum},
    #                 )
    #     print(hlevel)
    #     # numero.to_csv('numero.csv')
    #     #Converting dataframe to series to avoid error while dividing below
    #     numero=numero.iloc[0]
    #     # numero.to_csv('numero2.csv')
    # else:
    #Numerator function call
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['Num Proj Factor','CS_Stock'],
                aggfunc={'Num Proj Factor':np.max,'CS_Stock':np.sum},
                )
    # smch1.to_csv('smch2.csv')
    # Redefining dbf to get stores with no CS_Stock
    dbf = (smch1.CS_Stock == 0)
    numero = pd.pivot_table(
                smch1[dbf],
                values=['Num Proj Factor'],
                columns=columnf,
                    aggfunc={'Num Proj Factor':np.sum},
                )
    # numero.to_csv('numero3.csv')
    # print(hlevel)
    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]
    # numero.to_csv("numero4.csv")
    # Handling
    hkpi = numero/deno*100
    # hkpi.to_csv('hkpi.csv')
    return hkpi


# Function for Urbanity numeric handling
def uoos_handling(db,gid,geog,geog2,dbf,level):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = oos_hand2.denomin(db,gid,gid2,dbf,columnf)
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)


    # Calling External NUMERATOR handling function for EACH level
    if level=='SKU':
        hlevel=['SM','Vendor','Brand','PS','SKU']
        indexf1= ['Month',gid,gid2,'SM','Vendor','Brand','PS','SKU','shop_code']

    if level=='SM':
        hlevel=['SM']
        indexf1= ['Month',gid,gid2,'SM','shop_code']

    if level=='Manu':
        hlevel=['SM','Vendor']
        indexf1= ['Month',gid,gid2,'SM','Vendor','shop_code']

    if level=='Brand':
        hlevel=['SM','Vendor','Brand']
        indexf1= ['Month',gid,gid2,'SM','Vendor','Brand','shop_code']

    if level=='PS':
        hlevel=['SM','Vendor','Brand','PS']
        indexf1= ['Month',gid,gid2,'SM','Vendor','Brand','PS','shop_code']

    indexf2 = [gid2]

    # This is for the table formating as per quantum
    if geog=='kpajk' or geog=='shopper' or geog=='trade':
        columnf = ['Month',*hlevel]
    else:
        columnf = [*hlevel,'Month']

    #Numerator function call
    numero = oos_hand2.numerator(db,dbf,indexf1,indexf2,columnf,level)
    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    return hkpi

def uoos_handling_nat(db,gid,geog,geog2,dbf,level):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = oos_hand2.denomin(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    if level=='SKU':
        hlevel=['SM','Vendor','Brand','PS','SKU']
        indexf1= ['Month',gid2,'SM','Vendor','Brand','PS','SKU','shop_code']

    if level=='SM':
        hlevel=['SM']
        indexf1= ['Month',gid2,'SM','shop_code']

    if level=='Manu':
        indexf1= ['Month',gid2,'SM','Vendor','shop_code']
        hlevel = ['SM','Vendor']

    if level=='Brand':
        indexf1= ['Month',gid2,'SM','Vendor','Brand','shop_code']
        hlevel = ['SM','Vendor','Brand']

    if level=='PS':
        indexf1= ['Month',gid2,'SM','Vendor','Brand','PS','shop_code']
        hlevel = ['SM','Vendor','Brand','PS']

    columnf = [*hlevel,'Month']

    #Numerator function call
    if level=='SKU':
        dbf = dbf&(db.CS_Stock == 0)
        smch1 = pd.pivot_table(
                    db[dbf],
                    index=indexf1,
                    values=['Num Proj Factor'],
                    aggfunc={'Num Proj Factor':np.max},
                    )

        numero = pd.pivot_table(
                    smch1,
                    index=[gid2],
                    values=['Num Proj Factor'],
                    columns=columnf,
                        aggfunc={'Num Proj Factor':np.sum},
                    )
    else:
        smch1 = pd.pivot_table(
                    db[dbf],
                    index=indexf1,
                    values=['Num Proj Factor','CS_Stock'],
                    aggfunc={'Num Proj Factor':np.max,'CS_Stock':np.sum},
                    )
        # Redefining dbf to get stores with no CS_Stock
        dbf = (smch1.CS_Stock == 0)
        numero = pd.pivot_table(
                    smch1[dbf],
                    index=[gid2],
                    values=['Num Proj Factor'],
                    columns=columnf,
                        aggfunc={'Num Proj Factor':np.sum},
                    )

    # Solving division error after anaconda upgrade
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)
    # convert nemerator from df to series
    numero = numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    return hkpi

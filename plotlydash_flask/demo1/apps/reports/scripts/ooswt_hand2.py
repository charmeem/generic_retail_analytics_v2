import pandas as pd
import numpy as np
import importlib


# General Funcion to Calculate Numeric Handliing KPI
# Function to calculate Denominator
def denomin(db,gid,gid2,dbf,columnf):

    # Check if this is urbanity
    if gid2=='RC_Total_Urban_Rural':
        indexf = [gid2]

    else:
        indexf = [gid]
    deno = pd.pivot_table(
                    db[dbf],
                    index=indexf,
                    values=['Volume'],
                    columns=columnf,
                    aggfunc={
                        'Volume':np.sum,
                        },
                    dropna=False
                    )

    return deno

def denomin_cat(db,gid,gid2,dbf,columnf):
    deno = pd.pivot_table(
                    db[dbf],
                    values=['Volume'],
                    columns=columnf,
                    aggfunc={
                        'Volume':np.sum,
                        },
                    dropna=False
                    )
    return deno

# Special deno function for National Geogrphy id
def denomin_nat(db,columnf):

    deno = pd.pivot_table(
                    db,
                    values=['Volume'],
                    columns=columnf,
                    aggfunc={
                        'Volume':np.sum,
                        },
                    dropna=False
                    )

    #As all columns has same value we take single value to be used as denominator below
    # deno=sm_s_pf.iloc[0,0]
    return deno

# Function to calculate Numerator for numeric handling general
def numerator(db,dbf,indexf1,indexf2,columnf,hlevel):
    # if 'SKU' in hlevel:
    #     dbf = dbf&(db.CS_Stock == 0)
    #     smch1 = pd.pivot_table(
    #                 db[dbf],
    #                 index=indexf1,
    #                 values=['proj_vol'],
    #                 aggfunc={'proj_vol':np.max},
    #                 )
    #     numero = pd.pivot_table(
    #                 smch1,
    #                 index=indexf2,
    #                 values=['proj_vol'],
    #                 columns=columnf,
    #                     aggfunc={'proj_vol':np.sum},
    #                 )
    # else:
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['proj_vol','CS_Stock'],
                aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                )

    # Redefining dbf to get stores with no CS_Stock
    dbf = (smch1.CS_Stock == 0)
    numero = pd.pivot_table(
                smch1[dbf],
                index=indexf2,
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )

    return numero

# Function to calculate Numerator for Category handling
def numerator_cat(db,dbf,indexf,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['proj_vol','CS_Stock'],
                aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                )

    # Redefining dbf to get stores with no CS_Stock
    dbf = (smch1.CS_Stock == 0)
    numero = pd.pivot_table(
                smch1[dbf],
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )
    # renaming 'proj_vol' back to 'Volume' for proper division
    numero.rename(index={'proj_vol':'Volume'},inplace=True)

    return numero

### Functions for Numeric Handling

### Functions for Category Handling
# Generic function for Ctegory Handling
def cat_handling(db,gid,geog,dbf):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    columnf = ['Month']
    #CAlling External Denominator Function
    deno = denomin_cat(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month',gid,'shop_code']
    columnf = ['Month']

    #Numerator function call
    numero = numerator_cat(db,dbf,indexf,columnf)

    # Handling
    hkpi = numero/deno*100
    return hkpi
    # Format the Indexes to match with the SKU Base
    # hkpi = format(hkpi)

# Function For calculating National Geoghraphy
def cat_handling_nat(db):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table

    columnf = ['Month']
#         dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #CAlling External Denominator Function
    deno = denomin_nat(db,columnf)

    # Calling External NUMERATOR handling function for EACH level
    dbf = (db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month','shop_code']
    columnf = ['Month']

    #Numerator function call
    numero = numerator_cat(db,dbf,indexf,columnf)

    # Handling
    hkpi = numero/deno*100
    # hkpi.to_csv('hji.csv')
    return hkpi

    # Format the Indexes to match with the SKU Base
    # hkpi = format(hkpi)

# Function for Urbanity numeric handling
def ucat_handling(db,gid,geog,geog2,dbf):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = denomin_cat(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month',gid,gid2,'shop_code']
    # This is for the table formating as per quantum
    columnf = ['Month']

    #Numerator function call
    numero = numerator_cat(db,dbf,indexf,columnf)

    # Handling
    hkpi = numero/deno*100
    return hkpi

    # Format the Indexes to match with the SKU Base
    # hkpi = format(hkpi)

def ucat_handling_nat(db,gid,geog,geog2,dbf):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = denomin_cat(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    #define new dbf for numerator
    dbf = (db[gid2] == geog2)&(db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month',gid2,'shop_code']
    columnf = ['Month']

    #Numerator function call
    numero = numerator_cat(db,dbf,indexf,columnf)

    # Handling
    hkpi = numero/deno*100
    return hkpi

    # Format the Indexes to match with the SKU Base
    # hkpi = format(hkpi)

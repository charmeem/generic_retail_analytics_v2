import pandas as pd
import numpy as np


# General Funcion to Calculate Numeric Handliing KPI
# Function to calculate Denominator
def denomin(db,gid,gid2,dbf,columnf,g):

    # # Check if this is urbanity
    # if gid2=='RC_Total_Urban_Rural':
    #     indexf = [gid2]
    #     # Getting unique store NUmPf set of Rows
    #     newdb = db[['Month','shop_code','RC_Total_Urban_Rural','Num Proj Factor']].drop_duplicates()
    #
    # else:

    indexf = [gid]
    
    # Getting unique store NUmPf set of Rows
    # This is better way then the one we used in numerator calculation
    newdb = db[['Month','shop_code',gid,'Num Proj Factor']].drop_duplicates()
    dbf = (newdb[gid]==g)

    deno = pd.pivot_table(
                    newdb[dbf],
                    index=indexf,
                    values=['Num Proj Factor'],
                    columns=columnf,
                    aggfunc={
                        'Num Proj Factor':np.sum,
                        },
                    dropna=False
                    )

    return deno

def denomin_cat(db,gid,gid2,columnf,g):

    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code',gid,'Num Proj Factor']].drop_duplicates()
    dbf = (newdb[gid]==g)

    deno = pd.pivot_table(
                    newdb[dbf],
                    values=['Num Proj Factor'],
                    columns=columnf,
                    aggfunc={
                        'Num Proj Factor':np.sum,
                        },
                    dropna=False
                    )
    return deno

# Special deno function for National Geogrphy id
def denomin_nat(db,columnf):
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code','Num Proj Factor']].drop_duplicates()

    deno = pd.pivot_table(
                    newdb,
                    values=['Num Proj Factor'],
                    columns=columnf,
                    aggfunc={
                        'Num Proj Factor':np.sum,
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
    #                 values=['Num Proj Factor'],
    #                 aggfunc={'Num Proj Factor':np.max},
    #                 )
    #     numero = pd.pivot_table(
    #                 smch1,
    #                 index=indexf2,
    #                 values=['Num Proj Factor'],
    #                 columns=columnf,
    #                     aggfunc={'Num Proj Factor':np.sum},
    #                 )
    # else:
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['Num Proj Factor','CS_Stock'],
                aggfunc={'Num Proj Factor':np.max,'CS_Stock':np.sum},
                )
    # if smch1.index.all()=='REST OF URBAN (OVERALL)':
    #     smch1.to_csv('smch2.csv')
    # print("SMCHCOLs",smch1.columns)
    # Redefining dbf to get stores with no CS_Stock
    dbf = (smch1.CS_Stock == 0)
    # print('DBF',dbf)
    numero = pd.pivot_table(
                smch1[dbf],
                index=indexf2,
                values=['Num Proj Factor'],
                columns=columnf,
                    aggfunc={'Num Proj Factor':np.sum},
                )

    return numero

# Function to calculate Numerator for Category handling
def numerator_cat(db,dbf,indexf,columnf):

    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['Num Proj Factor','CS_Stock'],
                aggfunc={'Num Proj Factor':np.max,'CS_Stock':np.sum},
                )
    # smch1.to_csv('smchoos.csv')
    # Redefining dbf to get stores with no CS_Stock
    dbf = (smch1.CS_Stock == 0)
    numero = pd.pivot_table(
                smch1[dbf],
                values=['Num Proj Factor'],
                columns=columnf,
                    aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

### Functions for Numeric Handling

### Functions for Category Handling
# Generic function for Ctegory Handling
def cat_handling(db,gid,geog,dbf1,g):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    columnf = ['Month']
    #CAlling External Denominator Function
    deno = denomin_cat(db,gid,gid2,columnf,g)

    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf1&(db.Product_code!=0)&(db.Product_code!='0')
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
    return hkpi

    # Format the Indexes to match with the SKU Base
    # hkpi = format(hkpi)

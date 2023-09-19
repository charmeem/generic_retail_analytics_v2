import pandas as pd
import numpy as np


# Category handling for HIH KPI

# Function to calculate Denominator
def denomin(db,gid,gid2,dbf,columnf,g):
    # print(gid, gid2)
    # # Check if this is urbanity
    # if gid2=='RC_Total_Urban_Rural':
    #     print("you are in if")
    #     indexf = [gid2]
    #     # Getting unique store NUmPf set of Rows
    #     newdb = db[['Month','shop_code',gid2,'Num Proj Factor']].drop_duplicates()
    #
    # else:
    
    indexf = [gid]
    # Getting unique store NUmPf set of Rows
    # db is reduced to limited columns
    db = db[['Month','shop_code',gid,'Num Proj Factor']].drop_duplicates()
    dbf = (db[gid]==g)

    deno = pd.pivot_table(
                    db[dbf],
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

    # # Check if this is urbanity
    # if gid2=='RC_Total_Urban_Rural':
    #     # Getting unique store NUmPf set of Rows
    #     db = db[['Month','shop_code','RC_Total_Urban_Rural','Num Proj Factor']].drop_duplicates()
    # else:
    # Getting unique store NUmPf set of Rows
    db = db[['Month','shop_code',gid,'Num Proj Factor']].drop_duplicates()

    dbf = (db[gid]==g)

    deno = pd.pivot_table(
                    db[dbf],
                    values=['Num Proj Factor'],
                    columns=columnf,
                    aggfunc={
                        'Num Proj Factor':np.sum,
                        },
                    dropna=False
                    )
    return deno

# Special deno function for Total Geogrphy id
def denomin_nat(db,columnf):
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code','Num Proj Factor']].drop_duplicates()
    # dbf = (newdb[indexf[0]]!=0)

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
def numerator(db,dbf,indexf1,indexf2,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['Num Proj Factor'],
                aggfunc={'Num Proj Factor':np.max},
                )
    numero = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                index=indexf2,
                values=['Num Proj Factor'],
                columns=columnf,
                    aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

# Function to calculate Numerator for Category handling
def numerator_cat(db,dbf,indexf,columnf):
    # db[dbf].to_csv('dbp.csv')
    # db.to_csv("dberror.csv")
    # print("indexf1",indexf)
    # print(dbf)
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['Num Proj Factor'],
                aggfunc={'Num Proj Factor':np.max},
                )
    # smch1.to_csv('smch1.csv')
    numero = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                values=['Num Proj Factor'],
                columns=columnf,
                    aggfunc={'Num Proj Factor':np.sum},
                )
    # numero.to_csv('numero.csv')
    return numero
# Function to calculate Numerator for urban nat
def numerator_unat(db,dbf,indexf,columnf,gid2):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
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

    # db.to_csv('dbincathand.csv')
    # print("gid:",gid)
    #Numerator function call
    numero = numerator_cat(db,dbf,indexf,columnf)

    # Handling
    hkpi = numero/deno*100
    return hkpi
    # Format the Indexes to match with the SKU Base
    # hkpi = format(hkpi)

# Function For calculating Total Geoghraphy
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

# # Function for Urbanity numeric handling
# def ucat_handling(db,gid,geog,geog2,dbf):
#
#     # CAlling functions to Calculate DENOMINATOR and NUMERATOR
#     #
#     #Parameters for Pivot table
#     gid2 = 'RC_Total_Urban_Rural'
#     columnf = ['Month']
#
#     #CAlling External Denominator Function
#     deno = denomin_cat(db,gid,gid2,dbf,columnf)
#
#     # Calling External NUMERATOR handling function for EACH level
#     dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
#     indexf= ['Month',gid,gid2,'shop_code']
#     # This is for the table formating as per quantum
#     columnf = ['Month']
#
#     #Numerator function call
#     numero = numerator_cat(db,dbf,indexf,columnf)
#
#     # Handling
#     hkpi = numero/deno*100
#     return hkpi
#
#     # Format the Indexes to match with the SKU Base
#     # hkpi = format(hkpi)

# def ucat_handling_nat(db,gid,geog,geog2,dbf):
#     gid2 = 'RC_Total_Urban_Rural'
#     # CAlling functions to Calculate DENOMINATOR and NUMERATOR
#     #
#     #Parameters for Pivot table
#     columnf = ['Month']
#
#     #CAlling External Denominator Function
#     deno = denomin_cat(db,gid,gid2,dbf,columnf)
#
#     # Calling External NUMERATOR handling function for EACH level
#     #define new dbf for numerator
#     dbf = (db[gid2] == geog2)&(db.Product_code!=0)&(db.Product_code!='0')
#     indexf= ['Month',gid2,'shop_code']
#     columnf = ['Month']
#
#     #Numerator function call
#     numero = numerator_cat(db,dbf,indexf,columnf)
#
#     # Handling
#     hkpi = numero/deno*100
#     return hkpi
#
#     # Format the Indexes to match with the SKU Base
#     # hkpi = format(hkpi)

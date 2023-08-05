import pandas as pd
import numpy as np

# General Funcion to Calculate Numeric Handliing KPI
# The functions to prepare pivot table params for category handling are also included HEre
# Category handling cater for numeric, oos

# Function to calculate Denominator
def denomin(newdb,dbf,indexf,columnf):
    deno = pd.pivot_table(
                newdb[dbf],
                index=indexf,
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={
                    'Num Proj Factor':np.sum
                    },
                    dropna=False
                    )
    return deno

def denomin_urb(newdb,dbf,indexf,columnf):

    deno = pd.pivot_table(
                newdb[dbf],
                index=indexf,
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={
                    'Num Proj Factor':np.sum
                    },
                    dropna=False
                    )

    return deno

def denomin_markt(newdb,dbf,columnf):
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

# Special deno function for Total Geogrphy id
def denomin_nat(newdb,columnf):
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
def numerator(db,newdb,dbf,dbf1,indexf,columnf):
    numero = pd.pivot_table(
                newdb[dbf&dbf1],
                index=indexf,
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

def numerator_urb(db,newdb,dbf,indexf,columnf):
    numero = pd.pivot_table(
                newdb[dbf&(db['Product_code']!=0)],
                index=indexf,
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

# Function to calculate Numerator for Category and Total handling
def numerator_markt(db,newdb,dbf,columnf):
    numero = pd.pivot_table(
                newdb[dbf&(db['Product_code']!=0)],
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={'Num Proj Factor':np.sum},
                )
    return numero


def numerator_nat(db,newdb,dbf,dbf1,columnf):
    numero = pd.pivot_table(
                # newdb[dbf&(db['Product_code']!=0)],
                newdb[dbf1],
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

# Function to calculate Numerator for urban nat
def numerator_unat(db,newdb,dbf,indexf,columnf):
    numero = pd.pivot_table(
                newdb[dbf&(db['Product_code']!=0)],
                index=indexf,
                values=['Num Proj Factor'],
                columns=columnf,
                aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

### Functions for Category Handling ROW
### Denomiator and NUmerator for Category handliing row
def denomin_cat(db,gid,gid2,columnf,g):
    # Check if this is urbanity
    if gid2=='RC_Total_Urban_Rural':
        # Getting unique store NUmPf set of Rows
        newdb = db[['Month','shop_code','RC_Total_Urban_Rural','Num Proj Factor']].drop_duplicates()
    else:
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
def numerator_cat(db,dbf,indexf,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['Num Proj Factor'],
                aggfunc={'Num Proj Factor':np.max},
                )
    numero = pd.pivot_table(
                smch1,
                values=['Num Proj Factor'],
                columns=columnf,
                    aggfunc={'Num Proj Factor':np.sum},
                )
    return numero

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

# Calculating Category Handling Row
# NOTE: This is different from above category handling functions
def cat_handling_nat(db):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table

    columnf = ['Month']
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code','Num Proj Factor']].drop_duplicates()

    #CAlling External Denominator Function
    deno = denomin_nat(newdb,columnf)

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

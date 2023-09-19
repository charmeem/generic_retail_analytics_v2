import pandas as pd
import numpy as np
import importlib
import level_format
importlib.reload(level_format)

# Generic functions for SISH Handling

# Helper functions
def sish(db,dbf,indexf1,indexf2,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['SISH_Volume'],
                aggfunc={'SISH_Volume':np.max},
                )
    numero = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                index=indexf2,
                values=['SISH_Volume'],
                columns=columnf,
                    aggfunc={'SISH_Volume':np.sum},
                )

    return numero


def sish_mix(db,dbf,indexf,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['SISH_Volume'],
                aggfunc={'SISH_Volume':np.max},
                )

    sish = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                values=['SISH_Volume'],
                columns=columnf,
                    aggfunc={'SISH_Volume':np.sum},
                )
    return sish

# Main Functions
def sish_handling(db,dbf,hlevel,gid):
    # CAlling functions to Calculate Sish
    #
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
    #     sishd = sish_mix(db,dbf,indexf1,columnf)
    # else:
    columnf = [*hlevel,'Month']
    sishd = sish(db,dbf,indexf1,indexf2,columnf)

    # # renaming 'proj_vol' back to 'Volume' for proper division
    # numero.rename(columns={'proj_vol':'Volume'},inplace=True)

    #Converting dataframe to series to avoid error while dividing below
    # hkpi=sishd.iloc[0]

    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return sishd

# Function For calculating National Geoghraphy
def sish_handling_nat(db,dbf,hlevel):

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
    #     # indexf2 = ['SM','Vendor','Brand','PS']

    columnf = [*hlevel,'Month']

    #Numerator function call
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['SISH_Volume'],
                aggfunc={'SISH_Volume':np.max},
                )
    
    numero = pd.pivot_table(
                smch1,
                values=['SISH_Volume'],
                columns=columnf,
                    aggfunc={'SISH_Volume':np.sum},
                )

    # renaming 'proj_vol' back to 'Volume' for proper division
    # numero.rename(columns={'SISH_Volume':'Volume'},inplace=True)

    #Converting dataframe to series to avoid error while dividing below
    # hkpi=numero.iloc[0]

    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)

    return numero


# Function for Urbanity weighted handling
def usish_handling(db,gid,geog,geog2,dbf,level):
    gid2 = 'RC_Total_Urban_Rural'

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
    numero = sish(db,dbf,indexf1,indexf2,columnf)

    return numero

def usish_handling_nat(db,gid,geog,geog2,dbf,level):
    gid2 = 'RC_Total_Urban_Rural'
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
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['SISH_Volume'],
                aggfunc={'SISH_Volume':np.max},
                )
    numero = pd.pivot_table(
                smch1,
                index=[gid2],
                values=['SISH_Volume'],
                columns=columnf,
                    aggfunc={'SISH_Volume':np.sum},
                )
    return numero

# Category handling functions
def numerator_cat(db,dbf,indexf,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['SISH_Volume'],
                aggfunc={'SISH_Volume':np.max},
                )
    numero = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                values=['SISH_Volume'],
                columns=columnf,
                    aggfunc={'SISH_Volume':np.sum},
                )
    return numero

def cat_handling(db,gid,geog,dbf):
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month',gid,'shop_code']
    columnf = ['Month']
    numero = numerator_cat(db,dbf,indexf,columnf)

    return numero

def cat_handling_nat(db):
    dbf = (db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month','shop_code']
    columnf = ['Month']

    numero = numerator_cat(db,dbf,indexf,columnf)
    return numero

def ucat_handling(db,gid,geog,geog2,dbf):
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month',gid,gid2,'shop_code']
    numero = numerator_cat(db,dbf,indexf,columnf)

    return numero

def ucat_handling_nat(db,gid,geog,geog2,dbf):
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    dbf = (db[gid2] == geog2)&(db.Product_code!=0)&(db.Product_code!='0')
    indexf= ['Month',gid2,'shop_code']
    numero = numerator_cat(db,dbf,indexf,columnf)
    return numero

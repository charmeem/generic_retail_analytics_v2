import importlib
import sppd2
importlib.reload(sppd2)
import level_format
importlib.reload(level_format)

# Generic function for NUmeric Handling
def sppdf(db,gid,geog,dbf,level):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    # gid2='dummy'
    # Calling Volume functions and calculating ooscost

    dbf = dbf&(db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)

    # NUMERATOR generating function based on input level
    if level=='SKU':
        hlevel=['SM','Vendor','Brand','PS','SKU']
        indexf1= ['Month',gid,'SM','Vendor','Brand','PS','SKU','shop_code']

    if level=='SM':
        hlevel = ['SM']
        indexf1= ['Month',gid,'SM','shop_code']

    if level=='Manu':
        hlevel=['SM','Vendor']
        indexf1= ['Month',gid,'SM','Vendor','shop_code']

    if level=='Brand':
        hlevel=['SM','Vendor','Brand']
        indexf1= ['Month',gid,'SM','Vendor','Brand','shop_code']

    if level=='PS':
        hlevel=['SM','Vendor','Brand','PS']
        indexf1= ['Month',gid,'SM','Vendor','Brand','PS','shop_code']

    indexf2 = [gid]

    if geog == 'irmarket' or geog == 'tenkc' or geog == 'fourmetros' or geog == 'kpajk':
        columnf = ['Month',*hlevel]
        vols = sppd2.vols_mix(db,dbf,indexf1,columnf,level)   # oos volume
        vol = sppd2.volume_mix(db,dbf,indexf1,columnf)    # normal volume

    else:
        columnf = [*hlevel,'Month']
        vols = sppd2.vols(db,dbf,indexf1,indexf2,columnf,level)   # oos volume
        vol = sppd2.volume(db,dbf,indexf1,indexf2,columnf)            # normal volume

    # renaming columns for proper division
    vols = volo.rename(columns={'proj_vol':'sppd'})
    vol = vol.rename(columns={'proj_vol':'sppd'})


    #Converting dataframe to series to avoid error while dividing below
    vols=vols.iloc[0]
    vol=vol.iloc[0]


    # OOS Cost
    hkpi =vols/vol
    # hkpi.to_csv('hkpi.csv')
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

# Function For calculating National Geoghraphy
def sppd_nat(db,level):

    #Parameters for Pivot table
    # columnf = ['Month']
    dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)

    # Calling External NUMERATOR handling function for EACH level
    if level=='SKU':
        hlevel=['SM','Vendor','Brand','PS','SKU']
        indexf1= ['Month','SM','Vendor','Brand','PS','SKU','shop_code']
        # indexf2 = ['SM','Vendor','Brand','PS','SKU']

    if level=='SM':
        hlevel=['SM']
        indexf1= ['Month','SM','shop_code']
        # indexf3 = ['Month','SM']
        # indexf2 = ['SM']

    if level=='Manu':
        hlevel=['SM','Vendor']
        indexf1= ['Month','SM','Vendor','shop_code']
        # indexf2 = ['SM','Vendor']

    if level=='Brand':
        hlevel=['SM','Vendor','Brand']
        indexf1= ['Month','SM','Vendor','Brand','shop_code']
        # indexf2 = ['SM','Vendor','Brand']

    if level=='PS':
        hlevel=['SM','Vendor','Brand','PS']
        indexf1= ['Month','SM','Vendor','Brand','PS','shop_code']
        # indexf2 = ['SM','Vendor','Brand','PS']

    columnf = [*hlevel,'Month']
    vols = sppd2.volsnat(db,dbf,indexf1,columnf,level)   # oos volume
    vol = sppd2.volumenat(db,dbf,indexf1,columnf)    # normal volume


    # # Converting indeces to columns
    # val=val.reset_index()
    # volo=volo.reset_index()
    # vol = vol.reset_index()

    # renaming columns for proper division
    vols = vols.rename(index={'proj_vol':'sppd'})
    vol = vol.rename(index={'proj_vol':'sppd'})
    vols.to_csv('vols.csv')
    vol.to_csv('vol.csv')

    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =vols/vol
    hkpi.to_csv('hkpinat.csv')
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    # hkpi.to_csv('hkpi2.csv')
    return hkpi


# Function for Urbanity
def usppdf(db,gid,geog,geog2,dbf,level):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    dbf = dbf&(db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)

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
    vols = sppd2.vols(db,dbf,indexf1,indexf2,columnf,level)   # oos volume
    vol = sppd2.volume(db,dbf,indexf1,indexf2,columnf)            # normal volume

    # renaming columns for proper division
    vols = vols.rename(columns={'proj_vol':'sppd'})
    vol = vol.rename(columns={'proj_vol':'sppd'})

    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =vols/vol
    # hkpi.to_csv('hkpi.csv')

    # Format the Indexes to match with the SKU Base
    # hkpi =level_format.format(hkpi,level)
    return hkpi

def usppd_nat(db,gid,geog,geog2,dbf,level):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate Value
    #
    #Parameters for Pivot table

    dbf = dbf&(db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)

    #CAlling External Denominator Function
    # val = ooscost2.value(db,gid,gid2,dbf,columnf)

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
    vols = sppd2.volsunat(db,dbf,indexf1,columnf,gid2,level)   # oos volume
    vol = sppd2.volumeunat(db,dbf,indexf1,columnf,gid2)            # normal volume


    # renaming columns for proper division
    volo = volo.rename(columns={'proj_vol':'sppd'})
    vol = vol.rename(columns={'proj_vol':'sppd'})

    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =vols/vol
    # hkpi.to_csv('hkpi.csv')
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

# CATEGORY HANDLING FUNCTIONS
def sppdcat_handling(db,gid,geog,dbf):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    columnf = ['Month']


    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month',gid,'shop_code']
    columnf = ['Month']
    indexf2 = [gid]

    #functions call
    vols_cat = sppd2.vols_cat(db,dbf,indexf1,columnf)
    vol_cat = sppd2.volume_cat(db,dbf,indexf1,indexf2,columnf)

    # renaming columns for proper division
    vols_cat = vols_cat.rename(index={'proj_vol':'sppd'})
    vol_cat = vol_cat.rename(index={'proj_vol':'sppd'})

    # Handling
    hkpi = vols_cat/vol_cat

    return hkpi

def sppdcat_handling_nat(db):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    # Calling functions
    dbf = (db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month','shop_code']
    columnf = ['Month']

    vols_cat = sppd2.vols_cat(db,dbf,indexf1,columnf)
    vol_cat = sppd2.volumenat(db,dbf,indexf1,columnf)

    # renaming columns for proper division
    vols_cat = vols_cat.rename(index={'proj_vol':'ooscost'})
    vol_cat = vol_cat.rename(index={'proj_vol':'ooscost'})

    # Handling
    hkpi = voloos_cat/vol_cat

    return hkpi

# Function for Urbanity numeric handling
def sppducat_handling(db,gid,geog,geog2,dbf):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month',gid,gid2,'shop_code']
    # This is for the table formating as per quantum
    columnf = ['Month']
    indexf2 = [gid]

    #functions call
    vols_cat = sppd2.vols_cat(db,dbf,indexf1,columnf)
    vol_cat = sppd2.volume_cat(db,dbf,indexf1,indexf2,columnf)

    # renaming columns for proper division
    vols_cat = vols_cat.rename(index={'proj_vol':'sppd'})
    vol_cat = vol_cat.rename(index={'proj_vol':'sppd'})

    # Handling
    hkpi = vols_cat/vol_cat

    return hkpi

def sppducat_handling_nat(db,gid,geog,geog2,dbf):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    # Calling External NUMERATOR handling function for EACH level
    #define new dbf for numerator
    dbf = (db[gid2] == geog2)&(db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month',gid2,'shop_code']
    columnf = ['Month']
    indexf2 = [gid2]

    #functions call
    vols_cat = sppd2.vols_cat(db,dbf,indexf1,columnf)
    vol_cat = sppd2.volume_cat(db,dbf,indexf1,indexf2,columnf)

    # renaming columns for proper division
    vols_cat = vols_cat.rename(index={'proj_vol':'ooscost'})
    vol_cat = vol_cat.rename(index={'proj_vol':'ooscost'})

    # Handling
    hkpi = vols_cat/vol_cat

    return hkpi

import importlib
import ooscost2 
importlib.reload(ooscost2)
import level_format 
importlib.reload(level_format)

# Generic function for NUmeric Handling
def ocost(db,dbf,hlevel,gid):
    
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    # Calling Volume functions and calculating ooscost

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
    #     val = ooscost2.value_mix(db,gid,gid2,dbf,columnf)
    #     volo = ooscost2.voloos_mix(db,dbf,indexf1,columnf,level)   # oos volume
    #     vol = ooscost2.volume_mix(db,dbf,indexf1,columnf)    # normal volume
    #
    # else:
    columnf = [*hlevel,'Month']
    val = ooscost2.value(db,gid,gid2,dbf,columnf)
    volo = ooscost2.voloos(db,dbf,indexf1,indexf2,columnf,hlevel)   # oos volume
    vol = ooscost2.volume(db,dbf,indexf1,indexf2,columnf)            # normal volume

    # renaming columns for proper division
    val = val.rename(columns={'val_abs':'ooscost'})
    volo = volo.rename(columns={'proj_vol':'ooscost'})
    vol = vol.rename(columns={'proj_vol':'ooscost'})



    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =val*(volo/vol)
    # hkpi.to_csv('hkpi.csv')
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

# Function For calculating Total Geoghraphy
def ocost_nat(db,dbf,hlevel):
    
    #Parameters for Pivot table

    # Calling External NUMERATOR handling function for EACH level
    indexf1= ['Month',*hlevel,'shop_code']
    # if level=='SKU':
    #     hlevel=['SM','Vendor','Brand','PS','SKU']
    #     indexf1= ['Month','SM','Vendor','Brand','PS','SKU','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand','PS','SKU']
    #
    # if level=='SM':
    #     hlevel=['SM']
    #     indexf1= ['Month','SM','shop_code']
    #     # indexf3 = ['Month','SM']
    #     # indexf2 = ['SM']
    #
    # if level=='Manu':
    #     hlevel=['SM','Vendor']
    #     indexf1= ['Month','SM','Vendor','shop_code']
    #     # indexf2 = ['SM','Vendor']
    #
    # if level=='Brand':
    #     hlevel=['SM','Vendor','Brand']
    #     indexf1= ['Month','SM','Vendor','Brand','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand']
    #
    # if level=='PS':
    #     hlevel=['SM','Vendor','Brand','PS']
    #     indexf1= ['Month','SM','Vendor','Brand','PS','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand','PS']

    columnf = [*hlevel,'Month']
    val = ooscost2.value_nat(db,dbf,columnf)
    volo = ooscost2.voloosnat(db,dbf,indexf1,columnf,hlevel)   # oos volume
    vol = ooscost2.volumenat(db,dbf,indexf1,columnf)    # normal volume


    # # Converting indeces to columns
    # val=val.reset_index()
    # volo=volo.reset_index()
    # vol = vol.reset_index()

    # renaming columns for proper division
    volo = volo.rename(index={'proj_vol':'ooscost'})
    vol = vol.rename(index={'proj_vol':'ooscost'})
    val = val.rename(index={'val_abs':'ooscost'})

    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =val*volo/vol
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    # hkpi.to_csv('hkpi2.csv')
    return hkpi


# Function for Urbanity
def uocost(db,gid,geog,geog2,dbf,level):
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
    val = ooscost2.value(db,gid,gid2,dbf,columnf)
    volo = ooscost2.voloos(db,dbf,indexf1,indexf2,columnf,level)   # oos volume
    vol = ooscost2.volume(db,dbf,indexf1,indexf2,columnf)            # normal volume

    # renaming columns for proper division
    volo = volo.rename(columns={'proj_vol':'ooscost'})
    vol = vol.rename(columns={'proj_vol':'ooscost'})
    val = val.rename(columns={'val_abs':'ooscost'})

    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =val*(volo/vol)
    # hkpi.to_csv('hkpi.csv')

    # Format the Indexes to match with the SKU Base
    # hkpi =level_format.format(hkpi,level)
    return hkpi

def uocost_nat(db,gid,geog,geog2,dbf,level):
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
    val = ooscost2.value(db,gid,gid2,dbf,columnf)
    volo = ooscost2.voloosunat(db,dbf,indexf1,columnf,gid2,level)   # oos volume
    vol = ooscost2.volumeunat(db,dbf,indexf1,columnf,gid2)            # normal volume


    # renaming columns for proper division
    volo = volo.rename(columns={'proj_vol':'ooscost'})
    vol = vol.rename(columns={'proj_vol':'ooscost'})
    val = val.rename(columns={'val_abs':'ooscost'})

    #Converting dataframe to series to avoid error while dividing below
    # volo=volo.iloc[0]
    # vol=vol.iloc[0]

    # OOS Cost
    hkpi =val*(volo/vol)
    # hkpi.to_csv('hkpi.csv')
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

# CATEGORY HANDLING FUNCTIONS
def ocostcat_handling(db,gid,geog,dbf):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    columnf = ['Month']

    #CAlling Value Function
    val = ooscost2.value_cat(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month',gid,'shop_code']
    columnf = ['Month']
    indexf2 = [gid]

    #functions call
    voloos_cat = ooscost2.voloos_cat(db,dbf,indexf1,columnf)
    vol_cat = ooscost2.volume_cat(db,dbf,indexf1,indexf2,columnf)

    # renaming columns for proper division
    voloos_cat = voloos_cat.rename(index={'proj_vol':'ooscost'})
    vol_cat = vol_cat.rename(index={'proj_vol':'ooscost'})
    val = val.rename(index={'val_abs':'ooscost'})

    # Handling
    hkpi = val*(voloos_cat/vol_cat)

    return hkpi

def ocostcat_handling_nat(db,indexf):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    # Calling functions
    dbf = (db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month','shop_code']
    columnf = ['Month']

    voloos_cat = ooscost2.voloos_cat(db,dbf,indexf1,columnf)
    vol_cat = ooscost2.volumenat(db,dbf,indexf1,columnf)

    # Calling value pivot
    dbf = (db[indexf[0]]!=0)
    # dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    val = ooscost2.value_nat(db,dbf,columnf)

    # renaming columns for proper division
    voloos_cat = voloos_cat.rename(index={'proj_vol':'ooscost'})
    vol_cat = vol_cat.rename(index={'proj_vol':'ooscost'})
    val = val.rename(index={'val_abs':'ooscost'})

    # Handling
    hkpi = val*(voloos_cat/vol_cat)

    return hkpi

# Function for Urbanity numeric handling
def ocostucat_handling(db,gid,geog,geog2,dbf):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    #CAlling Value Function
    val = ooscost2.value_cat(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    dbf = dbf&(db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month',gid,gid2,'shop_code']
    # This is for the table formating as per quantum
    columnf = ['Month']
    indexf2 = [gid]

    #functions call
    voloos_cat = ooscost2.voloos_cat(db,dbf,indexf1,columnf)
    vol_cat = ooscost2.volume_cat(db,dbf,indexf1,indexf2,columnf)

    # renaming columns for proper division
    voloos_cat = voloos_cat.rename(index={'proj_vol':'ooscost'})
    vol_cat = vol_cat.rename(index={'proj_vol':'ooscost'})
    val = val.rename(index={'val_abs':'ooscost'})

    # voloos_cat.to_csv('voloos.csv')
    # vol_cat.to_csv('vol_cat.csv')
    # val.to_csv('val.csv')

    # Handling
    hkpi = val*(voloos_cat/vol_cat)
    # hkpi.to_csv('hkpi.csv')

    return hkpi

def ocostucat_handling_nat(db,gid,geog,geog2,dbf):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    #CAlling Value Function
    val = ooscost2.value_nat(db,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    #define new dbf for numerator
    dbf = (db[gid2] == geog2)&(db.Product_code!=0)&(db.Product_code!='0')
    indexf1= ['Month',gid2,'shop_code']
    columnf = ['Month']
    indexf2 = [gid2]

    #functions call
    voloos_cat = ooscost2.voloos_cat(db,dbf,indexf1,columnf)
    vol_cat = ooscost2.volume_cat(db,dbf,indexf1,indexf2,columnf)

    # renaming columns for proper division
    voloos_cat = voloos_cat.rename(index={'proj_vol':'ooscost'})
    vol_cat = vol_cat.rename(index={'proj_vol':'ooscost'})
    val = val.rename(index={'val_abs':'ooscost'})


    # Handling
    hkpi = val*(voloos_cat/vol_cat)

    return hkpi

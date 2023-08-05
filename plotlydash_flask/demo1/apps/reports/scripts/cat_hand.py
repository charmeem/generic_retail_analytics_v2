## HIH calculations
## This is Function used as a denominator for HIH

import numpy as np
import importlib
import cath_hand2
importlib.reload(cath_hand2)
import level_format
importlib.reload(level_format)

# Generic function for NUmeric Handling
def cath_handling(db,dbf,hlevel,gid,g):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']
    indexf = [gid]
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code',gid,'Num Proj Factor']].drop_duplicates()
    dbf = (newdb[gid]==g)

    #@ Create new dataframe ndb from cpmmon index rows of db and newdb
    #@ Then use ndb to get the filter dbf for cath_hand2.numerator_nat function call below
    #@ This will supress Booleankey reindex Warning messages
    indx = np.intersect1d(db.index,newdb.index)
    ndb = db.loc[indx]
    # # ndb.to_csv('ndb2.csv')
    dbf1 = ndb['Product_code']!=0
    # dbf1 = dbf&dbf2
    # # dbf1 = dbf2


    deno = cath_hand2.denomin(newdb,dbf,indexf,columnf)
    numero = cath_hand2.numerator(db,newdb,dbf,dbf1,indexf,columnf)
    # numero.to_csv('numeroo.csv')
    # Category Handling
    hkpi = numero/deno*100
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    # hkpi.to_csv('hkpih.csv')
    return hkpi

# Function For calculating Total Geoghraphy
def cath_handling_nat(db,dbf,hlevel):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #Parameters for Pivot table
    # dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    columnf = ['Month']
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code','Num Proj Factor']].drop_duplicates()

    # # Create new dataframe ndb from cpmmon index rows of db and newdb
    # # Then use ndb to get the filter dbf for cath_hand2.numerator_nat function call below
    # # This will supress Booleankey reindex Warning messages
    indx = np.intersect1d(db.index,newdb.index)
    ndb = db.loc[indx]
    # ndb.to_csv('ndb.csv')
    # newdb.to_csv('newdb.csv')
    dbf1 = ndb['Product_code']!=0

    #CAlling External Denominator and Numerator Functions
    deno = cath_hand2.denomin_nat(newdb,columnf)
    #Numerator function call
    numero = cath_hand2.numerator_nat(db,newdb,dbf,dbf1,columnf)

    # Handling
    hkpi = numero/deno*100
    # hkpi = level_format.format(hkpi,level)

    return hkpi


# Function for Urbanity numeric handling
def ucath_handling(db,gid,geog,dbf,level):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    indexf = [gid2]
    columnf = ['Month']
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code',gid2,'Num Proj Factor']].drop_duplicates()

    #CAlling External Denominator and Numerator Functions
    deno = cath_hand2.denomin_urb(newdb,dbf,indexf,columnf)

    #Numerator function call
    numero = cath_hand2.numerator_urb(db,newdb,dbf,indexf,columnf)

    # Handling
    hkpi = numero/deno*100

    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

def ucath_handling_nat(db,gid,geog,dbf,level):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    indexf = [gid2]
    columnf = ['Month']
    # Getting unique store NUmPf set of Rows
    newdb = db[['Month','shop_code',gid2,'Num Proj Factor']].drop_duplicates()

    #CAlling External Denominator Function
    deno = cath_hand2.denomin_urb(newdb,dbf,indexf,columnf)

    # # Calling External NUMERATOR handling function for EACH level
    # if level=='SKU':
    #     indexf= ['Month',gid2,'SM','Vendor','Brand','PS','SKU','shop_code']
    # if level=='SM':
    #     indexf= ['Month',gid2,'SM','shop_code']
    # if level=='Manu':
    #     indexf= ['Month',gid2,'SM','Vendor','shop_code']
    # if level=='Brand':
    #     indexf= ['Month',gid2,'SM','Vendor','Brand','shop_code']
    # if level=='PS':
    #     indexf= ['Month',gid2,'SM','Vendor','Brand','PS','shop_code']

    #Numerator function call
    numero = cath_hand2.numerator_unat(db,newdb,dbf,indexf,columnf)


    # Handling
    hkpi = numero/deno*100

    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

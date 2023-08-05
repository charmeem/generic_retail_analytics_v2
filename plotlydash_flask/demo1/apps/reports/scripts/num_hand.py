import importlib
import num_hand2 
importlib.reload(num_hand2)
import level_format 
importlib.reload(level_format)

# Generic function for NUmeric Handling
def numeric_handling(db,dbf,hlevel,gid,g):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    columnf = ['Month']

    deno = num_hand2.denomin(db,gid,gid2,dbf,columnf,g)
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)

    indexf1= ['Month',gid,*hlevel,'shop_code']

    # # NUMERATOR generating function based on input level
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
    #     numero = num_hand2.numerator_cat(db,dbf,indexf1,columnf)
    # else:
    columnf = [*hlevel,'Month']
    numero = num_hand2.numerator(db,dbf,indexf1,indexf2,columnf)


    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]
    # Handling
    hkpi = numero/deno*100
    return hkpi

# Function For calculating Total Geoghraphy
def numeric_handling_nat(db,dbf,hlevel):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table

    columnf = ['Month']
#         dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #CAlling External Denominator Function
    deno = num_hand2.denomin_nat(db,columnf)

    # Calling External NUMERATOR handling function for EACH level
    indexf1= ['Month',*hlevel,'shop_code']

    # if level=='SKU':
    #     hlevel=['SM','Vendor','Brand','PS','SKU']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf= ['Month','SM','Vendor','Brand','PS','SKU','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand','PS','SKU']
    #
    # if level=='SM':
    #     hlevel=['SM']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf= ['Month','SM','shop_code']
    #     # indexf2 = ['SM']
    #
    # if level=='Manu':
    #     hlevel=['SM','Vendor']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf= ['Month','SM','Vendor','shop_code']
    #     # indexf2 = ['SM','Vendor']
    #
    # if level=='Brand':
    #     hlevel=['SM','Vendor','Brand']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf= ['Month','SM','Vendor','Brand','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand']
    #
    # if level=='PS':
    #     hlevel=['SM','Vendor','Brand','PS']
    #     dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #     indexf= ['Month','SM','Vendor','Brand','PS','shop_code']
    #     # indexf2 = ['SM','Vendor','Brand','PS']

    columnf = [*hlevel,'Month']

    #Numerator function call
    numero = num_hand2.numerator_cat(db,dbf,indexf1,columnf)
    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    return hkpi


# Function for Urbanity numeric handling
def unumeric_handling(db,gid,geog,geog2,dbf,level):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = num_hand2.denomin(db,gid,gid2,dbf,columnf)
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
    numero = num_hand2.numerator(db,dbf,indexf1,indexf2,columnf)

    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

def unumeric_handling_nat(db,gid,geog,geog2,dbf,level):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = num_hand2.denomin(db,gid,gid2,dbf,columnf)

    # Calling External NUMERATOR handling function for EACH level
    if level=='SKU':
        hlevel=['SM','Vendor','Brand','PS','SKU']
        indexf= ['Month',gid2,'SM','Vendor','Brand','PS','SKU','shop_code']

    if level=='SM':
        hlevel=['SM']
        indexf= ['Month',gid2,'SM','shop_code']

    if level=='Manu':
        indexf= ['Month',gid2,'SM','Vendor','shop_code']
        hlevel = ['SM','Vendor']

    if level=='Brand':
        indexf= ['Month',gid2,'SM','Vendor','Brand','shop_code']
        hlevel = ['SM','Vendor','Brand']

    if level=='PS':
        indexf= ['Month',gid2,'SM','Vendor','Brand','PS','shop_code']
        hlevel = ['SM','Vendor','Brand','PS']

    columnf = [*hlevel,'Month']

    #Numerator function call
    numero = num_hand2.numerator_unat(db,dbf,indexf,columnf,gid2)

    # Solving division error after anaconda upgrade
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)
    # deno.to_csv('denoo.csv')
    # numero.to_csv('numeroo.csv')
    # convert nemerator from df to series
    numero = numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    return hkpi

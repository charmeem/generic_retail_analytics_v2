import pandas as pd
import numpy as np
import importlib
import wt_hand2 
importlib.reload(wt_hand2)
import level_format
importlib.reload(level_format)

# Generic function for NUmeric Handling
def wt_handling(db,dbf,hlevel,gid):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2='dummy'
    columnf = ['Month']

    #CAlling External Denominator Function
    # if geog == 'irmarket' or geog == 'tenkc' or geog == 'fourmetros' or geog == 'kpajk':
    #     deno = wt_hand2.denomin_mix(db,gid,gid2,dbf,columnf)
    #     # deno.to_csv('deno.csv')
    # else:
    deno = wt_hand2.denomin(db,gid,gid2,dbf,columnf)
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)


    # NUMERATOR generating function based on input level
    indexf1= ['Month',gid,*hlevel,'shop_code']

    indexf2 = [gid]
    # if geog == 'irmarket' or geog == 'tenkc' or geog == 'fourmetros' or geog == 'kpajk':
    #     columnf = ['Month',*hlevel]
    #     numero = wt_hand2.numerator_mix(db,dbf,indexf1,columnf)
        # numero.to_csv('numero.csv')
    # else:
    columnf = [*hlevel,'Month']
    numero = wt_hand2.numerator(db,dbf,indexf1,indexf2,columnf)


    # renaming 'proj_vol' back to 'Volume' for proper division
    numero.rename(columns={'proj_vol':'Volume'},inplace=True)

    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    # hkpi.to_csv('hkpiwt.csv')
    return hkpi

# Function For calculating National Geoghraphy
def wt_handling_nat(db,dbf,hlevel):

    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table

    columnf = ['Month']
#         dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
    #CAlling External Denominator Function
    deno = wt_hand2.denomin_nat(db,columnf)

    # Calling External NUMERATOR handling function
    indexf1= ['Month',*hlevel,'shop_code']

    columnf = [*hlevel,'Month']
    # print(hlevel)
    #Numerator function call
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )

    numero = pd.pivot_table(
                smch1,
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )


    # renaming 'proj_vol' back to 'Volume' for proper division
    numero.rename(columns={'proj_vol':'Volume'},inplace=True)
    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100
    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)

    return hkpi


# Function for Urbanity weighted handling
def uwt_handling(db,gid,geog,geog2,dbf,hlevel):
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    gid2 = 'RC_Total_Urban_Rural'
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = wt_hand2.denomin(db,gid,gid2,dbf,columnf)
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)

    indexf1= ['Month',gid,gid2,*hlevel,'shop_code']


    indexf2 = [gid2]

    # This is for the table formating as per quantum
    if geog=='kpajk' or geog=='shopper' or geog=='trade':
        columnf = ['Month',*hlevel]
    else:
        columnf = [*hlevel,'Month']

    #Numerator function call
    numero = wt_hand2.numerator(db,dbf,indexf1,indexf2,columnf)

    # renaming 'proj_vol' back to 'Volume' for proper division
    numero.rename(columns={'proj_vol':'Volume'},inplace=True)

    #Converting dataframe to series to avoid error while dividing below
    numero=numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    # Format the Indexes to match with the SKU Base
    # hkpi =level_format.format(hkpi,level)
    return hkpi

def uwt_handling_nat(db,gid,geog,geog2,dbf,hlevel):
    gid2 = 'RC_Total_Urban_Rural'
    # CAlling functions to Calculate DENOMINATOR and NUMERATOR
    #
    #Parameters for Pivot table
    columnf = ['Month']

    #CAlling External Denominator Function
    deno = wt_hand2.denomin(db,gid,gid2,dbf,columnf)

    indexf1= ['Month',gid2,*hlevel,'shop_code']


    columnf = [*hlevel,'Month']

    #Numerator function call
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )
    numero = pd.pivot_table(
                smch1,
                index=[gid2],
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )
    # renaming 'proj_vol' back to 'Volume' for proper division
    numero.rename(columns={'proj_vol':'Volume'},inplace=True)
    # if level =='SM':
    #     numero.to_csv('nwt.csv')
    # Solving division error after anaconda upgrade
    #remove one level of column in denomin
    deno.columns = deno.columns.droplevel(0)
    # convert nemerator from df to series
    numero = numero.iloc[0]

    # Handling
    hkpi = numero/deno*100

    # Format the Indexes to match with the SKU Base
    # hkpi = level_format.format(hkpi,level)
    return hkpi

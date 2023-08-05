import pandas as pd
import numpy as np
import importlib
import helper
importlib.reload(helper)
import level_format2
importlib.reload(level_format2)

# Functions to build geographical tables by pivoting and concating

def geo_build(db,geo,d,hlevel,market_array,valuef1,valuef2):
    # kpi='sale_price'
    # valuef1 = kpi
    # valuef2 = 'Sale_new'
    kpi = valuef1
    indexf=hlevel

    # A pivot function to be called as needed
    def pivot(dbf,valuef1,valuef2,indexf,columnf):
        sale_p = pd.pivot_table(
               db[dbf],
               index=indexf,values=[valuef1], columns=columnf, aggfunc={valuef1:np.sum},
               # fill_value=0
                )
        # if indexf==['Vendor']:
        # sale_p.to_csv('sale_p3.csv')
        t_sale = pd.pivot_table(
            db[dbf],
           index=indexf,values=[valuef2], columns=columnf, aggfunc={valuef2:np.sum},
           # fill_value=0,
             )
        # if indexf==['Vendor']:
        # t_sale.to_csv('t_sale.csv')
        t_sale = t_sale.rename(columns={valuef2:valuef1})
        # t_sale.to_csv('salet3.csv')

        result=sale_p/t_sale
        # result.to_csv('result3.csv')
        return result

    # Total MBD
    def Mkt1():
        dbf = (db[indexf[0]]!=0)
        #First create Total table
        columnf = ['Month']
        hkpi = pivot(dbf, valuef1,valuef2,indexf, columnf)

        # once more roundingsnto prevent some minor unrounded values found
        # Appplying round method to all the columns
        # hkpi = hkpi.applymap(lambda x:round(x,d))
        # hkpi[kpi] = hkpi[kpi].round(decimals=d)

        # rename kpi column
        hkpi = hkpi.rename(columns={kpi:'Total'},level=0)
        # if hlevel==['Vendor']:
            # hkpi.to_csv('resultgeo.csv')
        return hkpi


    def market(hkpi,mkt):
        gid=mkt
        # geog are the geograhies in Mkt5 columns
        # We have to create a loop over unique values and calculate handling
        geog = db[gid].unique()

        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issues
        geog=sorted(geog)

        for g in geog:

            dbf = (db[indexf[0]]!=0)&(db[gid]==g)
            columnf = [mkt,'Month']
            hgeo = pivot(dbf, valuef1,valuef2,indexf, columnf)
            # hgeo.columns = pd.MultiIndex.from_product([hgeo.columns, [g]]).swaplevel(0,1)
            # once more roundingsnto prevent some minor unrounded found
            # Appplying round method to all the columns
            # hgeo = hgeo.applymap(lambda x:round(x,d))
            # hgeo[kpi] = hgeo[kpi].round(decimals=d)

            hgeo.columns=hgeo.columns.droplevel(0)

            hkpi = pd.concat([hkpi,hgeo],axis=1)

        return hkpi

    # Calculation for Total MBD
    if 'Mkt1' in market_array:

        # strip away Mkt1 from array
        market_array = [string for string in market_array if string !='Mkt1']

        hkpi = Mkt1()          #National

        # Calculating Other MBDs other then Mkt1
        for mkt in market_array:
            hkpi = market(hkpi,mkt)
            # hkpi = pd.concat([hkpi,hgeo],axis=1)

    else:
        # Calculating Other MBDs other then Mkt1
        # This one is to start concatenation chain
        hkpi = market(market_array[0])

        for mkt in market_array[1:]:
            hgeo = market(mkt)
            hkpi = pd.concat([hkpi,hgeo],axis=1)


    # Converting indeces to columns
    # hkpi=hkpi.reset_index()

    return hkpi



# CATEGORY ########################################################

# Functions to build geographical tables by pivoting and concating
def geo_build_cat(db,geo,d,hlevel,market_array,valuef1,valuef2):
    kpi = valuef1
    indexf=hlevel
    # A pivot function to be called as needed
    def pivot(dbf,valuef1,valuef2,indexf,columnf):

        sale_p = pd.pivot_table(
               db[dbf],
               values=[valuef1], columns=columnf, aggfunc={valuef1:np.sum},
               fill_value=0
                )

        t_sale = pd.pivot_table(
            db[dbf],
           values=[valuef2], columns=columnf, aggfunc={valuef2:np.sum},
           fill_value=0,
             )

        t_sale = t_sale.rename(index={valuef2:valuef1})
        result=sale_p/t_sale
        # result =  result.reset_index()
        return result

    # Functions calls


    # Total MBD
    def Mkt1():
        dbf = (db[indexf[0]]!=0)
        #First create Total table
        columnf = ['Month']
        hkpi = pivot(dbf, valuef1,valuef2,indexf, columnf)

        # Adding kpi column and bringing on top
        hkpi.columns = pd.MultiIndex.from_product([hkpi.columns, ['Total']]).swaplevel(0,1)

        # once more roundingsnto prevent some minor unrounded values found
        # Appplying round method to all the columns
        # hkpi = hkpi.applymap(lambda x:round(x,d))
        # hkpi[kpi] = hkpi[kpi].round(decimals=d)

        # rename kpi column
        # hkpi = hkpi.rename(columns={kpi:'Total'},level=0)

        return hkpi


    def market(hkpi,mkt):
        gid=mkt
        # geog are the geograhies in Mkt5 columns
        # We have to create a loop over unique values and calculate handling
        geog = db[gid].unique()
        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issue in SISH
        geog=sorted(geog)

        for g in geog:
            dbf = (db[indexf[0]]!=0)&(db[gid]==g)
            columnf = [mkt,'Month']
            hgeo = pivot(dbf, valuef1,valuef2,indexf, columnf)
            # once more roundingsnto prevent some minor unrounded found
            # Appplying round method to all the columns
            # hgeo = hgeo.applymap(lambda x:round(x,d))
            # Concat total table with previous table
            hkpi = pd.concat([hkpi,hgeo],axis=1)

        return hkpi

    def market2(mkt):
        gid=mkt
        # geog are the geograhies in Mkt5 columns
        # We have to create a loop over unique values and calculate handling
        geog = db[gid].unique()
        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issue in SISH
        geog=sorted(geog)

        for g in geog:
            dbf = (db[indexf[0]]!=0)&(db[gid]==g)
            columnf = [mkt,'Month']
            hgeo = pivot(dbf, valuef1,valuef2,indexf, columnf)
            # once more roundingsnto prevent some minor unrounded found
            # Appplying round method to all the columns
            # hgeo = hgeo.applymap(lambda x:round(x,d))

        return hgeo

    # Calculation for Total MBD
    if 'Mkt1' in market_array:
        # strip away Mkt1 from array as we donot need it in the function
        market_array = [string for string in market_array if string !='Mkt1']

        hkpi = Mkt1()          #National

        # Calculating Other MBDs other then Mkt1
        for mkt in market_array:
            hkpi = market(hkpi,mkt)

    else:
        # Calculating Other MBDs other then Mkt1
        # This one is to start concatenation chain
        hkpi = market2(market_array[0])

        for mkt in market_array[1:]:
            hkpi = market(hkpi,mkt)

    # Converting indeces to columns
    # hkpi=hkpi.reset_index()

    return hkpi

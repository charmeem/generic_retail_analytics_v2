import pandas as pd
import numpy as np
import importlib
import helper as helper
importlib.reload(helper)

# General Function for all Heirarchies
def hfunc(db,kpi,geo,d,indexf,heir,brand,plist):
    # print("We are In Hierarchy")

    #As shares are calculted from absolutes we have to rename share kpi to absolutes
    if kpi == 'vol_share':
        kpi='vol_abs'
    if kpi == 'val_share':
        kpi='val_abs'
    if kpi == 'purvol_share':
        kpi='purvol_abs'
    if kpi == 'stockvol_share':
        kpi='stockvol_abs'
    if kpi == 'fwdstockvol_share':
        kpi='fwdstockvol_abs'

    # Common parameters for h pivot table
#     indexf = ['SM', 'Vendor','Brand','PS', 'SKU' ]
    aggfuncf = {kpi:np.sum}
    valuef = [kpi]

    # A pivot function to be called as needed
    def pivot(dbf, indexf, valuef, columnf, aggfuncf):
        pivot_t = pd.pivot_table(
                    db[dbf],
                   index=indexf,values=valuef, columns=columnf, aggfunc=aggfuncf,fill_value=0,
                    # margins=True, margins_name='Grand Total'
                    )
        # pivot_t.drop('Grand Total', axis=1, inplace=True, level=1)

        return pivot_t

    # Generic function to generate  Pivot
    def Total():
        #First create Total table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)
        columnf = ['Month']
        hgeo = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded values found
        hgeo[kpi] = hgeo[kpi].round(decimals=d)
        # rename kpi column
        hgeo = hgeo.rename(columns={kpi:'Total'},level=0)

        # Now create National Urbanity table- Call pivot table
        columnf = ['RC_Total_Urban_Rural','Month']
        hkpi = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hkpi[kpi] = hkpi[kpi].round(decimals=d)
        #Drop vol_abs level for concetenations later below
        hkpi.columns=hkpi.columns.droplevel(0)
        # reordering, Bring Total Urban column in the start
        order = ['Total Urban','Total Rural']
        hkpi = hkpi.reindex(order,axis=1,level=0)
        # Concat both the tables
        hkpi = pd.concat([hgeo,hkpi],axis=1)
        return hkpi

    def Regions(region,hkpi):
        #First create CP Total table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['PTC_REGION'] == region)
        columnf = ['PTC_REGION','Month']
        hgeo = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hgeo[kpi] = hgeo[kpi].round(decimals=d)
        hgeo.columns=hgeo.columns.droplevel(0)
        # Renaming columns
        hgeo = hgeo.rename(columns={region:region+' Region'},level=0)
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hgeo],axis=1)

        # Now create CP Urbanity table- Call pivot table
        columnf = ['PTC_REGION','RC_Total_Urban_Rural','Month']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hrg[kpi] = hrg[kpi].round(decimals=d)
        #Drop vol_abs level for concetenations later below
        hrg.columns=hrg.columns.droplevel([0,1])
        # reordering, Bring Total Urban column in the start
        order = ['Total Urban','Total Rural']
        hrg = hrg.reindex(order,axis=1,level=0)
        # Renaming columns
        hrg = hrg.rename(columns={'Total Urban':region+' Urban','Total Rural':region+' Rural'},level=0)
        # Concat both the tables
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def Area(city,hkpi):
        #First create Fslb Area table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['PTC_AREA_M'] == city)
        columnf = ['PTC_AREA_M','Month']
        hgeo = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hgeo[kpi] = hgeo[kpi].round(decimals=d)
        hgeo.columns=hgeo.columns.droplevel(0)
        # Renaming columns
        hgeo = hgeo.rename(columns={city:city+' Area'},level=0)
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hgeo],axis=1)
        return hkpi

    def Market(city,hkpi):
        #Next create Fslb Top10 Rural/Urban table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['RC_Top_10_Cities_ROU_Rural'] == city)
        columnf = ['RC_Top_10_Cities_ROU_Rural','Month']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hrg[kpi] = hrg[kpi].round(decimals=d)
        hrg.columns=hrg.columns.droplevel(0)
        # Renaming columns
        if city == 'Rest of Urban':
            hrg = hrg.rename(columns={city: city + ' Pakistan'},level=0)
        if city == 'LRG-Rural':
            hrg = hrg.rename(columns={city: 'Rural Large Villages'},level=0)
        if city == 'MED-Rural':
            hrg = hrg.rename(columns={city: 'Rural Medium / Small Villages'},level=0)

        hrg = hrg.rename(columns={city: city + ' Market'},level=0)
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def IRMarket(hkpi):
        #Next create Fslb Top10 Rural/Urban table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['RC_Top_10_Cities_ROU_Rural'] == 'Islamabad')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Rawalpindi')
        columnf = ['Month','RC_Top_10_Cities_ROU_Rural']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
#         hrg[kpi] = hrg[kpi].round(decimals=d)
        hrg = hrg.sum(level=1,axis=1)
        #Add new level = Total
        hrg.columns = pd.MultiIndex.from_product([['Islamabad&Rawalpindi Market'],hrg.columns])
#         hrg.to_csv('hrg.csv')
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def TenKC(hkpi):
        #Next create  Top10 Key Cities table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&((db['RC_Top_10_Cities_ROU_Rural'] == 'Faisalabad')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Gujranwala')|
        (db['RC_Top_10_Cities_ROU_Rural'] == 'Hyderabad')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Islamabad')|
        (db['RC_Top_10_Cities_ROU_Rural'] == 'Karachi')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Lahore')|
        (db['RC_Top_10_Cities_ROU_Rural'] == 'Multan')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Peshawar')|
        (db['RC_Top_10_Cities_ROU_Rural'] == 'Quetta')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Rawalpindi'))

        columnf = ['Month','RC_Top_10_Cities_ROU_Rural']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
#         hrg[kpi] = hrg[kpi].round(decimals=d)
        hrg = hrg.sum(level=1,axis=1)
        #Add new level = Total
        hrg.columns = pd.MultiIndex.from_product([['10 Key Cities (Combined)'],hrg.columns])
#         hrg.to_csv('hrg.csv')
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def FourMetros(hkpi):
         #Next create 4Metropoliton  Cities table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&((db['RC_Top_10_Cities_ROU_Rural'] == 'Islamabad')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Karachi')|
        (db['RC_Top_10_Cities_ROU_Rural'] == 'Lahore')|(db['RC_Top_10_Cities_ROU_Rural'] == 'Rawalpindi'))

        columnf = ['Month','RC_Top_10_Cities_ROU_Rural']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
#         hrg[kpi] = hrg[kpi].round(decimals=d)
        hrg = hrg.sum(level=1,axis=1)
        #Add new level = Total
        hrg.columns = pd.MultiIndex.from_product([['Four Metros (K.L.I.R.)'],hrg.columns])
#         hrg.to_csv('hrg.csv')
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def Province(province,hkpi):
        #First create Province Total table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['PROVINCE'] == province)
        columnf = ['PROVINCE','Month']
        hgeo = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hgeo[kpi] = hgeo[kpi].round(decimals=d)
        hgeo.columns=hgeo.columns.droplevel(0)
        # Renaming columns
#         hgeo = hgeo.rename(columns={province:province+' Province'},level=0)
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hgeo],axis=1)

        # Now create Province Urbanity table- Call pivot table
        columnf = ['PROVINCE','RC_Total_Urban_Rural','Month']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        hrg[kpi] = hrg[kpi].round(decimals=d)
        #Drop vol_abs level for concetenations later below
        hrg.columns=hrg.columns.droplevel([0,1])
        # reordering, Bring Total Urban column in the start
        order = ['Total Urban','Total Rural']
        hrg = hrg.reindex(order,axis=1,level=0)
        # Renaming columns
        hrg = hrg.rename(columns={'Total Urban':'Urban '+ province,'Total Rural':'Rural '+ province},level=0)
        # Concat both the tables
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def SindNK(hkpi):
        province = 'Sind'
        #First create Province Total table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['PROVINCE'] == province)&(db['RC_Top_10_Cities_ROU_Rural'] != 'Karachi')
        columnf = ['PROVINCE','Month']
        hgeo = pivot(dbf, indexf, valuef, columnf, aggfuncf)

        # once more roundingsnto prevent some minor unrounded found
        hgeo[kpi] = hgeo[kpi].round(decimals=d)
        hgeo.columns=hgeo.columns.droplevel(0)

        # Renaming columns
        hgeo = hgeo.rename(columns={province:'Sindh without Karachi'},level=0)

        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hgeo],axis=1)

        # NOW CREATE Province Urbanity table BUT ONLY URBAN- Call pivot table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&(db['PROVINCE'] == province)&(db['RC_Top_10_Cities_ROU_Rural'] != 'Karachi')&(db['RC_Total_Urban_Rural'] == 'Total Urban')

        columnf = ['PROVINCE','RC_Total_Urban_Rural','Month']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)

        # once more roundingsnto prevent some minor unrounded found
        hrg[kpi] = hrg[kpi].round(decimals=d)

        #Drop vol_abs level for concetenations later below
        hrg.columns=hrg.columns.droplevel([0,1])

        # Renaming column
        hrg = hrg.rename(columns={'Total Urban':'Urban Sindh without Karachi'},level=0)

        # Concat both the tables
        hkpi = pd.concat([hkpi,hrg],axis=1)

        return hkpi

    def KPAJK(hkpi):
         #Next create 4Metropoliton  Cities table
        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&((db['PROVINCE'] == 'KPK')|(db['PROVINCE'] == 'AJK'))

        columnf = ['Month','PROVINCE']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
#         hrg[kpi] = hrg[kpi].round(decimals=d)
        hrg = hrg.sum(level=1,axis=1)
        #Add new level = Total
        hrg.columns = pd.MultiIndex.from_product([['KPK(incl AJK)'],hrg.columns])
#         hrg.to_csv('hrg.csv')
        # Concat total table with previous table
        hkpi = pd.concat([hkpi,hrg],axis=1)

        # Now create Province Urbanity table- Call pivot table
        columnf = ['RC_Total_Urban_Rural','Month','PROVINCE']
        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
#         hrg[kpi] = hrg[kpi].round(decimals=d)

        # Sum of Provinces along y axis
        hrg = hrg.sum(level=[1,2],axis=1)
        # reordering, Bring Total Urban column in the start
        order = ['Total Urban','Total Rural']
        hrg = hrg.reindex(order,axis=1,level=0)
        # Renaming columns
        hrg = hrg.rename(columns={'Total Urban':'Urban KPK(incl AJK)','Total Rural':'Rural KPK(incl AJK)'},level=0)
        # Concat both the tables
        hkpi = pd.concat([hkpi,hrg],axis=1)
        return hkpi

    def Shopper(tcode,hkpi):

        if tcode=='t1':
            dbt = ((db['shop_type'] == 'Departmental Store')|(db['shop_type'] == 'Departmental Store/Super Markets')|
            (db['shop_type'] == 'General Store')|(db['shop_type'] == 'General-Medical Store')|
            (db['shop_type'] == 'Kiryana Store')|(db['shop_type'] == 'Super Markets'))

        if tcode == 't2':
            dbt = ((db['shop_type'] == 'Kiosk/Hawker')|(db['shop_type'] == 'Pan/Cigarette Shop')|
                  (db['shop_type'] == 'Petro Mart'))

        if tcode == 't3':
            dbt = ((db['shop_type'] == 'Canteen')|(db['shop_type'] == 'Corner / Snack Shop')|
                  (db['shop_type'] == 'Eating Place / High Way Hotel'))


        # CREATE Channnel Urbanity table BUT ONLY URBAN by Calling pivot table

        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&        (db['RC_Total_Urban_Rural'] == 'Total Urban') & dbt

        columnf = ['RC_Total_Urban_Rural','Month','shop_type']

        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)

        # once more roundingsnto prevent some minor unrounded found
        hrg[kpi] = hrg[kpi].round(decimals=d)

        # Sum of Channels along y axis
        hrg = hrg.sum(level=[1,2],axis=1)

        # Renaming column
        if tcode=='t1':
            hrg = hrg.rename(columns={'Total Urban':'Urban Grocery'},level=0)
        if tcode=='t2':
            hrg = hrg.rename(columns={'Total Urban':'Urban Pay & Go'},level=0)
        if tcode=='t3':
            hrg = hrg.rename(columns={'Total Urban':'Urban Entertainment'},level=0)

        # Concat both the tables
        hkpi = pd.concat([hkpi,hrg],axis=1)

        return hkpi

    def Trade(tcode,hkpi):

        if tcode == 't4':
            dbt = ((db['shop_type'] == 'Departmental Store')|(db['shop_type'] == 'General Store')|
                  (db['shop_type'] == 'Departmental Store/Super Markets')|(db['shop_type'] == 'Super Markets')|(db['shop_type'] == 'General-Medical Store'))

        if tcode == 't5':
            dbt = (db['shop_type'] == 'Kiryana Store')
        if tcode == 't6':
            dbt = ((db['shop_type'] == 'Pan/Cigarette Shop'))

        if tcode == 't7':
            dbt = ((db['shop_type'] == 'Corner / Snack Shop')|(db['shop_type'] == 'Kiosk/Hawker')|
                  (db['shop_type'] == 'Petro Mart'))

        if tcode == 't8':
            dbt = ((db['shop_type'] == 'Canteen')|(db['shop_type'] == 'Eating Place / High Way Hotel'))

        # CREATE Channnel Urbanity table BUT ONLY URBAN by Calling pivot table

        dbf = (db['Brand']!=0)&(db['PS']!=0)&(db['SKU']!=0)&(db['SM']!=0)&(db['Vendor']!=0)&        (db['RC_Total_Urban_Rural'] == 'Total Urban') & dbt

        columnf = ['RC_Total_Urban_Rural','Month','shop_type']

        hrg = pivot(dbf, indexf, valuef, columnf, aggfuncf)

        # once more roundingsnto prevent some minor unrounded found
        hrg[kpi] = hrg[kpi].round(decimals=d)

        # Sum of Channels along y axis
        hrg = hrg.sum(level=[1,2],axis=1)

        # Renaming column
        if tcode=='t4':
            hrg = hrg.rename(columns={'Total Urban':'Urban Gen/Gen-Med Store with DPS'},level=0)
        if tcode=='t5':
            hrg = hrg.rename(columns={'Total Urban':'Urban Kiryana Store'},level=0)
        if tcode=='t6':
            hrg = hrg.rename(columns={'Total Urban':'Urban Pan Shop'},level=0)
        if tcode=='t7':
            hrg = hrg.rename(columns={'Total Urban':'Urban Kiosks/Haw/Corner St./Petros'},level=0)
        if tcode=='t8':
            hrg = hrg.rename(columns={'Total Urban':'Urban Rest / Canteens / Hotels'},level=0)

        # Concat both the tables
        hkpi = pd.concat([hkpi,hrg],axis=1)

        return hkpi

    if 'Total' in geo:
        hkpi = Total()

    if 'CP' in geo:
        hkpi= Regions('CP',hkpi)

    if 'Faisalabad' in geo:
        hkpi = Area('Faisalabad',hkpi)
        hkpi = Market('Faisalabad',hkpi)

    if 'Gujranwala' in geo:
        hkpi = Area('Gujranwala',hkpi)
        hkpi = Market('Gujranwala',hkpi)

    if 'Jhang' in geo:
        hkpi = Area('Jhang',hkpi)

    if 'Lahore' in geo:
        hkpi = Area('Lahore',hkpi)
        hkpi = Market('Lahore',hkpi)

    if 'SP' in geo:
        hkpi= Regions('SP',hkpi)

    if 'Bahawalpur' in geo:
        hkpi = Area('Bahawalpur',hkpi)

    if 'D.G.Khan' in geo:
        hkpi = Area('D.G.Khan',hkpi)

    if 'Multan' in geo:
        hkpi = Area('Multan',hkpi)
        hkpi = Market('Multan',hkpi)

    if 'Sahiwal' in geo:
        hkpi = Area('Sahiwal',hkpi)

    if 'NR' in geo:
        hkpi= Regions('NR',hkpi)

    if 'Islarea' in geo:
        hkpi = Area('Islamabad',hkpi)

    if 'islrwlmarket' in geo:
        hkpi = IRMarket(hkpi)

    if 'islmarket' in geo:
        hkpi = Market('Islamabad',hkpi)

    if 'rwlmarket' in geo:
        hkpi = Market('Rawalpindi',hkpi)

    if 'Sargodha' in geo:
        hkpi = Area('Sargodha',hkpi)

    if 'North A' in geo:
        hkpi = Area('Northern Areas',hkpi)

    if 'Peshawar' in geo:
        hkpi = Area('Peshawar',hkpi)
        hkpi = Market('Peshawar',hkpi)

    if 'Jhelum' in geo:
        hkpi = Area('Jhelum',hkpi)

    #-----------

    if 'S&B' in geo:
        hkpi= Regions('S&B',hkpi)

    if 'Quetta' in geo:
        hkpi = Area('Quetta',hkpi)
        hkpi = Market('Quetta',hkpi)

    if 'Hyderabad' in geo:
        hkpi = Area('Hyderabad',hkpi)
        hkpi = Market('Hyderabad',hkpi)

    if 'Karachi' in geo:
        hkpi = Area('Karachi',hkpi)
        hkpi = Market('Karachi',hkpi)

    if 'Nawab Shah' in geo:
        hkpi = Area('Nawab Shah',hkpi)

    if 'Sukkur' in geo:
        hkpi = Area('Sukkur',hkpi)
    #----

    if 'Rest of Urban' in geo:
        hkpi = Market('Rest of Urban',hkpi)

    if 'LRG-Rural' in geo:
        hkpi = Market('LRG-Rural',hkpi)

    if 'MED-Rural' in geo:
        hkpi = Market('MED-Rural',hkpi)

    if '10KC' in geo:
        hkpi = TenKC(hkpi)

    if '4Metros' in geo:
        hkpi = FourMetros(hkpi)

    #---

    if 'Punjab' in geo:
        hkpi= Province('Punjab',hkpi)

    if 'Sind' in geo:
        hkpi= Province('Sind',hkpi)

    if 'Sind NK' in geo:
        hkpi= SindNK(hkpi)

    if 'KPAJK' in geo:
        hkpi= KPAJK(hkpi)

    if 'Balochistan' in geo:
        hkpi= Province('Balochistan',hkpi)

    #---------

    if 'Urban Grocery' in geo:
        hkpi = Shopper('t1',hkpi)

    if 'Urban Pay & Go' in geo:
        hkpi = Shopper('t2',hkpi)

    if 'Urban Entertainment' in geo:
        hkpi = Shopper('t3',hkpi)

    if 'DPS' in geo:
        hkpi = Trade('t4',hkpi)

    if 'Kiryana' in geo:
        hkpi = Trade('t5',hkpi)

    if 'Pan' in geo:
        hkpi = Trade('t6',hkpi)

    if 'Kiosk' in geo:
        hkpi = Trade('t7',hkpi)

    if 'Hotels' in geo:
        hkpi = Trade('t8',hkpi)

    ##
    # Common Routines for all the Geographies
    # Converting indeces to columns
#     hkpi=hkpi.reset_index()

    def h5func(hkpi):

        # Create New Grand Total Row containing sum of all brands
        hkpi.loc['Grand Total'] = hkpi.sum(numeric_only=True).round(decimals=d)

        # Filter only the selected brand and the grand row
        hkpi = hkpi.loc[[brand,'Grand Total']]

        # Rename Grand Total row index to 'Category'
        hkpi = hkpi.rename({hkpi.index[-1]:'Category'})

        # Bring Category ( Grand Total) on the top of brand row
        hkpi = hkpi.reindex(['Category',brand])

        # Rename Brand 'House of Rothman' to 'Gold Flake(Ba)' as per requirement
        hkpi = hkpi.rename({brand:"Gold Flake(Ba)"})

        # Now replace multilevel column name 'Month' with blank
        # As there are two level one blank and one Month we have to give both in orfder to set one
        hkpi = hkpi.rename_axis(['',''],axis=1)

        return hkpi

    # Calling Custom Function
    hchy=h5func(hkpi)

    return hchy

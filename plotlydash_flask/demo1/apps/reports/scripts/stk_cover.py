
# This function is used to generate report for OOS COST

import numpy as np
import importlib

# Importing supporting scripts
import helper 
importlib.reload(helper)
import hierchy
importlib.reload(hierchy)
import h_filter_brand_pcode 
importlib.reload(h_filter_brand_pcode)
import hierchy_hand 
importlib.reload(hierchy_hand)
import hierchy_price 
importlib.reload(hierchy_price)
import kpis 
importlib.reload(kpis)
import calculations
importlib.reload(calculations)

def main(dbm,geo,d,heir,indexf,hlist,market_array):
    kpia=['vol_abs','stockvol_abs']
    for kpi in kpia:
        # print('KPI',kpi)

        db = calculations.calcs(dbm,kpi)
        # db.to_csv('db.csv')
        if 'Mkt1' in market_array:
            market_array2 = [string for string in market_array if string !='Mkt1']
        else:
            market_array2 = market_array

        # Calling function to genertae new rounded base table
        db = helper.rounded_vol_db(db,d,kpi,hlist,market_array2)

        # Converting indeces into columns
        db=db.reset_index()


        # Call heirarchy Function to generate pivot
        # OOS Cover days (Million PKR)
        #
        # Formula = (OOS Volume / Sale Volume * 30.5
        # 1. Getting OOS Volume
        if kpi == 'vol_abs':
            vol_v = hierchy.hfunc(db,kpi,geo,d,indexf,heir,market_array)
            # To avoid DivisionByZero error- replacing 0 by nan
            vol_v = vol_v.replace({'0':np.nan,'0.0':np.nan,0:np.nan,0.0:np.nan})

        #2.  Getting Weighted Handling
        elif kpi == 'stockvol_abs':
            oos_v = hierchy.hfunc(db,kpi,geo,d,indexf,heir,market_array)


    # oos cover days
    hchy = oos_v/vol_v*30.5
    # Convert back nan to 0
    hchy = hchy.replace(np.nan, 0, regex=True)

    return hchy

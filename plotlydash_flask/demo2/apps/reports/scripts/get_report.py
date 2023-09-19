import pandas as pd
import numpy as np
import importlib
from legends import geo
import hierchy
importlib.reload(hierchy)
import hierchy_hand
importlib.reload(hierchy_hand)
import hierchy_price
importlib.reload(hierchy_price)
import hierchy_priceU
importlib.reload(hierchy_priceU)
import sppd
importlib.reload(sppd)
import stk_cover as stk_cover
importlib.reload(stk_cover)

# from apps.reports.scripts.legends import geo
# import apps.reports.scripts.hierchy as hierchy
# importlib.reload(hierchy)
# import apps.reports.scripts.hierchy_hand as hierchy_hand
# importlib.reload(hierchy_hand)
# import apps.reports.scripts.hierchy_price as hierchy_price
# importlib.reload(hierchy_price)
# import apps.reports.scripts.hierchy_priceU as hierchy_priceU
# importlib.reload(hierchy_priceU)
# import apps.reports.scripts.sppd as sppd
# importlib.reload(sppd)
# import apps.reports.scripts.stk_cover as stk_cover
# importlib.reload(stk_cover)
#-----------------------------------------------
#  Function to Call respective FACTS scripts
#   to generte Reports
#-----------------------------------------------

# Helper function to Create SISH_Volume column only for SISH calculations
# Help taken from sish_simulation.csv provided by Asad Ali Khan

def sish_vol(dbm):
    aggfuncf = {'vol_abs':np.sum}
    valuef = ['vol_abs']
    # indexf = ['SM', 'Vendor','Brand','PS', 'SKU' ]
    indexf = ['Month','shop_code']
    pivot_v = pd.pivot_table(
                dbm,
               index=indexf,values=valuef, aggfunc=aggfuncf,fill_value=0,
                )
    # Convert index to columns
    pivot_v = pivot_v.reset_index()
    pivot_v = pivot_v.rename(columns={'vol_abs':'SISH_Volume'})
    dbm = pd.merge(dbm,pivot_v)
    return dbm
    
def get_report_func(db,dbm,kpi,d,indexf,hr,market_array):
    
    #NUM HANDLING- WT. HANDLING - OOS HANDLING - OOSWT. HANDLING - HIH
    if kpi in ['num_hand','wt_hand','oos_hand','ooswt','hih','ooscost','sppd']:                  #Refactor

        hchy = hierchy_hand.hfunc(db,kpi,geo,d,indexf,hr,market_array)

    # SELLING PRICE RETAIL for Pack
    elif kpi == 'sale_price':
        hchy = hierchy_price.hfunc(db,geo,d,hr,indexf,market_array)*10000

    # Retail selling price for unit
    elif kpi == 'price_stick':
        # kpi='sale_price'
        hchy = hierchy_priceU.hfunc(db,geo,d,hr,indexf,market_array)/10000


    # SISH
    # sish = sales volabs total/sales volabs for PTC only*100
    elif kpi == 'sish':
        #Calculate Numerator
        #
        # Since sish numerator is same as volume absolute
        kpi = 'vol_abs'
        # db.to_csv('dbb.csv')
        hchy = hierchy.hfunc(db,kpi,geo,d,indexf,hr,market_array)

        # Calculating denominator for sish
        #
        #setting back kpi
        kpi = 'sish'
        # Calling function to Create sish volume colume in the db
        db = sish_vol(dbm)

        hchy_sish = hierchy_hand.hfunc(db,kpi,geo,d,indexf,hr,market_array)
        # To avoid DivisionByZero error- replacing 0 by nan
        hchy_sish = hchy_sish.replace({'0':np.nan,'0.0':np.nan,0:np.nan,0.0:np.nan})

        # Calculate SISH in absolute multiplied by million
        # one Way
        # hchy = hchy/hchy_sish
        # another Way
        hchy=hchy.div(hchy_sish,axis=0)

        # Appplying round method to all the columns
        # hchy = hchy.applymap(lambda x:round(x,d))

        # Convert back nan to 0
        hchy = hchy.replace(np.nan, 0, regex=True)

    # Taking seperate path for ooscover days KPI
    elif kpi == 'stock_cover':
        hlist=indexf
        hchy = stk_cover.main(dbm,geo,d,hr,indexf,hlist,market_array)

    # Sales per point of distribution


    # HANDLING REST OF THE KPIS
    else:
        hchy = hierchy.hfunc(db,kpi,geo,d,indexf,hr,market_array)

    return hchy

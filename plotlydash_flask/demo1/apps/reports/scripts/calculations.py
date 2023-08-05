# This File Along with kpi.py is Used to calculate Different Facts/KPIs
#
#  NOTE: Might not be needed in future as DP already got finalized values from Stat.
#

import pandas as pd
import numpy as np
import importlib
import kpis
importlib.reload(kpis)


def calcs(dbm,kpi):
    print("KPI",kpi)

    # Calculate Sale Although the existing Sales is also same
    # db['Sale_new'] = db['OpeningStock']+db['Purchase']-db['Stk1']-db['Stk2']

    #Creating raw sales on cusomer requirement
#     db['Raw_Sale'] = db.Sale*db.Sticks

    # Calculating KPIs

    # Sales_items
    if (kpi=='sales_items'):
        db=kpis.s_items(dbm)
        
    #Sale price
    if (kpi=='sale_price')|(kpi=='price_stick'):
        db=kpis.sale_price(dbm)

    #Volume absolute
    if (kpi=='vol_abs')|(kpi=='vol_share')|(kpi=='saleleg')|(kpi=='shareleg')|(kpi=='sish'):
        db=kpis.new_vol(dbm)
        # dbm['vol_abs'] = dbm['Volume']
        # db=dbm


    #Value absolute
    if (kpi=='val_abs')|(kpi=='val_share'):
        # For time being not using new calculation rather using existing Value colume
        db=kpis.new_val(dbm)
        # dbm['val_abs'] = dbm['Value']
        # db=dbm

    #PurchASE vOLUME
    if (kpi=='purvol_abs')|(kpi=='purvol_share'):
        db=kpis.new_purchasevol(dbm)

    #Stocks vOLUME
    if (kpi=='stockvol_abs')|(kpi=='stockvol_share'):
        db=kpis.new_stockvol(dbm)

    #Forward Stocks vOLUME
    if (kpi=='fwdstockvol_abs')|(kpi=='fwdstockvol_share'):
        db=kpis.new_fwdstockvol(dbm)

    # OOS cost
    if (kpi == 'ooscost'):
        db=kpis.new_vol(dbm)
        db=kpis.new_val(dbm)


    db = db.fillna(0)
#     db.to_csv('db.csv')
    return db

# Following function ONLY for historical reason and are not used
def Acv_pf_cig(db):
    # cat_filter = db.Cat.isin(cat_array) # there is only one subcategory for cigarette
    s_acv = pd.pivot_table(
                db,
                 index=[
                     'WAVE',
                     'Cat',
                    'Merged_Cell',
                     'Store Code',
                     'p_p_code'
                 ],
                values=[
                    'Shop_ACV_Monthly',
                ],
                aggfunc={
                    'Shop_ACV_Monthly':np.max,
                })
    s_acv.reset_index(inplace=True)
    s_acv.drop_duplicates(subset =['WAVE','Store Code'
                                   ,'Cat'
                                  ], keep='first',inplace=True)
#     s_acv.to_csv('s_acvcat.csv')
    # try:

    s_acv_sum = pd.pivot_table(
                s_acv,
                 index=[
                     'WAVE',
                     'Cat',
                    'Merged_Cell',
                 ],
                values=[
                    'Shop_ACV_Monthly',
                ],
                aggfunc={
                    'Shop_ACV_Monthly':np.sum,
                })
    # except:
    #     print('OOPs something went wrong, please check your db')
    #     sys.exit()
#     s_acv_sum.to_csv('s_acvcat_sum.csv')
    cell_acv = pd.pivot_table(
                db[(db[filter]==0)],  # bigdata
                 index=[
                     'WAVE',
                     'Cat',
                    'Merged_Cell'
                 ],
                values=[
                    'Cell Calib ACV',
                ],
                aggfunc={
                    'Cell Calib ACV':np.max,
                })

    acv_pf_n = pd.concat([cell_acv,s_acv_sum], axis=1, keys=['cell_acv','s_acv_sum'])
    acv_pf_n.columns=acv_pf_n.columns.droplevel(0)

    acv_pf_n['acv_pf'] = acv_pf_n['Cell Calib ACV']/acv_pf_n['Shop_ACV_Monthly']
    acv_pf_n['acv_pf'] = acv_pf_n['acv_pf'].replace(np.inf,np.nan)

#     acv_pf_n.to_csv('acv_pf_cat2.csv')

    return acv_pf_n



# # Calculate volumes
# db = calcs(db)

# Store new db
# db.to_csv('../../../../electron/pydem_dev/engine/logs/db_new.csv')

## This is a File contining routines to Calculate different FACTS/KPIs

# import hand             # Routine to calcukate handlings
# importlib.reload(hand)

# Sales Items
# = raw sales * ACV Proj Factor
def s_items(dbm):
    dbm['Sale_new'] = dbm['OpeningStock']+dbm['Purchase']-dbm['Stk1']-dbm['Stk2']
    dbm['sales_items'] = (dbm['ACV Proj Factor']*dbm['Sale_new'])
    
    return dbm

# New coliumn = Sale of SKU * price of SKu
def sale_price(dbm):
    dbm['sale_price']= dbm['Sale_new']*dbm['Price']
    return dbm

# Function for Sales Volume Calculation
def new_vol(dbm):
    # dbm.to_csv('dbm.csv')
    if 'vol_abs' in dbm.columns:
        dbm.drop(['vol_abs'], axis=1, inplace=True)
        #create absolute volume column as well
        dbm['vol_abs'] = (dbm['ACV Proj Factor']*dbm['Sale_new']*dbm['Weights'])
    else:
        dbm['vol_abs'] = (dbm['ACV Proj Factor']*dbm['Sale_new']*dbm['Weights'])
    # dbm.to_csv('db22.csv')
    return dbm

# Function for Sales Value Calculation
def new_val(dbm):

    if 'val_abs' in dbm.columns:
        dbm.drop(['val_abs'], axis=1, inplace=True)
        #create absolute volume column as well
        dbm['val_abs'] = (dbm['ACV Proj Factor']*dbm['Sale_new']*dbm['Price'])
    else:
        dbm['val_abs'] = (dbm['ACV Proj Factor']*dbm['Sale_new']*dbm['Price'])
    return dbm

# Function for Purchase Volume Calculation
def new_purchasevol(dbm):
    if 'purvol_abs' in dbm.columns:
        dbm.drop(['purvol_abs'], axis=1, inplace=True)
        #create absolute volume column as well
        dbm['purvol_abs'] = (dbm['ACV Proj Factor']*dbm['Purchase']*dbm['Weights'])
    else:
        dbm['purvol_abs'] = (dbm['ACV Proj Factor']*dbm['Purchase']*dbm['Weights'])

    return dbm

# Function for Stocks Volume Calculation
def new_stockvol(dbm):
    if 'stockvol_abs' in dbm.columns:
        dbm.drop(['stockvol_abs'], axis=1, inplace=True)
        #create absolute volume column as well
        dbm['stockvol_abs'] = (dbm['ACV Proj Factor']*(dbm['Stk1']+dbm['Stk2'])*dbm['Weights'])
    else:
        dbm['stockvol_abs'] = (dbm['ACV Proj Factor']*(dbm['Stk1']+dbm['Stk2'])*dbm['Weights'])

    return dbm

# Function for Forward Stocks Volume Calculation
def new_fwdstockvol(dbm):
    if 'fwdstockvol_abs' in dbm.columns:
        dbm.drop(['fwdstockvol_abs'], axis=1, inplace=True)
        #create absolute volume column as well
        dbm['fwdstockvol_abs'] = (dbm['ACV Proj Factor']*dbm['Stk1']*dbm['Weights'])
    else:
        dbm['fwdstockvol_abs'] = (dbm['ACV Proj Factor']*dbm['Stk1']*dbm['Weights'])
    return dbm

#Neumeric HAndling
    if 'numhand%' in dbm.columns:
        dbm.drop(['numhand%'], axis=1, inplace=True)
        

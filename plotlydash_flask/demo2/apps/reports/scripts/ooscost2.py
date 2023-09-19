import pandas as pd
import numpy as np


# General Funcion to Calculate Numeric Handliing KPI
# Function to calculate Denominator
def value(db,gid,gid2,dbf,columnf):

    # Check if this is urbanity
    if gid2=='RC_Total_Urban_Rural':
        indexf = [gid2]
    else:
        indexf = [gid]

    val = pd.pivot_table(
                    db[dbf],
                    index=indexf,
                    values=['val_abs'],
                    columns=columnf,
                    aggfunc={
                        'val_abs':np.sum,
                        },
                    # dropna=False
                    )
    return val
def value_cat(db,gid,gid2,dbf,columnf):

    # Check if this is urbanity
    if gid2=='RC_Total_Urban_Rural':
        indexf = [gid2]
    else:
        indexf = [gid]

    val = pd.pivot_table(
                    db[dbf],
                    # index=indexf,
                    values=['val_abs'],
                    columns=columnf,
                    aggfunc={
                        'val_abs':np.sum,
                        },
                    # dropna=False
                    )
    return val

def value_mix(db,gid,gid2,dbf,columnf):

    val = pd.pivot_table(
                    db[dbf],
                    values=['val_abs'],
                    columns=columnf,
                    aggfunc={
                        'val_abs':np.sum,
                        },
                    # dropna=False
                    )
    return val

# Special deno function for Total Geogrphy id
def value_nat(db,dbf,columnf):
    # db.to_csv('db.csv')
    val = pd.pivot_table(
                    db[dbf],
                    # index=indexf,
                    values=['val_abs'],
                    columns=columnf,
                    aggfunc={
                        'val_abs':np.sum,
                        },
                    # dropna=False
                    )

    #As all columns has same value we take single value to be used as denominator below
    # deno=sm_s_pf.iloc[0,0]
    return val


# Function to calculate oos volume
def voloos(db,dbf,indexf1,indexf2,columnf,hlevel):
    if hlevel == 'SKU':
        volo1 = pd.pivot_table(
                    db[dbf&(db.CS_Stock == 0)],
                    index=indexf1,
                    # columns=columnf,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.max},
                    )
        volo = pd.pivot_table(
                    volo1,
                    index=indexf2,
                    columns=columnf,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.sum},
                    )
    else:
        smch1 = pd.pivot_table(
                    db[dbf],
                    index=indexf1,
                    values=['proj_vol','CS_Stock'],
                    aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                    )

        # Redefining dbf to get stores with no CS_Stock
        dbf = (smch1.CS_Stock == 0)
        volo = pd.pivot_table(
                    smch1[dbf],
                    index=indexf2,
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )

    return volo

def voloosnat(db,dbf,indexf1,columnf,hlevel):
    if hlevel == 'SKU':
        volo1 = pd.pivot_table(
                    db[dbf&(db.CS_Stock == 0)],
                    index=indexf1,
                    # columns=columnf,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.max},
                    )

        volo = pd.pivot_table(
                    volo1,
                    # index=indexf2,
                    columns=columnf,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.sum},
                    )
    else:
        smch1 = pd.pivot_table(
                    db[dbf],
                    index=indexf1,
                    values=['proj_vol','CS_Stock'],
                    aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                    )

        # Redefining dbf to get stores with no CS_Stock
        dbf = (smch1.CS_Stock == 0)
        volo = pd.pivot_table(
                    smch1[dbf],
                    # index=indexf2,
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )

    return volo

# Function to calculate oos volume for special geographies
def voloos_mix(db,dbf,indexf,columnf,level):
    if level == 'SKU':
        volo1 = pd.pivot_table(
                    db[dbf&(db.CS_Stock == 0)],
                    index=indexf,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.max},
                    )
        volo = pd.pivot_table(
                    volo1,
                    # index=indexf,
                    columns=columnf,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.sum},
                    )
    else:
        smch1 = pd.pivot_table(
                    db[dbf],
                    index=indexf,
                    values=['proj_vol','CS_Stock'],
                    aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                    )

        # Redefining dbf to get stores with no CS_Stock
        dbf = (smch1.CS_Stock == 0)
        volo = pd.pivot_table(
                    smch1[dbf],
                    # index=indexf2,
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )

    return volo

# Function to calculate normal volume
def volume(db,dbf,indexf1,indexf2,columnf):
    vol1 = pd.pivot_table(
                db[dbf&(db.CS_Stock > 0)],
                index=indexf1,
                # columns=columnf2,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )
    vol = pd.pivot_table(
                vol1,
                index=indexf2,
                columns=columnf,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.sum},
                )
    return vol

def volume_cat(db,dbf,indexf1,indexf2,columnf):
    vol1 = pd.pivot_table(
                db[dbf&(db.CS_Stock > 0)],
                index=indexf1,
                # columns=columnf2,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )
    vol = pd.pivot_table(
                vol1,
                # index=indexf2,
                columns=columnf,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.sum},
                )
    return vol

def volumenat(db,dbf,indexf1,columnf):
    vol1 = pd.pivot_table(
                db[dbf&(db.CS_Stock > 0)],
                index=indexf1,
                # columns=columnf2,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )
    vol = pd.pivot_table(
                vol1,
                # index=indexf2,
                columns=columnf,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.sum},
                )
    return vol

def volume_mix2(db,dbf,columnf2,indexf):
    vol1 = pd.pivot_table(
                db[dbf&(db.CS_Stock > 0)],
                index=indexf,
                values=['proj_vol'],
                # columns=columnf2,
                aggfunc={'proj_vol':np.sum},
                )
    return vol1
# Function to calculate normal volume for special geographies
def volume_mix(db,dbf,indexf,columnf):
    vol1 = pd.pivot_table(
                db[dbf&(db.CS_Stock > 0)],
                index=indexf,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )

    vol = pd.pivot_table(
                vol1,                          # Note : no filter is used here
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )
    return vol


# Functions for urban nat
# Function to calculate normal volume
def volumeunat(db,dbf,indexf1,columnf,gid2):
    vol1 = pd.pivot_table(
                db[dbf&(db.CS_Stock > 0)],
                index=indexf1,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )
    vol = pd.pivot_table(
                vol1,                          # Note : no filter is used here
                index=[gid2],
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )
    return vol

# Function to calculate normal volume
def voloosunat(db,dbf,indexf1,columnf,gid2,level):
    if level == 'SKU':
        vol1 = pd.pivot_table(
                    db[dbf&(db.CS_Stock == 0)],
                    index=indexf1,
                    values=['proj_vol'],
                    aggfunc={'proj_vol':np.max},
                    )
        vol = pd.pivot_table(
                    vol1,                          # Note : no filter is used here
                    index=[gid2],
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )
    else:
        smch1 = pd.pivot_table(
                    db[dbf],
                    index=indexf1,
                    values=['proj_vol','CS_Stock'],
                    aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                    )

        # Redefining dbf to get stores with no CS_Stock
        dbf = (smch1.CS_Stock == 0)
        vol = pd.pivot_table(
                    smch1[dbf],
                    index=[gid2],
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )

    return vol

# Functions for Ctaegory handling
def voloos_cat(db,dbf,indexf1,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['proj_vol','CS_Stock'],
                aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                )

    # Redefining dbf to get stores with no CS_Stock
    dbf = (smch1.CS_Stock == 0)
    numero = pd.pivot_table(
                smch1[dbf],
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )

    return numero

import pandas as pd
import numpy as np
import importlib


# Function to calculate oos volume
def vols(db,dbf,indexf1,indexf2,columnf,level):
    if level == 'SKU':
        volo1 = pd.pivot_table(
                    db[dbf],
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

        volo = pd.pivot_table(
                    smch1[dbf],
                    index=indexf2,
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )

    return volo

def volsnat(db,dbf,indexf1,columnf,level):
    volo = pd.pivot_table(
                db[dbf],
                index=indexf1,
                columns=columnf,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )

    return volo

# Function to calculate oos volume for special geographies
def vols_mix(db,dbf,indexf,columnf,level):
    if level == 'SKU':
        volo1 = pd.pivot_table(
                    db[dbf],
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
                db[dbf],
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
                db[dbf],
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
                db[dbf],
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
                db[dbf],
                index=indexf,
                values=['proj_vol'],
                # columns=columnf2,
                aggfunc={'proj_vol':np.sum},
                )
    return vol1
# Function to calculate normal volume for special geographies
def volume_mix(db,dbf,indexf,columnf):
    vol1 = pd.pivot_table(
                db[dbf],
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
                db[dbf],
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
def volsunat(db,dbf,indexf1,columnf,gid2,level):
    if level == 'SKU':
        vol1 = pd.pivot_table(
                    db[dbf],
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

        vol = pd.pivot_table(
                    smch1[dbf],
                    index=[gid2],
                    values=['proj_vol'],
                    columns=columnf,
                        aggfunc={'proj_vol':np.sum},
                    )

    return vol

# Functions for Ctaegory handling
def vols_cat(db,dbf,indexf1,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['proj_vol','CS_Stock'],
                aggfunc={'proj_vol':np.max,'CS_Stock':np.sum},
                )

    numero = pd.pivot_table(
                smch1[dbf],
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )

    return numero

import pandas as pd
import numpy as np
import sys
import tkinter as tk
from tkinter import messagebox


# General Funcion to Calculate Numeric Handliing KPI
# Function to calculate Denominator
def denomin(db,gid,gid2,dbf,columnf):

    # Check if this is urbanity
    if gid2=='RC_Total_Urban_Rural':
        indexf = [gid2]
    else:
        indexf = [gid]

    try:
        deno = pd.pivot_table(
                    db[dbf],
                    index=indexf,
                    values=['Volume'],
                    columns=columnf,
                    aggfunc={
                        'Volume':np.sum,
                        },
                    dropna=False
                    )
    except:
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning('alert title', gid+' Column is missing')
        sys.exit()

    return deno

def denomin_mix(db,gid,gid2,dbf,columnf):

    deno = pd.pivot_table(
                    db[dbf],
                    values=['Volume'],
                    columns=columnf,
                    aggfunc={
                        'Volume':np.sum,
                        },
                    dropna=False
                    )
    return deno

# Special deno function for National Geogrphy id
def denomin_nat(db,columnf):

    deno = pd.pivot_table(
                    db,
                    values=['Volume'],
                    columns=columnf,
                    aggfunc={
                        'Volume':np.sum,
                        },
                    dropna=False
                    )

    #As all columns has same value we take single value to be used as denominator below
    # deno=sm_s_pf.iloc[0,0]
    return deno

# Function to calculate Numerator for numeric handling general
def numerator(db,dbf,indexf1,indexf2,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf1,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )
    numero = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                index=indexf2,
                values=['proj_vol'],
                columns=columnf,
                aggfunc={'proj_vol':np.sum},
                )
    return numero

# Function to calculate Numerator for Category handling
def numerator_mix(db,dbf,indexf,columnf):
    smch1 = pd.pivot_table(
                db[dbf],
                index=indexf,
                values=['proj_vol'],
                aggfunc={'proj_vol':np.max},
                )

    numero = pd.pivot_table(
                smch1,                          # Note : no filter is used here
                values=['proj_vol'],
                columns=columnf,
                    aggfunc={'proj_vol':np.sum},
                )
    return numero

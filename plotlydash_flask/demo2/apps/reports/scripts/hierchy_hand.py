import pandas as pd
import importlib
import helper 
importlib.reload(helper)
import geo_hand 
importlib.reload(geo_hand)
# import apps.reports.scripts.geo_handytd
# importlib.reload(geo_handytd)
import geo_cat 
importlib.reload(geo_cat)
import string
importlib.reload(string)
import indent
importlib.reload(indent)

# import num_hand
# importlib.reload(num_hand)

#--------------------------------------------------------------------------------------
# Design STrretigy for Hum handling e.g for H2 - comlete heirarchy
#
# Final Table will be merging of SM, Manufac, Brand, PS and SKU level
#
# 1. First SKU table will be created and used as final template
# 2. Here only SKU values are reliable.
# 3. Seperate numhandling tables for SM, Manuf, Brand and PS will be created
# 4. The values from these tables will be inserted into SKu table to get the final Table
# 5. Four Seperate files for Geography for each level will be made
# 6. From these files numhandling calculation files will be called
# 7. Finaly all the files will be assembled here
#
# Parameters:
# indexf = hlist - heirarchy list
#------------------------------------------------------------------------------------------

# General Function for all Heirarchies

def hfunc(db,kpi,geo,d,indexf,heir,market_array):
    # CATEGORY HANDLING Row only for selected handling KPIs
    if kpi in ['num_hand','oos_hand', 'hih', 'ooswt', 'ooscost', 'sish']:
        hcat = geo_cat.gen_geo(db,d,kpi,geo,indexf,market_array)
        
        if kpi in ['num_hand','oos_hand', 'hih']:
            hcat.rename(index={'Num Proj Factor':'Category'},inplace=True)
        
        elif kpi == 'ooswt':
            hcat.rename(index={'Volume':'Category'},inplace=True)
        
        elif kpi == 'ooscost':
            hcat.rename(index={'ooscost':'Category'},inplace=True)
        
        elif kpi == 'sish':
            hcat.rename(index={'SISH_Volume':'Category'},inplace=True)
            
            

    # Get heirarchies from template file coming from UI
    hlist = indexf
    
    # Deriving hlevel lists for each level and store it in a dictionary 'hlev'
    
    # Example:    
    # {'Vendor': ['Vendor'], 'Brand': ['Vendor', 'Brand'], 'SKU': ['Vendor', 'Brand', 'SKU']}
    
    hlev = {}
    for i,v in enumerate(hlist):
        hlev[v] = hlist[:i+1]
        
    #--------------------------------------------------------------------------------------
    # Calculate lower order levels seperately and store in a dictionary 'hand'
    # to be used in h2func() below
    #
    # Also deriving high order from hlev dictionary above to be used in the next functions
    #---------------------------------------------------------------------------------------
    # Marker for the highest Hierarchy
    mhh = 0

    hand = {}
    for level in hlist[:-1]:
        hlevel = hlev[level]
        hand['hand'+ str(level)] = geo_hand.gen_geo(db,d,kpi,geo,hlevel,mhh,hlist,market_array)

    # print(hand['handVendor'].columns)
    # hand['handPS'].to_csv('hps.csv')
    # hand['handVendor'].to_csv('hmanu.csv')
    # hand['handFlavor'].to_csv('hflavor.csv')

    # # OLD NON GENERIC CODE
    # # Get SM Handling
    # level='SM'
    # hands = geo_hand.gen_geo(db,d,kpi,geo,level)
    # # Get Vendor Handling
    # level='Manu'
    # handm = geo_hand.gen_geo(db,d,kpi,geo,level)
    # # Get Brand Handling
    # level='Brand'
    # handb = geo_hand.gen_geo(db,d,kpi,geo,level)
    # # Get PS Handling
    # level='PS'
    # handp = geo_hand.gen_geo(db,d,kpi,geo,level)
    
    
    #----------------------------------------------------
    # Function for Heirarchy
    # We will generate Table upto highest hierarchy
    #
    # and later modify the lower heirarchies by Replacing
    #
    # with the tabl generated above
    #-------------------------------------------------------
    def h2func():
 
        # Marker for the Total/highest level Hierarchy
        mhh = 1

        hlevel = hlev[hlist[-1]]

        # Get highest heirachy level from hlist above
        hkpi = geo_hand.gen_geo(db,d,kpi,geo,hlevel,mhh,hlist,market_array)
        hkpi = hkpi.reset_index()
        
        # BUG SOLUTION:
        # Now rename 'index' column to heirarchy for SINGLE LEVEL Heirarchy ONLY
        if len(hlist)==1:
            hkpi.rename(columns={'index':hlist[0]},inplace=True)
        
        # WHY WHY WHY WHY?
        # Delete the row if any one of these heierstchy columns has zero value
        # This to avoid concat error with 0 row value
        for i in hlist:
            if (hkpi[i]==0).any():
                hkpi=hkpi[:-1]
        
        # Some columns like variant has 0 in it so
        # Convert Heirarchy level columns to strings
        for i in range(len(hlist)):
            hkpi[hlist[i]] = hkpi[hlist[i]].apply(str)

        # # Adding suffixes and indentations to columns as per requirement
        hkpi = indent.indentation(hkpi,hlist)
        
        # Old CODE
        # hkpi['SM'] =' ' + hkpi['SM'] + ' (Sm)'
        # hkpi['Vendor'] ='  ' + hkpi['Vendor'] + ' (Ma)'
        # hkpi['Brand'] ='    ' + hkpi['Brand'] + ' (Ba)'
        # hkpi['PS'] ='   ' + hkpi['PS'] + ' (Ps)'
        # hkpi['SKU'] = '     ' + hkpi['SKU'] + ' (Sk)'
        
        # ERROR:
        # SM and SKU both have S as a first character
        #To manage this duplicacy we do as follows:
        # Creating new list by taking first letter only and managing SM and SKU duplicates
        ## DO CHECK MORE DUPLICATE FIRST CHARACTER HEIRARCHY NAMES IN JUICES AND CIG e.
        mini_hlist = [x[0] if x!='SKU' else x[1] for x in hlist]
        # print(mini_hlist)

        # Generate new alphabatical list to be used in magic function below
        minihlist = list(string.ascii_lowercase)
        mini_hlist = minihlist[0:len(hlist)]

        # Creating dictionary from hlist and minihlist
        hdict = dict(zip(hlist,mini_hlist))
        
        # Rename columns to mini columns for easy looping used in magic function below
        ndb = hkpi.rename(columns=hdict)
        
        # Convert mini hlist to a string e.g 'SMBPK'
        hstring = ('').join(mini_hlist)
        
        # with open('t2.txt','w') as f:
        #     f.write(str(t2))
        
        
        # MAGIC FUNCTION to Create HEIRARCHICAL data rows
        h2 = pd.concat([
                ndb.assign(
                    **{x: '' for x in hstring[i:]}
                ).groupby(list(hstring)).sum() for i in range(1, (len(hstring)+1))
            ]).sort_index()
        
        
        
        # EXECUTE FOLLOWING CODE ONLY FOR MULTI LEVEL HIERARCHIES
        if len(hstring)>>1:
            # Arrange order as per Quantum
            # Index sorting as per requirement
            #for cigeratte and where index is 'SM'
            if hlist[0]=='SM':
                h2 = h2.reindex([' Pakistan Tobacco Company (SM)',' Philip Morris Pak Ltd (SM)',' Local (Other than PTC-PMI) (SM)',' ITB (SM)'],level=0)

            # Joining index columns into one as Quatum table requirement
            h2.index = h2.index.map('_'.join)

            
            # Replacing correct handling values from hand tables above
            #
            for level in hlist[:-1]:
                h2.loc[hand['hand'+ str(level)].index, :] = hand['hand'+ str(level)][:]

            ## OLD CODE
            # h2.loc[hands.index, :] = hands[:]
            # # Replace all Ma handling rows
            # h2.loc[handm.index, :] = handm[:]
            # # Replace all Brand handling rows
            # h2.loc[handb.index, :] = handb[:]
            # # # Replace all Ps handling rows
            # h2.loc[handp.index, :] = handp[:]

            # Converting index to a column with name index
            h2=h2.reset_index()

            # Remove trailing '_'
            h2['index'] = h2['index'].str.rstrip('_')

            # splitting the index column to filter the last part
            h2[['col1','col2']]= h2['index'].str.rsplit('_', 1, expand=True).rename(lambda x: f'col{x + 1}', axis=1)

            # Copy values from col1 to col2 where col2=nan
            h2['col2'] = h2['col2'].fillna(h2['col1'])

            # Removing surplus columns
            h2=h2.drop(['col1','index'],axis=1)

            # Move col2 to the start
            first_col =h2.pop('col2')
            h2.insert(0,'H2',first_col)
            

            # Get grand total row by calling helper function
            # But not for 'wt_hand' as it is not shown in the sample sheet
            if kpi!='wt_hand':
                h2_tot_row = helper.add_tot_h2_nat_vol(hkpi,indexf)

                # Move H2 Column to the start to align with h2 table
                # This is important to avaiod the alphabatical ordering of concation operation below
                fcol = h2_tot_row.pop('H2')
                h2_tot_row.insert(0,'H2',fcol)

                # concat
                h2 = pd.concat([h2_tot_row,h2])
                
            # convert column to index
            h2.set_index('H2',inplace=True)
            # Setting columns(H2) and index(Month) names to blank
            h2 = h2.rename_axis(['',''],axis=1)
            h2 = h2.rename_axis([''],axis=0)

            # Replace all the columns of Category Row with the calculated one above
            if (kpi=='num_hand')|(kpi=='oos_hand')|(kpi=='ooswt')|(kpi=='hih')|(kpi=='sish')|(kpi=='ooscost'):
                h2.loc[hcat.index,:] = hcat[:]

        return h2/100


    # Calling Custom Function
    hchy=h2func()


    return hchy

import pandas as pd
import importlib
import helper 
import level_format2 
importlib.reload(level_format2)
import gb 
importlib.reload(gb)
import indent 
importlib.reload(indent)
import string

# General Function for all Heirarchies
def hfunc(db,geo,d,heir,indexf,market_array):

    # Create new unit sale price columns
    # by dividing the sale by Weight columns
    db['sale_priceU'] = db['sale_price']/db['Weights']
    db['Sale_newU'] = db['Sale_new']
    # db.to_csv('dbprice.csv')

    # assigning pivot values to be used in gb file later
    valuef2 = 'Sale_newU'
    
    valuef1='sale_priceU'

    # Get heirarchies from template file coming from q2py.py
    hlist = indexf

    # Custom Function for Heirarchy=2
    def h2func():
        # BUild geographies for each level by calling geo_build FUnction

        # Deriving hlevel lists for each level and store it in a dictionary 'hlev'
        hlev = {}
        # create a dictionary from hlist using enumerate function
        for i,v in enumerate(hlist):
            hlev[v] = hlist[:i+1]

        # Calculate lower order levels seperately and store in a dictionary 'hand'
        # to be used  below
        #
        # Also deriving high order from hlev dictionary above to be used in the next functions

        # Marker for the highest Hierarchy
        mhh = 0
        hand = {}
        for level in hlist[:-1]:
            hlevel = hlev[level]

            hand['hand'+ str(level)] = gb.geo_build(db,geo,d,hlevel,market_array,valuef1,valuef2)


            # delete last row as it contains 0 in the indexf
            hand['hand'+ str(level)] = hand['hand'+ str(level)][:-1]

            nat=1
            hand['hand'+ str(level)] = level_format2.format(hand['hand'+ str(level)],nat,hlevel,mhh,hlist)
            # hand['handVendor'].to_csv('handm.csv')



        # We will generate Table upto highest hierarchy
        #
        # and later modify the lower heirarchies by Replacing
        #
        # with the tabl generated above

        # Marker for the highest Hierarchy
        mhh = 1

        hlevel = hlev[hlist[-1]]
        hkpi = gb.geo_build(db,geo,d,hlevel,market_array,valuef1,valuef2)
        # delete last row as it contains 0 in the indexf
        hkpi = hkpi[:-1]

        # Get Category table- only one row
        level='cat'
        # indexf='none'
        hcat = gb.geo_build_cat(db,geo,d,hlevel,market_array,valuef1,valuef2)
        hcat.rename(index={'sale_priceU':'Category'},inplace=True)
        # hcat.rename(index={'sale_price':'Category'},inplace=True)

        # Adding suffixes and indentations to columns as per requirement
        hkpi=hkpi.reset_index()


        # BUG SOLUTION Now rename 'index' column to heirarchy for SINGLE LEVEL Heirarchy ONLY
        if len(hlist)==1:
            hkpi.rename(columns={'index':hlist[0]},inplace=True)
        # Delete the row if any one of these heierstchy columns has zero value
        # This to avaid concat error with 0 row value
        for i in hlist:
            if (hkpi[i]==0).any():
                hkpi=hkpi[:-1]
        # some columns like variant has 0 in it so
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


        # ERROR: This method ceate duplicate columns hence giving error
        # Creating new temporary list by taking first letter only and managing SM and SKU duplicates
        # mini_hlist = [x[0] if x!='SKU' else x[1] for x in hlist]

        # Create new temporary list to be used in magic function below
        minihlist = list(string.ascii_lowercase)
        mini_hlist = minihlist[0:len(hlist)]

        # Creating dictionary from hlist and minihlist
        hdict = dict(zip(hlist,mini_hlist))
        # Rename columns to mini columns easy looping used in magic function below
        ndb = hkpi.rename(columns=hdict)

        # Convert mini hlist to a string e.g 'SMBPK'
        hstring = ('').join(mini_hlist)


        # MAGIC FUNCTION to Create heirachical rows
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

            # Replacing correct handling values from SM,Ma, Brand and PS tables
            #
            for level in hlist[:-1]:
                h2.loc[hand['hand'+ str(level)].index, :] = hand['hand'+ str(level)][:]

            ## OLD CODE
            # h2.loc[hands.index, :] = hands[:]
            #
            # # Replace all Ma handling rows
            # h2.loc[handm.index, :] = handm[:]
            #
            # # Replace all Brand handling rows
            # h2.loc[handb.index, :] = handb[:]
            #
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
            # h2.to_csv('h2cat.csv')
            # Get grand total row by calling helper function
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

            # replacing hcat row calculated above
            h2.loc[hcat.index,:] = hcat[:]

        return h2


    # Calling Custom Functions for each Heirarchy
    hchy=h2func()

    return hchy

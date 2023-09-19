import pandas as pd
import numpy as np
import importlib
import string
import helper
import indent 
importlib.reload(indent)
importlib.reload(helper)


# General Function for all Heirarchies
def hfunc(db,kpi,geo,d,indexf,heir,market_array):

    # Function to create hlist from a file heir_list.csv in data folder
    # This function also give the print order to the Heirarchy also fetched from above file
    # def hlistf():
    #     # Read CSV file into list
    #     a_csv_file = open('data/heir_file.csv','r')
    #     list_reader= csv.reader(a_csv_file)
    #     list_from_csv = list(list_reader)[heir]
    #
    #     # remove first 2 elements , "client" and "Name" from the list
    #     nlist=list_from_csv[2:]
    #
    #     # Strip all the emty or spaces elements from the list
    #     hlist = [el for el in nlist if el.strip()]
    #
    #     return hlist

    #As shares are calculted from absolutes we have to rename share kpi to absolutes
    if (kpi == 'vol_share'):
        kpi='vol_abs'
    if kpi == 'val_share':
        kpi='val_abs'
    if kpi == 'purvol_share':
        kpi='purvol_abs'
    if kpi == 'stockvol_share':
        kpi='stockvol_abs'
    if kpi == 'fwdstockvol_share':
        kpi='fwdstockvol_abs'
    if (kpi == 'saleleg')|(kpi == 'shareleg'):
        kpi='vol_abs'

    # Common parameters for h pivot table
#     indexf = ['SM', 'Vendor','Brand','PS', 'SKU' ]
    aggfuncf = {kpi:np.sum}
    valuef = [kpi]
    # print('valuef',valuef)
    # print("indexf",indexf)
    # indexf=['shop_code','Product_code']
    # aggfuncf = {kpi:np.max}

    # A pivot function to be called as needed
    def pivot(dbf, indexf, valuef, columnf, aggfuncf):
        # db.to_csv('db3.csv')
        if (kpi == 'saleleg')|(kpi == 'shareleg'):
            pivot_t = pd.pivot_table(
                    db[dbf&((db['SM']=='Philip Morris Pak Ltd')|(db['SM']=='Pakistan Tobacco Company'))],
                   index=indexf,values=valuef, columns=columnf, aggfunc=aggfuncf,fill_value=0,
                    )
        else:
            pivot_t = pd.pivot_table(
                    db[dbf],
                   index=indexf,values=valuef, columns=columnf, aggfunc=aggfuncf,fill_value=0,
                    # margins=True, margins_name='Grand Total'
                    )
        # pivot_t.drop('Grand Total', axis=1, inplace=True, level=1)


        # if (kpi == 'vol_abs'):
        #     pivot_t = pivot_t
        # elif kpi == 'val_abs':
        #     pivot_t = pivot_t
        # elif kpi == 'purvol_abs':
        #     pivot_t = pivot_t
        # elif kpi == 'stockvol_abs':
        #     pivot_t = pivot_t
        # elif kpi == 'fwdstockvol_abs':
        #     pivot_t = pivot_t

        return pivot_t


    # Total MBD
    def Mkt1():
        dbf = (db[indexf[0]]!=0)
        #First create  Total table
        columnf = ['Month']
        hkpi = pivot(dbf,indexf, valuef, columnf, aggfuncf)

        # once more roundingsnto prevent some minor unrounded values found
        # Appplying round method to all the columns
        hkpi = hkpi.applymap(lambda x:round(x,d))

        # hkpi[kpi] = hkpi[kpi].round(decimals=d)
        # rename kpi column
        hkpi = hkpi.rename(columns={kpi:'Total'},level=0)
        # hkpi.to_csv('hkpi.csv')
        return hkpi

    # Rest of the mbds
    def market(mkt):
        dbf = (db[indexf[0]]!=0)

        columnf = [mkt,'Month']
        hgeo = pivot(dbf,indexf, valuef, columnf, aggfuncf)
        # once more roundingsnto prevent some minor unrounded found
        # Appplying round method to all the columns
        hgeo = hgeo.applymap(lambda x:round(x,d))

        # hgeo[kpi] = hgeo[kpi].round(decimals=d)
        hgeo.columns=hgeo.columns.droplevel(0)
        # Concat total table with previous table
        # hkpi = pd.concat([hkpi,hgeo],axis=1)
        # hkpi.to_csv('hkpi2.csv')

        return hgeo

    # Calculation for Total MBD
    if 'Mkt1' in market_array:
        # strip away Mkt1 from array as we donot need it in the function
        market_array = [string for string in market_array if string !='Mkt1']

        hkpi = Mkt1()          #Total

        # Calculating Other MBDs other then Mkt1
        for mkt in market_array:
            hgeo = market(mkt)
            hkpi = pd.concat([hkpi,hgeo],axis=1)

    else:
        # Calculating Other MBDs other then Mkt1
        # This one is to start concatenation chain
        hkpi = market(market_array[0])

        # Calculate rest of the mbds and later concat it with the above
        for mkt in market_array[1:]:
            hgeo = market(mkt)
            hkpi = pd.concat([hkpi,hgeo],axis=1)

    # hkpi.to_csv('hkpi3.csv')
    # Converting indeces to columns
    hkpi=hkpi.reset_index()

    # Custom Function for Heirarchy=2
    def h2func(hkpi):
        # Copy Heirarchy list from indexf into hlist variable
        hlist = indexf
        # BUG SOLUTION Now rename 'index' column to heirarchy for SINGLE LEVEL Heirarchy ONLY
        if len(hlist)==1:
            hkpi.rename(columns={'index':hlist[0]},inplace=True)

        # Delete the row if any one of these heierstchy columns has zero value
        # This to avaid concat error with 0 row value
        for i in hlist:
            if (hkpi[i]==0).any():
                hkpi=hkpi[:-1]

        # if ((hkpi['SM'] == 0)|(hkpi['Vendor'] == 0)|(hkpi['Brand'] == 0)|(hkpi['PS'] == 0)|(hkpi['SKU'] == 0)).any():
        #     hkpi=hkpi[:-1]

        # some columns like variant has 0 in it so
        # Convert Heirarchy level columns to strings
        # for i in range(len(hlist)):
        #     hkpi[hlist[i]] = hkpi[hlist[i]].apply(str)
            # hkpi[hlist[i]] = hkpi[hlist[i]].replace(0,'NaN')


        # # Adding suffixes and indentations to columns as per requirement
        # for i in range(len(hlist)):
        hkpi = indent.indentation(hkpi,hlist)

        ## OLD CODE
        # hkpi['SM'] =' ' + hkpi['SM'] + ' (Sm)'
        # hkpi['Vendor'] ='  ' + hkpi['Vendor'] + ' (Ma)'
        # hkpi['Brand'] = '    ' +  hkpi['Brand'] + ' (Ba)'
        # hkpi['PS'] = '   ' + hkpi['PS'] + ' (Ps)'
        # hkpi['SKU'] = '     ' + hkpi['SKU'] + ' (Sk)'
        # hkpi.loc(['SKU'],:) = '     ' + hkpi['SKU'] + ' (Sk)'


        # New Grand Total Row
        # hkpi.loc['Grand Total'] = hkpi.sum(numeric_only=True).round(decimals=d)
        hkpi.loc['Grand Total'] = hkpi.sum(numeric_only=True)

        # Following commands fetching input and creating generic handling
        # #

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

        # ndb = hkpi.rename(columns={'SM':'s','Vendor':'m','Brand':'b','PS':'p','SKU':'k'})
        # ndb = hkpi.rename(columns={'PS':'p'})

        # MAGIC FUNCTION to Create heirachical rows
        h2 = pd.concat([
                ndb.assign(
                    **{x: '' for x in hstring[i:]}
                ).groupby(list(hstring)).sum() for i in range(1, (len(hstring)+1))
            ]).sort_index()

        # Appplying round method to all the columns
        # This will make sure that all Columns are rounded equaly
        # h2 = h2.applymap(lambda x:round(x,d))


        # Create temporary table by converting SMBPK as columns
        h2t = h2.reset_index()


        # print("h2t",h2t.columns)
        # print(h2t[('S','')].unique())
        # print(h2t[('S','')].unique()[0])
        # print("h2index",h2.index.unique())

        # EXECUTE FOLLOWING CODE ONLY FOR MULTI LEVEL HIERARCHIES
        if len(hstring)>>1:
            # Arrange order as per Quantum requirement
            # Index sorting as per requirement
            #for cigeratte and where index is 'SM'

            # h2t[('S','')].unique() is list of 4 unique SMs in SM column
            # h2t[('S','')].unique()[0] = ITB
            # h2t[('S','')].unique()[1] = Local
            # h2t[('S','')].unique()[2] = PTC
            # h2t[('S','')].unique()[3] = Philip Morris

            if hlist[0]=='SM':
                h2 = h2.reindex([h2t[('S','')].unique()[2],h2t[('S','')].unique()[3],h2t[('S','')].unique()[1],h2t[('S','')].unique()[0]],level=0)

            # Joining index columns into one as Quatum table requirement
            h2.index = h2.index.map('_'.join)

            # Converting index to a column with name index
            h2=h2.reset_index()
            # h2.to_csv('h2index.csv')

            # Remove trailing '_'
            h2['index'] = h2['index'].str.rstrip('_')

            # splitting the index column to filter the last part
            h2[['col1','col2']]= h2['index'].str.rsplit('_', 1, expand=True).rename(lambda x: f'col{x + 1}', axis=1)
            # h2.to_csv('h2split.csv')
            # Copy values from col1 to col2 where col2=nan
            h2['col2'] = h2['col2'].fillna(h2['col1'])
            # h2.to_csv('h2split2.csv')
            # Removing surplus columns
            h2=h2.drop(['col1','index'],axis=1)

            # Move col2 to the start
            first_col =h2.pop('col2')
            h2.insert(0,'H2',first_col)
            # h2.to_csv('h22.csv')

            # Get grand total row by calling helper function
            h2_tot_row = helper.add_tot_h2_nat_vol(hkpi,indexf)
            # Move H2 to the start
            first_col =h2_tot_row.pop('H2')
            h2_tot_row.insert(0,'H2',first_col)
            # concat Total and the multi level heirarchy table
            h2 = pd.concat([h2_tot_row,h2])
            # Rename index from Grand Total to 'Category'
            h2.rename(index={'Grand Total':'Category'},inplace=True)

            # convert column to index
            h2.set_index('H2',inplace=True)
        
            # Setting columns(H2) and index(Month) names to blank
            h2 = h2.rename_axis(['',''],axis=1)
            h2 = h2.rename_axis([''],axis=0)

        # For single level Heirarchy
        else:
            # Arrange order as per Quantum
            # Index sorting as per requirement
            #for cigeratte and where index is 'SM'
            # if hlist[0]=='SM':
                # h2 = h2.reindex([' Pakistan Tobacco Company (SM)',' Philip Morris Pak Ltd (SM)',' Local (Other than PTC-PMI) (SM)',' ITB (SM)'])

            # Remove name of the index
            h2 = h2.rename_axis([''],axis=0)
            # Get grand total row by calling helper function
            h2_tot_row = helper.add_tot_h2_nat_vol(hkpi,indexf)
            # Drop 'H2' column
            h2_tot_row=h2_tot_row.drop(['H2'],axis=1)
            # concat Total and the single level heirarchy table
            h2 = pd.concat([h2_tot_row,h2])
            # Rename index from Grand Total to 'Category'
            h2.rename(index={'Grand Total':'Category'},inplace=True)


        return h2


    # Calling Custom Functions for each Heirarchy
    # hkpi.to_csv('hkpif.csv')
    hchy=h2func(hkpi)

    return hchy

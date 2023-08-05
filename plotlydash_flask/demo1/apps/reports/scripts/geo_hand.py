import pandas as pd
import importlib
import num_hand
importlib.reload(num_hand)
import wt_hand 
importlib.reload(wt_hand)
import ooscost 
importlib.reload(ooscost)
import sppd 
importlib.reload(sppd)
import oos_hand 
importlib.reload(oos_hand)
import ooswt_hand 
importlib.reload(ooswt_hand)
import sish_hand 
importlib.reload(sish_hand)
import cat_hand 
importlib.reload(cat_hand)
import level_format 
importlib.reload(level_format)


# This is General Function to calculate geographical KPIs
def gen_geo(db,d,kpi,geo,hlevel,mhh,hlist,market_array):
    indexf = hlist
    # level=highlist

    # FUnction for Calling respective Handling functions

    # For Nationat
    def hand_func_nat(dbf):
        nat=1
        if kpi == 'num_hand':
            hgeo = num_hand.numeric_handling_nat(db,dbf,hlevel)*100

        elif kpi == 'wt_hand':
            hgeo = wt_hand.wt_handling_nat(db,dbf,hlevel)*100

        elif kpi == 'ooscost':
            hgeo = ooscost.ocost_nat(db,dbf,hlevel)

        elif kpi == 'sppd':
            hgeo = sppd.sppdf_nat(db,dbf,hlevel)

        elif kpi == 'oos_hand':
            hgeo = oos_hand.oos_handling_nat(db,dbf,hlevel)*100

        elif kpi == 'ooswt':
            hgeo = ooswt_hand.ooswt_handling_nat(db,dbf,hlevel)*100
        # elif kpi == 'hih':
        #     if gid=='nat':
        #         hgeo = hih_hand.numeric_handling_nat(db,level)
        #         # hgeo.to_csv('nat.csv')
        #     else:
        #         hgeo = hih_hand.numeric_handling(db,gid,geog,dbf,level)

        elif kpi == 'hih':
            Num = num_hand.numeric_handling_nat(db,dbf,hlevel)
            Den = cat_hand.cath_handling_nat(db,dbf,hlevel)
            # Den.columns = Den.columns.droplevel(0)

            #Converting dataframe to series to avoid error while dividing below
            Num=Num.iloc[0]
            hgeo = (Num/Den)*10000

        elif kpi == 'sish':
            hgeo = sish_hand.sish_handling_nat(db,dbf,hlevel)

        hgeo = level_format.format(hgeo,nat,hlevel,mhh,hlist)


        return hgeo


    # For ret of markets
    def hand_func(dbf,gid,g):
        if kpi == 'num_hand':
            hgeo = num_hand.numeric_handling(db,dbf,hlevel,gid,g)*100

        elif kpi == 'wt_hand':
            hgeo = wt_hand.wt_handling(db,dbf,hlevel,gid)*100
            # if hlevel=='Brand':
                # hgeo.to_csv('hgeowtbrand.csv')

        elif kpi == 'ooscost':
            hgeo = ooscost.ocost(db,dbf,hlevel,gid)

        elif kpi == 'sppd':
            hgeo = sppd.sppdf(db,dbf,hlevel,gid)

        elif kpi == 'oos_hand':
            hgeo = oos_hand.oos_handling(db,dbf,hlevel,gid,g)*100

        elif kpi == 'ooswt':
            hgeo = ooswt_hand.ooswt_handling(db,dbf,hlevel,gid)*100
        # elif kpi == 'hih':
        #     if gid=='nat':
        #         hgeo = hih_hand.numeric_handling_nat(db,level)
        #         # hgeo.to_csv('nat.csv')
        #     else:
        #         hgeo = hih_hand.numeric_handling(db,gid,geog,dbf,level)

        elif kpi == 'hih':
            Num = num_hand.numeric_handling(db,dbf,hlevel,gid,g)
            Den = cat_hand.cath_handling(db,dbf,hlevel,gid,g)

            Den.columns = Den.columns.droplevel(0)
            #Converting dataframe to series to avoid error while dividing below
            #it transpose rows and columns
            Num=Num.iloc[0]

            hgeo = (Num/Den)*10000

        elif kpi == 'sish':
            hgeo = sish_hand.sish_handling(db,dbf,hlevel,gid)

        nat=0
        hgeo = level_format.format(hgeo,nat,hlevel,mhh,hlist)

        return hgeo


    #### End of Generic Functions    #####


    # Total MBD
    def Mkt1():
        dbf = (db[indexf[0]]!=0)

        # Calling respective Handling functions
        hkpi = hand_func_nat(dbf)
        # Appplying round method to all the columns
        hkpi = hkpi.applymap(lambda x:round(x,d))

        # once more roundingsnto prevent some minor unrounded values found
        # hgeo['Num Proj Factor'] = hgeo['Num Proj Factor'].round(decimals=d)
        # rename Top column
        if (kpi == 'num_hand')|(kpi == 'oos_hand')|(kpi == 'hih'):
            hkpi = hkpi.rename(columns={'Num Proj Factor':'Total'},level=0)
        elif (kpi == 'wt_hand')|(kpi == 'ooswt'):
            hkpi = hkpi.rename(columns={'Volume':'Total'},level=0)
        elif kpi == 'sish':
            hkpi = hkpi.rename(columns={'SISH_Volume':'Total'},level=0)
        elif kpi == 'ooscost':
            hkpi = hkpi.rename(columns={'ooscost':'Total'},level=0)
        elif kpi == 'sppd':
            hkpi = hkpi.rename(columns={'sppd':'Total'},level=0)

        # if hlevel==['Vendor','Brand','Flavor']:
        # hkpi.to_csv('hkpi2.csv')
        return hkpi


    def market(hkpi,mkt):
        gid = mkt
        # geog are the geograhies in Mkt columns
        # We have to create a loop over unique values and calculate handling
        geog = db[gid].unique()

        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issue in SISH
        geog=sorted(geog)

        for g in geog:
            dbf = (db[gid]==g)
            # columnf = [gid,'Month']

            hgeo = hand_func(dbf,gid,g)

            # Appplying round method to all the columns
            hgeo = hgeo.applymap(lambda x:round(x,d))

            # Concat total table with previous table
            hkpi = pd.concat([hkpi,hgeo],axis=1)
        return hkpi

    def market2(mkt):
        gid = mkt
        # geog are the geograhies in Mkt5 columns
        # We have to create a loop over unique values and calculate handling
        geog = db[gid].unique()

        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issue in SISH
        geog=sorted(geog)


        for g in geog:
            dbf = (db[gid]==g)
            # columnf = [gid,'Month']

            hgeo = hand_func(dbf,gid,g)

            # Appplying round method to all the columns
            hgeo = hgeo.applymap(lambda x:round(x,d))

            # Concat total table with previous table
            # hkpi = pd.concat([hkpi,hgeo],axis=1)
        return hgeo


    # Calculation for Total MBD
    if 'Mkt1' in market_array:
        # strip away Mkt1 from array as we donot need it in the function
        market_array = [string for string in market_array if string !='Mkt1']

        hkpi = Mkt1()          #Total

        # Calculating Other MBDs other then Mkt1
        for mkt in market_array:
            hkpi = market(hkpi,mkt)

    else:
        # Calculating Other MBDs other then Mkt1
        # This one is to start concatenation chain
        hkpi = market2(market_array[0])

        for mkt in market_array[1:]:
            hkpi = market(hkpi,mkt)
            # hkpi = pd.concat([hcat,hgeo],axis=1)

    return hkpi

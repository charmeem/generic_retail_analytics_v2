import pandas as pd
import importlib
import num_hand2
importlib.reload(num_hand2)
import oos_hand2
importlib.reload(oos_hand2)
import ooswt_hand2
importlib.reload(ooswt_hand2)
import cath_hand2
importlib.reload(cath_hand2)
import sish_hand
importlib.reload(sish_hand)
import ooscost
importlib.reload(ooscost)
import sppd
importlib.reload(sppd)

# General Function to calculate geographical KPIs
def gen_geo(db,d,kpi,geo,indexf,market_array):
    # print("indexf:",indexf)

    # FUnction for Calling respective Handling functions
    def hand_func(gid,geog,dbf1,g):
        if (kpi == 'num_hand'):
            if gid=='nat':
                hgeo = num_hand2.cat_handling_nat(db)*100
            else:
                hgeo = num_hand2.cat_handling(db,gid,geog,dbf1,g)*100

        if (kpi == 'oos_hand'):
            if gid=='nat':
                hgeo = oos_hand2.cat_handling_nat(db)
            else:
                hgeo = oos_hand2.cat_handling(db,gid,geog,dbf1,g)

        if (kpi == 'ooswt'):
            if gid=='nat':
                hgeo = ooswt_hand2.cat_handling_nat(db)
            else:
                hgeo = ooswt_hand2.cat_handling(db,gid,geog,dbf1)

        if (kpi == 'ooscost'):
            if gid=='nat':
                hgeo = ooscost.ocostcat_handling_nat(db,indexf)
            else:
                hgeo = ooscost.ocostcat_handling(db,gid,geog,dbf1)

        if (kpi == 'sppd'):
            if gid=='nat':
                hgeo = sppd.sppdcat_handling_nat(db)
            else:
                hgeo = sppd.sppdcat_handling(db,gid,geog,dbf1)

        elif kpi == 'hih':
            if gid=='nat':
                Num = num_hand2.cat_handling_nat(db)
                Den = cath_hand2.cat_handling_nat(db)
                hgeo = (Num/Den)*10000
            else:
                Num = num_hand2.cat_handling(db,gid,geog,dbf1,g)
                Den = cath_hand2.cat_handling(db,gid,geog,dbf1,g)
                hgeo = (Num/Den)*10000
        elif kpi == 'sish':
            if gid=='nat':
                hgeo = sish_hand.cat_handling_nat(db)
            else:
                hgeo = sish_hand.cat_handling(db,gid,geog,dbf1)
        return hgeo


    #### MBD Functions    #####
    def Mkt1():
        dbf1 = (db[indexf[0]]!=0)
        g = 'dummy'
        gid='nat'
        geog='nat'
        hcat = hand_func(gid,geog,dbf1,g)
        hcat.columns = pd.MultiIndex.from_product([hcat.columns, ['Total']]).swaplevel(0,1)
        return hcat

    def market(hkpi,mkt):
        gid=mkt
        # geog are the geograhies in Mkt5 columns
        # We have to create a loop over unique values and calculate handling
        # geog = ['Rural','Urban']
        geog = db[gid].unique()
        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issue in SISH
        geog=sorted(geog)

        for g in geog:
            dbf1 = (db[indexf[0]]!=0)&(db[gid]==g)
            hrg = hand_func(gid,geog,dbf1,g)
            hrg.columns = pd.MultiIndex.from_product([hrg.columns, [g]]).swaplevel(0,1)

            hkpi = pd.concat([hkpi,hrg],axis=1)

        return hkpi

    def market2(mkt):
        gid=mkt
        # geog are the geograhies in Mkt5 columns
        # We have to create a loop over unique values and calculate handling
        # geog = ['Rural','Urban']
        geog = db[gid].unique()
        # sort alphabaticaly to have consistent order of tables
        # hence removing division disorder issue in SISH
        geog=sorted(geog)


        for g in geog:
            dbf1 = (db[indexf[0]]!=0)&(db[gid]==g)
            hrg = hand_func(gid,geog,dbf1,g)
            hrg.columns = pd.MultiIndex.from_product([hrg.columns, [g]]).swaplevel(0,1)
            # hcat = pd.concat([hkpi,hrg],axis=1)
        return hrg


    # Calculation for Mkt1 = Total MBD
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


    hkpi = hkpi.rename(index = {'Num Proj Factor':'Category'})

    return hkpi

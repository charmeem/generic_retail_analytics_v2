import pandas as pd

# Thi Module is used for Testing different combinations of kpis.py
import kpis
dbm = pd.read_csv('C:/my_drive/python/access_retail/qtopy/desktop/data/csd/month_74_pytest.csv')

def test_price():
    assert kpis.sale_price(dbm) == dbm['Sale_new'].any()


# Thi Module is used for Testing different combinations of heir.csv file
# and observing the effect on diffent modules

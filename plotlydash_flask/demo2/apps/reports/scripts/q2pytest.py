# print('hellllooo babloo')
import pandas as pd
# db = pd.read_csv('data/month_13.csv')
db = pd.read_csv('logs/cig/cell_analysis.csv')

# dbh = db.head().to_html()
# db = db.to_html('dbhtml.html')
# print("dbhtml generated")
db2 = db.head().to_html()
# print("hello from python")
print(db2)
# print(db.shape)

import os
import requests
import time
import json
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))

# loading test dataset
df10 = pd.read_csv( base_path + '/../data/test.csv' )
df_store_raw = pd.read_csv( base_path + '/../data/store.csv', low_memory=False )

# merge test dataset + store
df_test = pd.merge( df10, df_store_raw, how='left', on='Store' )

# choose store for predicition
df_test = df_test[df_test['Store'].isin([24, 12, 22] )]

# remove closed days
df_test = df_test[df_test['Open'] != 0]
df_test = df_test[~df_test['Open'].isnull()]
df_test = df_test.drop( 'Id', axis=1 )

# convert dataframe to json
data = json.dumps( df_test.to_dict( orient='records' ) )

# API Call

url = 'http://0.0.0.0:5000/rossmann/predict'
header = { 'Content-type': 'application/json' }

r = requests.post( url=url, data=data, headers=header )

if r.status_code == 200:
    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys() )
    d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()

    for i in range( len( d2 ) ):
        print( f"Store Number {d2.loc[i, 'store']} will sell {d2.loc[i, 'prediction']:,.2f} in the next 6 weeks" )
        time.sleep(2)



import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy import types
import numpy as np
import pandas as pd
import time
import yaml

def engine_str_formatter(config):
    return 'mysql+mysqlconnector://' + \
        config['user'] + ':' + \
        config['password'] + '@' + \
        config['host'] + '/' + \
        config['database']

with open("config.yml", 'r') as config_doc:
    config = yaml.safe_load(config_doc)

engine = create_engine(engine_str_formatter(config))
cnx = engine.connect()
    
from_station_q = '''
select
    from_station_id as station_id
  , DATE(starttime) as ride_date
  , count(distinct trip_id) as num_trips_from
from divvy_trips
where DATE(starttime) >= DATE('{0}-01-01')
  and DATE(starttime) <= DATE('{0}-12-31')
group by 1, 2
'''

to_station_q = '''
select
    to_station_id as station_id
  , DATE(starttime) as ride_date
  , count(distinct trip_id) as num_trips_to
from divvy_trips
where DATE(starttime) >= DATE('{0}-01-01')
  and DATE(starttime) <= DATE('{0}-12-31')
group by 1, 2
'''

years = [2013, 2014, 2015, 2016, 2017, 2018]

for year in years:
    print("Running {0}".format(year))
    df_from = pd.read_sql(from_station_q.format(year), cnx)
    df_to = pd.read_sql(to_station_q.format(year), cnx)
    df = df_from.merge(df_to, how='outer', on=['station_id', 'ride_date'])
    df = df.fillna(0)
    df.num_trips_from = df.num_trips_from.astype('int')
    df.num_trips_to   = df.num_trips_to.astype('int')
    print('Uploading {0}'.format(year))
    df.to_sql(
        'divvy_station_daily_trips', 
        con=cnx, schema='divvybikes', if_exists='append', index=False,
        dtype={
            'station_id':types.Integer(),
            'ride_date':types.Date(),
            'num_trips_from':types.Integer(),
            'num_trips_to':types.Integer()
        })
print('Complete!')

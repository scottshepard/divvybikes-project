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


# Taxi Data
taxi_pickup_grid_q = '''
select 
  DATE(Trip_Start_Timestamp) as trip_date
  , pickup_grid as grid
  , count(*) as taxi_pickups
from Taxi_2016
group by 1,2
'''

taxi_dropoff_grid_q = '''
select 
  DATE(Trip_Start_Timestamp) as trip_date
  , dropoff_grid as grid
  , count(*) as taxi_dropoffs
from Taxi_2016
group by 1,2
'''

print("Fetch Taxi Pickup")
df_taxi_pick = pd.read_sql(taxi_pickup_grid_q, cnx)
print("Fetch Taxi Dropoff")
df_taxi_drop = pd.read_sql(taxi_dropoff_grid_q, cnx)

df_taxi = df_taxi_pick.merge(df_taxi_drop, how='outer', on=['grid', 'trip_date'])


# Divvy Data
divvy_grid_q = '''
select 
  grid
  , ride_date as trip_date
  , sum(num_trips_from) as divvy_pickups
  , sum(num_trips_to) as divvy_dropoffs
from divvy_station_daily_trips
group by 1,2
'''

print("Fetch Divvy")
df_divvy = pd.read_sql(divvy_grid_q, cnx)
df = df_taxi.merge(df_divvy, how='outer', on=['grid', 'trip_date'])

# CTA DATA
cta_q = '''
select
  t.grid
  , DATE(r.date) as trip_date
  , sum(r.rides)
from cta_station_daily_ridership r
  join (
    select distinct station_id, grid from cta_stations
    ) t on t.station_id = r.station_id
'''
print("Fetch CTA")
df_cta = pd.sql(cta_q, cnx)
df = df.merge(df_cta, how='outer', on=['grid', 'trip_date'])

# Back out into lat/long from grid ID
df['lat'] = df.grid.astype('str').apply(lambda x: x[:2]+'.'+x[2:4])
df['long'] = df.grid.astype('str').apply(lambda x: '-' + x[4:6]+'.'+x[6:8])

df.to_sql(
        'daily_grid_activity', 
        con=cnx, schema='divvybikes', if_exists='append', index=False)

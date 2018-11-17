import geopy.distance as geo
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import time
import yaml

with open("config.yml", 'r') as config_doc:
    config = yaml.safe_load(config_doc)

cnx = mysql.connector.connect(**config)

divvy = pd.read_sql('select * from stations', cnx).to_dict('records')
cta = pd.read_sql('select * from cta_stations', cnx)
cta = cta.drop_duplicates('station_id').to_dict('records')

print('Number of Divvy Stations:', len(divvy))
print('Number of CTA Stations:', len(cta))

def distance_between_two_stations(s1, s2):
    coords1 = (s1['latitude'], s1['longitude'])
    coords2 = (s2['latitude'], s2['longitude'])
    return geo.distance(coords1, coords2).miles

print("Computing distances")

l = []
for d in divvy:
    for c in cta:
        l.append({
            'divvy_station_id': d['id'], 
            'cta_station_id': c['station_id'], 
            'distance': distance_between_two_stations(d, c)
        })

df = pd.DataFrame(l)
df.drop_duplicates(inplace=True)
print('Number of distances computed:', len(df))

def engine_str_formatter(config):
    return 'mysql+mysqlconnector://' + \
        config['user'] + ':' + \
        config['password'] + '@' + \
        config['host'] + '/' + \
        config['database']

# The pandas to_sql function takes a SqlAlchemy connection instead of a
# mysql.connection connection so we have to wrap the mysql.connection in 
# a SqlAlchemy format
engine = create_engine(engine_str_formatter(config))
conn = engine.connect()

print('Uploading table')
df.to_sql('station_distance', con=conn, schema='divvybikes', if_exists='append', index=False)
print('Complete!')

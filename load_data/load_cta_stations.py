import requests
import mysql.connector
import yaml

r = requests.get('https://data.cityofchicago.org/resource/8mj8-j3c4.json')
stations = r.json()

with open("config.yml", 'r') as config_doc:
    config = yaml.safe_load(config_doc)

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

for station in stations:

    station['longitude'] = station['location']['coordinates'][0]
    station['latitude']  = station['location']['coordinates'][1]

    station['location'] = str(station['location'])

    print(station)

    add_station = ("INSERT INTO cta_stations"
                   "(stop_id, direction_id, stop_name, station_name, \
                   station_descriptive_name, station_id, ada, red, blue, green, \
                   brown, pink, purple, purple_express, orange, yellow, \
                   longitude, latitude)"
                    "VALUES (%(stop_id)s, %(direction_id)s, %(stop_name)s, \
                    %(station_name)s, %(station_descriptive_name)s, %(map_id)s, \
                    %(ada)s, %(red)s, %(blue)s, %(g)s, %(brn)s, %(pnk)s, \
                    %(p)s, %(pexp)s, %(o)s, %(y)s, \
                    %(longitude)s, %(latitude)s)")

    cursor.execute(add_station, station)

cnx.commit()
cursor.close()
cnx.close()
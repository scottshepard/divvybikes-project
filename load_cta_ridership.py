import requests
import mysql.connector
import yaml
import numpy as np
import time
import sys

def format_url(limit, offset, base):
    url = base + '?' + '$limit=' + str(limit) + '&$offset=' + str(offset) + '&$order=:id'
    return(url)

def get_data(url):
    r = requests.get(url)
    return(r.json())

def insert_data(data, conn):
    cursor = conn.cursor()
    for line in data:
        add_line = ("INSERT INTO cta_station_ridership"
                    "(station_id, stationname, date, daytype, rides)"
                    "VALUES (%(station_id)s, %(stationname)s, %(date)s, \
                    %(daytype)s, %(rides)s)")

        cursor.execute(add_line, line)
    conn.commit()

if __name__ == '__main__':

    with open("config.yml", 'r') as config_doc:
        config = yaml.safe_load(config_doc)

    cnx = mysql.connector.connect(**config)

    # There is too much data to fetch all at once
    # so page through 1000 items at a time
    base_url = 'https://data.cityofchicago.org/resource/mh5w-x5kh.json'

    if (len(sys.argv) == 2):
        initial_offset = int(sys.argv[1])
    else:
        initial_offset=0

    for o in np.arange(initial_offset, 1000000, 1000):
        print(o)
        data = get_data(format_url(1000, o, base_url))
        if len(data) == 0:
            break
        else:
            if o % 5000 == 0:
                cnx.close()
                print("Restablishing connection")
                time.sleep(10)
                cnx = mysql.connector.connect(**config)
            insert_data(data, cnx)

    cnx.commit()
    cnx.close()

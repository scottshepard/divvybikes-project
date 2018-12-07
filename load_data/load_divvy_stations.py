import requests
import mysql.connector
import yaml



with open("config.yml", 'r') as config_doc:
    config = yaml.safe_load(config_doc)

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

r = requests.get('https://feeds.divvybikes.com/stations/stations.json')
stations = r.json()['stationBeanList']
for station in stations:
    #print(station)

    add_station = ("INSERT INTO stations"
                   "(id, stationName, availableDocks, totalDocks, latitude, \
                     longitude, statusValue, statusKey, status, availableBikes, \
                     stAddress1, stAddress2, city, postalCode, location, altitude, \
                     testStation, lastCommunicationTime, kioskType, landMark, is_renting)"
                    "VALUES (%(id)s, %(stationName)s, %(availableDocks)s, %(totalDocks)s, %(latitude)s, \
                     %(longitude)s, %(statusValue)s, %(statusKey)s, %(status)s, %(availableBikes)s, \
                     %(stAddress1)s, %(stAddress2)s, %(city)s, %(postalCode)s, %(location)s, %(altitude)s, \
                     %(testStation)s, %(lastCommunicationTime)s, %(kioskType)s, %(landMark)s, %(is_renting)s)")

    data_station = station

    cursor.execute(add_station, data_station)

cnx.commit()
cursor.close()
cnx.close()

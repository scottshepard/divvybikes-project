import csv
import os
import mysql.connector
import numpy as np
import re
import requests
import pandas as pd
from sqlalchemy import create_engine
import yaml
import zipfile

with open("config.yml", 'r') as config_doc:
    config = yaml.safe_load(config_doc)

def engine_str_formatter(config):
    return 'mysql+mysqlconnector://' + \
        config['user'] + ':' + \
        config['password'] + '@' + \
        config['host'] + '/' + \
        config['database']

engine = create_engine(engine_str_formatter(config))

cnx = engine.connect()

# Each url might take an hour or more to download and upload to mysql
# It is recommended that you comment out any urls you do not wish to upload.
past_data_urls = [
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Stations_Trips_2013.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Stations_Trips_2014_Q1Q2.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Stations_Trips_2014_Q3Q4.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2015-Q1Q2.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2015_Q3Q4.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2016_Q1Q2.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2016_Q3Q4.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2017_Q1Q2.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2017_Q3Q4.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2018_Q1.zip',
    'https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2018_Q2.zip'
]

def download_divvy_zip(url, target_path='data'):
    '''
    Download the zipped divvy data for a given url. The data downloads and 
    unzips inside the target_path, defaults to a 'data' directory.
    '''
    response = requests.get(url, stream=True)
    handle = open('divvy.zip', "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    handle.close()

    zip = zipfile.ZipFile('divvy.zip')
    zip.extractall('data')

def format_dataframe(df):
    cols = df.columns
    cols = [re.sub('[0-9]+ - ', '', col) for col in cols]
    cols = [re.sub('Rental Details Local |Rental Details |Rental |Member Details |Member ','', col) for col in cols]
    cols = [re.sub(' ', '_', col.lower()) for col in cols]
    cols[0] = 'trip_id'
    df.columns = cols
    df.rename(columns={
        'birthday': 'birthyear',
        'birthday_year': 'birthyear',
        'start_time': 'starttime',
        'end_time': 'stoptime',
        'start_station_name': 'from_station_name',
        'start_station_id': 'from_station_id',
        'end_station_name': 'to_station_name',
        'end_station_id': 'to_station_id',
        'duration_in_seconds_uncapped': 'tripduration',
        'user_type': 'usertype',
        'bikeid': 'bike_id'}, 
        inplace=True)
    df['starttime'] = pd.to_datetime(df.starttime)
    df['stoptime']  = pd.to_datetime(df.stoptime)
    return(df)

def write_trips_file_to_mysql(file_path, eng):
    df = pd.read_csv(file_path)
    df = format_dataframe(df)
    # Iterate through chunks of 5000 rows or else the connection might time
    # out before the csv finishes uploading
    cnx = engine.connect()
    for k,g in df.groupby(np.arange(len(df))//5000):
        cnx.close()
        print("Restablishing connection")
        time.sleep(10)
        cnx = engine.connect()
        g.to_sql('trips', con=cnx, schema='divvybikes', if_exists='append', index=False)

def write_all_trips_files_to_mysql(directory, eng):
    '''
    Look through a given directory and insert files matching the pattern
    Divvy_Trips_[year].csv to a MySQL database
    '''
    file_list = os.listdir(directory)
    for file in file_list:
        csv_regex = re.search('.*_Trips_.*.csv', file)
        dir_regex = re.search('.*_Trips_.*', file)
        if csv_regex is not None:
            print("Starting ", file)
            write_trips_file_to_mysql(os.path.join(directory, file), eng)
            os.remove(os.path.join(directory, file))
            print("Finished ", file)
        elif dir_regex is not None:
            # Zip drives might contain multiple directories, each containing
            # their own csvs
            write_all_trips_files_to_mysql(os.path.join('data', file), eng)

# Download all the data
# After each download, insert the data into database from the config file
# Then remove the data that has been uploaded
for url in past_data_urls:
    print('Downloading from ', url)
    download_divvy_zip(url)
    write_all_trips_files_to_mysql('data', engine)

cnx.close()

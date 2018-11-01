## Setup

1. Create divvy database

Open MySQLWorkbench local connection

Run divvy_schema.sql 

2. Fill local db with data

make a copy of config.yml.example and name it config.yml

    cp config.yml.example config.yml

Enter your own local username/password in the config file

Install python packages

    pip install -r requirements.txt

Run the script

	python parse_divvy.py

Check that the data has been loaded in MySQLWorkbench

	select count(*) from stations


#Use the diivvybikes data set
Use divvybikes;

# Update the column names so that there are no spaces
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Payment Type` Payment_Type VARCHAR(100) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Trip ID` Trip_ID VARCHAR(255) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Taxi ID` Taxi_ID VARCHAR(255) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Trip Start Timestamp` Trip_Start_Timestamp text NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Trip End Timestamp` Trip_End_Timestamp text NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Trip Seconds` Trip_Seconds Decimal(10,2) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Trip Miles` Trip_Miles Decimal(7,3) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Trip Total` Trip_Total VARCHAR(255) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Pickup Centroid Latitude` Pickup_Centroid_Latitude Decimal(11,9) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Pickup Centroid Longitude` Pickup_Centroid_Longitude Decimal(11,9) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Dropoff Centroid Latitude` Dropoff_Centroid_Latitude Decimal(11,9) NOT NULL;
ALTER TABLE divvybikes.Taxi_2016 CHANGE COLUMN `Dropoff Centroid Longitude` Dropoff_Centroid_Longitude Decimal(11,9) NOT NULL;

#Remove all dollar signs from the Fare, Tips, Tolls, Extras, and Trip Total column
SET SQL_SAFE_UPDATES=0;
UPDATE divvybikes.Taxi_2016
SET Fare = REPLACE(Fare, '$', '');
UPDATE divvybikes.Taxi_2016
SET Tips = REPLACE(Tips, '$', '');
UPDATE divvybikes.Taxi_2016
SET Tolls = REPLACE(Tolls, '$', '');
UPDATE divvybikes.Taxi_2016
SET Extras = REPLACE(Extras, '$', '');
UPDATE divvybikes.Taxi_2016
SET Trip_Total = REPLACE(Trip_Total, '$', '');
SET SQL_SAFE_UPDATES=1;

#Remove all / from the dates and replace with a dash Timestamps column
SET SQL_SAFE_UPDATES=0;
UPDATE divvybikes.Taxi_2016 SET Trip_Start_Timestamp = STR_TO_DATE(Trip_Start_Timestamp,'%m/%d/%Y %h:%i:%s %p');
UPDATE divvybikes.Taxi_2016 SET Trip_End_Timestamp = STR_TO_DATE(Trip_End_Timestamp,'%m/%d/%Y %h:%i:%s %p');
SET SQL_SAFE_UPDATES=1;

#Create new columns of Lat and Long Area rounded to 100
ALTER TABLE divvybikes.Taxi_2016 MODIFY Fare Decimal(6,2);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Tips Decimal(6,2);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Tolls Decimal(6,2);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Extras Decimal(6,2);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Trip_Total Decimal(6,2);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Pickup_Centroid_Latitude Decimal(11,9);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Pickup_Centroid_Longitude Decimal(11,9);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Dropoff_Centroid_Latitude Decimal(11,9);
ALTER TABLE divvybikes.Taxi_2016 MODIFY Dropoff_Centroid_Longitude  Decimal(11,9);

SET SQL_SAFE_UPDATES=0;
ALTER TABLE divvybikes.Taxi_2016 ADD COLUMN Pickup_grid varchar(10) AFTER Pickup_Centroid_Longitude;
ALTER TABLE divvybikes.Taxi_2016 ADD COLUMN Dropoff_grid varchar(10) AFTER Dropoff_Centroid_Longitude;
UPDATE divvybikes.Taxi_2016	
SET Pickup_grid = REPLACE(REPLACE(concat(ROUND(Pickup_Centroid_Latitude,2),ROUND(Pickup_Centroid_Longitude,2)),'.',''),'-','');
UPDATE divvybikes.Taxi_2016
SET Dropoff_grid = REPLACE(REPLACE(concat(ROUND(Dropoff_Centroid_Latitude,2),ROUND(Dropoff_Centroid_Longitude,2)),'.',''),'-','');
SET SQL_SAFE_UPDATES=1;


#Script for cta_stations creation of grid
ALTER TABLE divvybikes.cta_stations ADD COLUMN grid varchar(10) AFTER latitude;
SET SQL_SAFE_UPDATES=0;
UPDATE divvybikes.cta_stations
SET grid = REPLACE(REPLACE(concat(ROUND(latitude,2),ROUND(longitude,2)),'.',''),'-','');
SET SQL_SAFE_UPDATES=1;

#Script for divy_stations creation of grid
ALTER TABLE divvybikes.divvy_stations ADD COLUMN grid varchar(10) AFTER longitude;
SET SQL_SAFE_UPDATES=0;
UPDATE divvybikes.divvy_stations
SET grid = REPLACE(REPLACE(concat(ROUND(latitude,2),ROUND(longitude,2)),'.',''),'-','');
SET SQL_SAFE_UPDATES=1;



#Alter the loaded tables to establish the primary keys
ALTER TABLE cta_station_daily_ridership
ADD PRIMARY KEY (station_id);

ALTER TABLE divvy_station_daily_trips2
ADD PRIMARY KEY (station_id);

ALTER TABLE divvy_trips2
ADD PRIMARY KEY (trip_id);

ALTER TABLE Taxi_2016
ADD PRIMARY KEY (New_ID);

ALTER TABLE Taxi_Trips_2017
ADD PRIMARY KEY (Trip_ID);

ALTER TABLE divvy_station_daily_trips2
ADD CONSTRAINT PK_id PRIMARY KEY (station_id,ride_date);

ALTER TABLE divvy_trips
ADD CONSTRAINT PK_id PRIMARY KEY (Trip_index,trip_id,starttime, bike_id);

#Alter the Divvy trips table to create a unique index column
ALTER TABLE divvybikes.divvy_trips2 ADD PRIMARY KEY(key_ID);

#Set desired not null columns
ALTER TABLE divvybikes.divvy_stations 
CHANGE grid grid varchar(10) NOT NULL;

ALTER TABLE divvybikes.divvy_station_daily_trips
CHANGE grid grid varchar(10) NOT NULL;

ALTER TABLE divvybikes.divvy_trips 
CHANGE starttime starttime DATETIME NOT NULL;

ALTER TABLE divvybikes.daily_grid_activity
CHANGE grid grid varchar(10) NOT NULL;

ALTER TABLE divvybikes.daily_grid_activity
CHANGE trip_date trip_date date NOT NULL;

ALTER TABLE divvybikes.divvy_trips 
CHANGE starttime starttime datetime NOT NULL;

ALTER TABLE divvybikes.Taxi_2016
CHANGE Time_start_timestamp Time_start_timestamp datetime NOT NULL;

ALTER TABLE divvybikes.Taxi_2016 
CHANGE Pickup_grid Pickup_grid varchar(10) NOT NULL;

ALTER TABLE divvybikes.Taxi_2016 
CHANGE Dropoff_grid Dropoff_grid varchar(10) NOT NULL;

ALTER TABLE divvybikes.cta_stations
CHANGE cta_grid cta_grid varchar(10) NOT NULL;


#Alter tables to establish foreign keys
ALTER TABLE cta_station_daily_ridership
ADD FOREIGN KEY (station_id) REFERENCES cta_stations(station_id);

ALTER TABLE cta_stations
ADD FOREIGN KEY (grid) REFERENCES divvy_stations(grid);

ALTER TABLE divvy_stations
ADD FOREIGN KEY (starttime) REFERENCES divvy_trips(starttime);

ALTER TABLE divvy_station_daily_trips
ADD FOREIGN KEY (station_id) REFERENCES divvy_stations(id);

ALTER TABLE daily_grid_activity
ADD FOREIGN KEY (divvy_pickups,divvy_dropoffs,divvy_ride_date,divvy_grid) REFERENCES divvy_station_daily_trips(num_trips_from,num_trips_to,ride_date,grid);

ALTER TABLE daily_grid_activity
ADD FOREIGN KEY (divvy_pickups,divvy_dropoffs,divvy_ride_date) REFERENCES divvy_station_daily_trips(num_trips_from,num_trips_to,ride_date);

ALTER TABLE cta_station_daily_ridership
ADD FOREIGN KEY (cta_grid) REFERENCES cta_stations(cta_grid);

ALTER TABLE daily_grid_activity
ADD FOREIGN KEY (cta_date, cta_rides, cta_grid) REFERENCES cta_station_daily_ridership(date, rides, cta_grid);

ALTER TABLE daily_grid_activity_has_Taxi_2016
ADD FOREIGN KEY (Taxi_start_timestamp, Taxi_pickup_grid, Taxi_dropoff_grid) REFERENCES Taxi_2016(Trip_start_timestamp,Pickup_grid, Dropoff_grid);

ALTER TABLE daily_grid_activity
ADD FOREIGN KEY (Taxi_start_timestamp, Taxi_pickup_grid, Taxi_dropoff_grid) REFERENCES daily_grid_activity_has_Taxi_2016(Taxi_start_timestamp, Taxi_pickup_grid, Taxi_dropoff_grid);
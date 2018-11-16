CREATE DATABASE IF NOT EXISTS `divvybikes`;

USE `divvybikes`;

CREATE TABLE IF NOT EXISTS `stations` (
	`id` int(11) NOT NULL,
	`stationName` varchar(50) DEFAULT NULL,
	`altitude` varchar(50) DEFAULT NULL,
	`availableBikes` int(11) DEFAULT NULL,
	`availableDocks` int(11) DEFAULT NULL,
	`totalDocks` int(11) DEFAULT NULL,
	`is_renting` boolean DEFAULT NULL,
	`kioskType` varchar(50) DEFAULT NULL,
	`landMark` varchar(50) DEFAULT NULL,
	`lastCommunicationTime` DATETIME DEFAULT NULL,
	`latitude` decimal(10,6) DEFAULT NULL,
	`location` varchar(50) DEFAULT NULL,
	`longitude` decimal(10,6) DEFAULT NULL,
	`city` varchar(50) DEFAULT NULL,
	`postalCode` varchar(50) DEFAULT NULL,
	`stAddress1` varchar(100) DEFAULT NULL,
	`stAddress2` varchar(100) DEFAULT NULL,
	`status` varchar(50) DEFAULT NULL,
	`statusKey` int(11) DEFAULT NULL,
	`statusValue` varchar(50) DEFAULT NULL,
	`testStation` boolean DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `trips` (
	`index` int(11) DEFAULT NULL,
	`trip_id` int(11) DEFAULT NULL,
	`starttime` DATETIME DEFAULT NULL,
	`stoptime` DATETIME DEFAULT NULL,
	`bike_id` int(11) DEFAULT NULL,
	`tripduration` int(11) DEFAULT NULL,
	`from_station_id` int(11) DEFAULT NULL,
    `from_station_name` varchar(50) DEFAULT NULL,
	`to_station_id` int(11) DEFAULT NULL,
    `to_station_name` varchar(50) DEFAULT NULL,
	`usertype` varchar(50) DEFAULT NULL,
	`gender` varchar(50) DEFAULT NULL,
	`birthyear` varchar(50) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `cta_stations` (
	`stop_id` int(11) DEFAULT NULL,
    `direction_id` varchar(50) DEFAULT NULL,
    `stop_name` varchar(50) DEFAULT NULL,
    `station_name` varchar(50) DEFAULT NULL,
    `station_descriptive_name` varchar(100) DEFAULT NULL,
    `station_id` int(11) DEFAULT NULL,
    `ada` varchar(50) DEFAULT NULL,
    `red` varchar(50) DEFAULT NULL,
    `blue` varchar(50) DEFAULT NULL,
    `green` varchar(50) DEFAULT NULL,
    `brown` varchar(50) DEFAULT NULL,
    `pink` varchar(50) DEFAULT NULL,
    `purple` varchar(50) DEFAULT NULL,
    `purple_express` varchar(50) DEFAULT NULL,
    `orange` varchar(50) DEFAULT NULL,
    `yellow` varchar(50) DEFAULT NULL,
    `longitude` decimal(10,6) DEFAULT NULL,
    `latitude` decimal(10,6) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `cta_station_ridership` (
	`station_id` int(11) DEFAULT NULL,
    `stationname` varchar(50) DEFAULT NULL,
	`date` DATETIME DEFAULT NULL,
    `daytype` varchar(50) DEFAULT NULL,
    `rides` int(11) DEFAULT NULL
);

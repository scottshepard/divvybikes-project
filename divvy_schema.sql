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
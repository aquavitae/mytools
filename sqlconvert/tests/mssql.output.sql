USE `master`
;
/****** Object:  Database `Test`    Script Date: 5/14/2015 4:36:54 PM ******/
CREATE DATABASE `Test`;
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC `Test`.`sp_fulltext_database` @action = 'enable'
end
;
USE `Test`
;
/****** Object:  Table `Project`    Script Date: 5/14/2015 4:36:54 PM ******/


CREATE TABLE `Project`(
	`Id` int NOT NULL,
	`Name` varchar(50) NULL,
	`Budget` numeric(18, 2) NULL,
	`Description` varchar(65535) NULL,
	`Author` varchar(50) NULL,
	`Created` datetime NULL,
	`Editor` varchar(50) NULL,
	`Modified` datetime NULL,
PRIMARY KEY
(
	`Id` ASC
)
)
;
USE `master`
;


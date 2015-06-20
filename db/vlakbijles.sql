-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 20, 2015 at 01:02 PM
-- Server version: 5.5.43-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `vlakbijles`
--

-- --------------------------------------------------------

--
-- Table structure for table `level`
--

CREATE TABLE IF NOT EXISTS `level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Table structure for table `offer`
--

CREATE TABLE IF NOT EXISTS `offer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `level_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `unique_index` (`user_id`,`subject_id`,`level_id`),
  KEY `fk_offer_user_idx` (`user_id`),
  KEY `fk_offer_subject_idx` (`subject_id`),
  KEY `fk_offer_level_idx` (`level_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=169 ;

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE IF NOT EXISTS `review` (
  `offer_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `description` text,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`offer_id`),
  UNIQUE KEY `id` (`offer_id`),
  KEY `fk_review_user1_idx` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE IF NOT EXISTS `subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=397 ;

-- --------------------------------------------------------

--
-- Table structure for table `token`
--

CREATE TABLE IF NOT EXISTS `token` (
  `user_id` int(11) NOT NULL,
  `hash` varchar(255) NOT NULL,
  `create_date` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`hash`,`create_date`),
  UNIQUE KEY `hash` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(64) DEFAULT NULL,
  `verified` tinyint(1) DEFAULT NULL,
  `join_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;

-- --------------------------------------------------------

--
-- Table structure for table `user_meta`
--

CREATE TABLE IF NOT EXISTS `user_meta` (
  `user_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `surname` varchar(64) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `zipcode` varchar(20) NOT NULL,
  `city` varchar(100) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `photo_id` varchar(255) NOT NULL,
  `facebook_id` varchar(255) NOT NULL,
  `description` text,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `zipcode`
--

CREATE TABLE IF NOT EXISTS `zipcode` (
  `id` int(11) NOT NULL,
  `zipcode` varchar(7) NOT NULL,
  `zipcode_id` int(10) unsigned NOT NULL,
  `pnum` smallint(4) unsigned NOT NULL,
  `pchar` char(2) NOT NULL,
  `minnumber` mediumint(10) unsigned NOT NULL,
  `maxnumber` mediumint(10) unsigned NOT NULL,
  `numbertype` enum('','mixed','even','odd') NOT NULL,
  `street` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `city_id` smallint(5) unsigned DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `municipality_id` smallint(5) unsigned DEFAULT NULL,
  `province` enum('','Drenthe','Flevoland','Friesland','Gelderland','Groningen','Limburg','Noord-Brabant','Noord-Holland','Overijssel','Utrecht','Zeeland','Zuid-Holland') DEFAULT NULL,
  `province_code` enum('','DR','FL','FR','GE','GR','LI','NB','NH','OV','UT','ZE','ZH') DEFAULT NULL,
  `lat` decimal(15,13) DEFAULT NULL,
  `lon` decimal(15,13) DEFAULT NULL,
  `rd_x` decimal(31,20) DEFAULT NULL,
  `rd_y` decimal(31,20) DEFAULT NULL,
  `location_detail` enum('','exact','postcode','pnum','city') NOT NULL DEFAULT 'postcode',
  `changed_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `postcode_number` (`zipcode_id`,`minnumber`,`maxnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `offer`
--
ALTER TABLE `offer`
  ADD CONSTRAINT `fk_offer_level` FOREIGN KEY (`level_id`) REFERENCES `level` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_offer_subject` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_offer_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `fk_review_offer` FOREIGN KEY (`offer_id`) REFERENCES `offer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_review_user` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `token`
--
ALTER TABLE `token`
  ADD CONSTRAINT `fk_offer_user2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `user_meta`
--
ALTER TABLE `user_meta`
  ADD CONSTRAINT `fk_user_meta_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 13, 2022 at 05:05 AM
-- Server version: 8.0.18
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_machine`
--

-- --------------------------------------------------------

--
-- Table structure for table `historian_data`
--

CREATE TABLE `historian_data` (
  `serial` bigint(20) NOT NULL,
  `ok` bigint(20) NOT NULL,
  `ng` bigint(20) NOT NULL,
  `by_pass` bigint(20) NOT NULL,
  `updated_time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `machine_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `p_date` date NOT NULL,
  `actual_cycle_time` bigint(20) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `production_data`
--

CREATE TABLE `production_data` (
  `serial` bigint(20) NOT NULL,
  `ok` bigint(20) NOT NULL,
  `ng` bigint(20) NOT NULL,
  `by_pass` bigint(20) NOT NULL,
  `toc` bigint(20) DEFAULT NULL,
  `updated_time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `machine_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `p_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `time_data`
--

CREATE TABLE `time_data` (
  `serial` bigint(20) NOT NULL,
  `cycle_time` bigint(20) DEFAULT NULL,
  `idle_time` bigint(20) DEFAULT NULL,
  `updated_time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `machine_id` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `historian_data`
--
ALTER TABLE `historian_data`
  ADD PRIMARY KEY (`serial`);

--
-- Indexes for table `production_data`
--
ALTER TABLE `production_data`
  ADD PRIMARY KEY (`serial`),
  ADD UNIQUE KEY `machine_id` (`machine_id`,`p_date`);

--
-- Indexes for table `time_data`
--
ALTER TABLE `time_data`
  ADD PRIMARY KEY (`serial`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `historian_data`
--
ALTER TABLE `historian_data`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `production_data`
--
ALTER TABLE `production_data`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `time_data`
--
ALTER TABLE `time_data`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

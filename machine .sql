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
-- Database: `machine`
--

-- --------------------------------------------------------

--
-- Table structure for table `display_device`
--

CREATE TABLE `display_device` (
  `serial` int(11) NOT NULL,
  `device_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ip` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cpu` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `disk` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `temp` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `device_time_stamp` datetime NOT NULL,
  `created_time_stamp` timestamp NOT NULL,
  `update_time_stamp` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `online_status`
--

CREATE TABLE `online_status` (
  `id` int(6) UNSIGNED NOT NULL,
  `machine_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ip_address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `product_line` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `live_date` date NOT NULL,
  `live_time` time NOT NULL,
  `reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipc_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `mac_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `subnet` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `default_gateway` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `dns_domain` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `dns_suffix` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `dhcp_enable` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `dhcp_server` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `dhcp_lease_time` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N/A',
  `product_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'UNKNOWN',
  `machine_date_time` varchar(100) COLLATE utf8mb4_general_ci DEFAULT 'MCHINE_DATE_TIME ERROR',
  `last_reboot` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prn_alert`
--

CREATE TABLE `prn_alert` (
  `serial` bigint(20) NOT NULL,
  `device_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `time_stamp` datetime NOT NULL,
  `alert_name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action` text COLLATE utf8mb4_general_ci,
  `action_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `action_by` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prn_data`
--

CREATE TABLE `prn_data` (
  `serial` bigint(20) NOT NULL,
  `device_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `machine_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `process_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `IP` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `CYCLE` bigint(20) NOT NULL,
  `OK` bigint(10) NOT NULL,
  `NG` bigint(10) NOT NULL,
  `time_stamp` datetime NOT NULL,
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Triggers `prn_data`
--
DELIMITER $$
CREATE TRIGGER `after_PrnData_update` AFTER UPDATE ON `prn_data` FOR EACH ROW BEGIN
    IF OLD.OK <> new.OK THEN
       UPDATE prn_target SET prn_target.tok=NEW.OK,prn_target.completed=NEW.OK
       WHERE prn_target.production_date=OLD.date AND prn_target.part_name=OLD.model AND prn_target.machine_name=OLD.machine_name;
    END IF;
       IF OLD.NG <> new.NG THEN
       UPDATE prn_target SET prn_target.tng=NEW.NG
       WHERE prn_target.production_date=OLD.date AND prn_target.part_name=OLD.model AND prn_target.machine_name=OLD.machine_name;
    END IF;
          IF OLD.NG <> new.CYCLE THEN
       UPDATE prn_target SET prn_target.toc=NEW.CYCLE
       WHERE prn_target.production_date=OLD.date AND prn_target.part_name=OLD.model AND prn_target.machine_name=OLD.machine_name;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `prn_device`
--

CREATE TABLE `prn_device` (
  `serial` int(11) NOT NULL,
  `device_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ip` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cpu` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `memory` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `disk` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `temp` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `device_time_stamp` datetime NOT NULL,
  `created_time_stamp` timestamp NOT NULL,
  `update_time_stamp` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prn_device_details`
--

CREATE TABLE `prn_device_details` (
  `serial` bigint(20) NOT NULL,
  `device_model` text COLLATE utf8mb4_general_ci,
  `device_id` text COLLATE utf8mb4_general_ci,
  `org_name` text COLLATE utf8mb4_general_ci,
  `product_line` text COLLATE utf8mb4_general_ci,
  `product_name` text COLLATE utf8mb4_general_ci,
  `product_type` text COLLATE utf8mb4_general_ci,
  `ip_address` text COLLATE utf8mb4_general_ci,
  `usr_id` text COLLATE utf8mb4_general_ci,
  `usr_password` text COLLATE utf8mb4_general_ci,
  `device_key` text COLLATE utf8mb4_general_ci,
  `last_sync` datetime DEFAULT NULL,
  `wifi_ssid` text COLLATE utf8mb4_general_ci,
  `wifi_password` text COLLATE utf8mb4_general_ci,
  `MQTT_enabled` text COLLATE utf8mb4_general_ci,
  `MQTT_IP` text COLLATE utf8mb4_general_ci,
  `MQTT_PORT` text COLLATE utf8mb4_general_ci,
  `HTPP_enabled` text COLLATE utf8mb4_general_ci,
  `HTTP_PORT` text COLLATE utf8mb4_general_ci,
  `INPUT` int(4) DEFAULT NULL,
  `OUTPUT` int(4) DEFAULT NULL,
  `Server_status` text COLLATE utf8mb4_general_ci,
  `time_stamp` datetime DEFAULT NULL,
  `machine_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `process_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `http_ip` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `home_path` text COLLATE utf8mb4_general_ci,
  `API_path` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prn_table`
--

CREATE TABLE `prn_table` (
  `serial` bigint(20) NOT NULL,
  `part_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `part_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `product_model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `product_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `process_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `machine_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `process_cost` int(5) NOT NULL,
  `part_cost` int(5) NOT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `customer` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `ideal_cycle_time` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `prn_target`
--

CREATE TABLE `prn_target` (
  `serial` bigint(20) NOT NULL,
  `order_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `part_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `target` bigint(100) NOT NULL,
  `completed` bigint(100) DEFAULT '0',
  `production_date` date NOT NULL,
  `dispatch_date` date DEFAULT NULL,
  `priority` int(2) DEFAULT NULL,
  `status` varchar(100) COLLATE utf8mb4_general_ci DEFAULT 'PENDING',
  `remark` text COLLATE utf8mb4_general_ci,
  `created_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `edited_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `edited_by` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `toc` bigint(20) DEFAULT '0',
  `tok` bigint(20) DEFAULT '0',
  `tng` bigint(20) DEFAULT '0',
  `device_id` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sync_time_stamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `machine_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sys_update`
--

CREATE TABLE `sys_update` (
  `serial` bigint(11) NOT NULL,
  `device_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `app_update` tinyint(1) DEFAULT NULL,
  `firmware_update` tinyint(1) DEFAULT NULL,
  `data_delete` tinyint(1) DEFAULT NULL,
  `db_backup` tinyint(1) DEFAULT NULL,
  `log_backup` tinyint(1) DEFAULT NULL,
  `app_backup` tinyint(1) DEFAULT NULL,
  `device_data_update` tinyint(1) DEFAULT NULL,
  `part_delete` tinyint(1) DEFAULT NULL,
  `part_update` tinyint(1) DEFAULT NULL,
  `created_time_stamp` timestamp NULL DEFAULT NULL,
  `updated_time_stamp` timestamp NULL DEFAULT NULL,
  `version` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `display_device`
--
ALTER TABLE `display_device`
  ADD PRIMARY KEY (`serial`);

--
-- Indexes for table `online_status`
--
ALTER TABLE `online_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `machine_name` (`machine_name`,`ip_address`,`product_line`);

--
-- Indexes for table `prn_alert`
--
ALTER TABLE `prn_alert`
  ADD PRIMARY KEY (`serial`);

--
-- Indexes for table `prn_data`
--
ALTER TABLE `prn_data`
  ADD PRIMARY KEY (`serial`);

--
-- Indexes for table `prn_device`
--
ALTER TABLE `prn_device`
  ADD PRIMARY KEY (`serial`),
  ADD UNIQUE KEY `device_id` (`device_id`);

--
-- Indexes for table `prn_device_details`
--
ALTER TABLE `prn_device_details`
  ADD PRIMARY KEY (`serial`);

--
-- Indexes for table `prn_table`
--
ALTER TABLE `prn_table`
  ADD PRIMARY KEY (`serial`),
  ADD UNIQUE KEY `part_name` (`part_name`),
  ADD UNIQUE KEY `part_id` (`part_id`);

--
-- Indexes for table `prn_target`
--
ALTER TABLE `prn_target`
  ADD PRIMARY KEY (`serial`),
  ADD UNIQUE KEY `unique_index` (`part_name`,`production_date`,`machine_name`);

--
-- Indexes for table `sys_update`
--
ALTER TABLE `sys_update`
  ADD PRIMARY KEY (`serial`),
  ADD UNIQUE KEY `device_id` (`device_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `display_device`
--
ALTER TABLE `display_device`
  MODIFY `serial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `online_status`
--
ALTER TABLE `online_status`
  MODIFY `id` int(6) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prn_alert`
--
ALTER TABLE `prn_alert`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prn_data`
--
ALTER TABLE `prn_data`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prn_device`
--
ALTER TABLE `prn_device`
  MODIFY `serial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prn_device_details`
--
ALTER TABLE `prn_device_details`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prn_table`
--
ALTER TABLE `prn_table`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `prn_target`
--
ALTER TABLE `prn_target`
  MODIFY `serial` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sys_update`
--
ALTER TABLE `sys_update`
  MODIFY `serial` bigint(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

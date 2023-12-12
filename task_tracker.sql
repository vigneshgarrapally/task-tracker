-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 10, 2023 at 11:54 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `task_tracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `Comments`
--

CREATE TABLE `Comments` (
  `CommentID` int(11) NOT NULL,
  `TaskID` int(11) NOT NULL,
  `Comment` text DEFAULT NULL,
  `UserID` int(11) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Comments`
--

INSERT INTO `Comments` (`CommentID`, `TaskID`, `Comment`, `UserID`, `CreatedAt`) VALUES
(5, 2, 'This is a sample comment\r\n', 2, '2023-12-10 22:47:50'),
(6, 2, 'Xampp installation is pending', 2, '2023-12-10 22:48:47');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`id`, `username`, `email`, `password_hash`) VALUES
(1, 'Vignesh', 'garrapallyvignesh8055@gmail.com', '$2b$12$iMuE7uW/gUrfFhTlFmQK8OVLHdbfqoTQXX9S/ubUyDhFqIx3DAsAG'),
(2, 'Shirisha', 'Shirisha@gmail.com', '$2b$12$dhi/e3CIwYg8Ubby9pgUMeHHOpZ4TwVHEXdKzG4diWEyMofzq3uEK');

-- --------------------------------------------------------

--
-- Table structure for table `Tasks`
--

CREATE TABLE `Tasks` (
  `TaskID` int(11) NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Description` text DEFAULT NULL,
  `Status` enum('Pending','In Progress','Completed') NOT NULL DEFAULT 'Pending',
  `Priority` enum('Low','Medium','High') NOT NULL DEFAULT 'Medium',
  `Category` varchar(100) DEFAULT NULL,
  `AssignedTo` int(11) DEFAULT NULL,
  `DueDate` date DEFAULT NULL,
  `CreatedBy` int(11) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Tasks`
--

INSERT INTO `Tasks` (`TaskID`, `Title`, `Description`, `Status`, `Priority`, `Category`, `AssignedTo`, `DueDate`, `CreatedBy`, `CreatedAt`) VALUES
(2, 'Create Front end for database project', 'Add html code\r\ninstall ampp', 'Pending', 'High', 'Frontend', 2, '2023-12-12', 2, '2023-12-10 13:05:35'),
(3, 'Test task', 'Description', 'In Progress', 'Low', 'Database Systems', 2, '2023-12-13', 2, '2023-12-10 14:40:54'),
(4, 'Test task', 'Description', 'Completed', 'Low', 'Database Systems', 2, '2023-12-13', 2, '2023-12-10 14:41:00'),
(5, 'Test task', 'Description', 'Completed', 'Low', 'Database Systems', 2, '2023-12-13', 2, '2023-12-10 14:41:08');

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `UserID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`UserID`, `Username`, `Email`, `Password`, `CreatedAt`) VALUES
(2, 'abc', 'abc@gmail.com', '$2b$12$dtm2b9qa3gCHxZobph7ZnOHDkZa2XLuc0EaGxHn78FTRUO9k1t/FO', '2023-12-10 12:52:10'),
(3, 'Varun', 'varun@gamil.com', '$2b$12$3CLZOJAagGjhg5ytk5s2t.L.lkkMGinQdY/hk5OjNPELcakoB4hzy', '2023-12-10 17:19:47');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Comments`
--
ALTER TABLE `Comments`
  ADD PRIMARY KEY (`CommentID`),
  ADD KEY `TaskID` (`TaskID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `Tasks`
--
ALTER TABLE `Tasks`
  ADD PRIMARY KEY (`TaskID`),
  ADD KEY `AssignedTo` (`AssignedTo`),
  ADD KEY `CreatedBy` (`CreatedBy`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`UserID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Comments`
--
ALTER TABLE `Comments`
  MODIFY `CommentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Tasks`
--
ALTER TABLE `Tasks`
  MODIFY `TaskID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `UserID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Comments`
--
ALTER TABLE `Comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`TaskID`) REFERENCES `Tasks` (`TaskID`),
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `Users` (`UserID`);

--
-- Constraints for table `Tasks`
--
ALTER TABLE `Tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`AssignedTo`) REFERENCES `Users` (`UserID`),
  ADD CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`CreatedBy`) REFERENCES `Users` (`UserID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

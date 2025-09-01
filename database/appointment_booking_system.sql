-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 01, 2025 at 06:37 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appointment_booking_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `doctor_name` varchar(100) NOT NULL,
  `patient_name` varchar(100) NOT NULL,
  `Dob` date NOT NULL,
  `Gender` varchar(100) NOT NULL,
  `Age` int(10) NOT NULL,
  `Specialization` varchar(100) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `Hospital_name` varchar(500) NOT NULL,
  `Hospital_address` varchar(2000) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `medical_records` varchar(300) NOT NULL,
  `status` enum('Pending','Confirmed','Cancelled') DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `appointment_history`
--

CREATE TABLE `appointment_history` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `doctor_name` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `reason_for_booking` text DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `appointment_date` date DEFAULT NULL,
  `appointment_time` time DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Completed',
  `consultation` varchar(2000) NOT NULL,
  `medical_record` varchar(500) NOT NULL,
  `prescription` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointment_history`
--

INSERT INTO `appointment_history` (`id`, `patient_id`, `doctor_id`, `patient_name`, `doctor_name`, `age`, `specialization`, `reason_for_booking`, `dob`, `appointment_date`, `appointment_time`, `gender`, `amount`, `status`, `consultation`, `medical_record`, `prescription`) VALUES
(1, 1, 5, 'Pratheesh Vel K', 'Dr. VijayKumar', 30, 'Endroconologist', 'Regular Check Up', '0000-00-00', '2025-08-19', '19:30:00', 'Male', 550.00, 'completed', 'Drink more water', '', ''),
(6, 3, 2, 'Shalini', 'Dr. Thiru', 30, 'Oncologist', 'General checkup', '2025-08-08', '2025-08-31', '18:58:00', 'Female', 300.00, 'completed', 'Drink more water.', 'uploads/medical_records/Sleep_tracking (1)_20250901190749556463.docx', 'uploads/prescriptions/Timetable_20250901190749556463.docx');

-- --------------------------------------------------------

--
-- Table structure for table `cancelled_appointments`
--

CREATE TABLE `cancelled_appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `patient_name` varchar(255) NOT NULL,
  `doctor_name` varchar(255) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `specialization` varchar(255) DEFAULT NULL,
  `reason_for_booking` text DEFAULT NULL,
  `reason_for_cancelling` text DEFAULT NULL,
  `status` varchar(200) NOT NULL,
  `dob` date DEFAULT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT 'Other',
  `cancelled_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cancelled_appointments`
--

INSERT INTO `cancelled_appointments` (`id`, `patient_id`, `doctor_id`, `patient_name`, `doctor_name`, `age`, `specialization`, `reason_for_booking`, `reason_for_cancelling`, `status`, `dob`, `appointment_date`, `appointment_time`, `gender`, `cancelled_at`) VALUES
(1, 4, 1, 'Karthick G', 'Dr. Malini', 25, 'Cardiologist', 'General Check up', 'Not Available at that date', 'Cancelled', '2025-08-19', '2025-08-22', '17:17:00', 'Male', '2025-08-18 10:57:22'),
(2, 2, 4, 'Sugathesh K', 'Dr. Jeyam', 25, 'Endocrinologist', 'Check up', 'Doctor on Vacation', 'Cancelled', '2025-08-21', '2025-08-30', '15:25:00', 'Male', '2025-08-18 13:31:50');

-- --------------------------------------------------------

--
-- Table structure for table `deleted_doctors`
--

CREATE TABLE `deleted_doctors` (
  `id` int(11) NOT NULL,
  `Doctor_name` varchar(255) NOT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(50) DEFAULT NULL,
  `Specialization` varchar(255) DEFAULT NULL,
  `Experience` varchar(50) DEFAULT NULL,
  `Address_line1` varchar(255) DEFAULT NULL,
  `Address_line2` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Hospital_name` varchar(255) DEFAULT NULL,
  `Hospital_address` varchar(255) DEFAULT NULL,
  `deletion_reason` varchar(500) DEFAULT NULL,
  `deleted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `deleted_doctors`
--

INSERT INTO `deleted_doctors` (`id`, `Doctor_name`, `DOB`, `Gender`, `Specialization`, `Experience`, `Address_line1`, `Address_line2`, `Email`, `Phone`, `Hospital_name`, `Hospital_address`, `deletion_reason`, `deleted_at`) VALUES
(2, 'Dr. Kalyani', '2001-12-24', 'Female', 'Neurologist', '3', '34, Main road', 'T nagar, Chennai', 'kalyani@gmail.com', '8907221345', 'WellNew Hospital', '1 st tower street, Kanchipuram', 'She is on medical leave .But no response regarding the leave.', '2025-08-20 16:39:21');

-- --------------------------------------------------------

--
-- Table structure for table `deleted_patients`
--

CREATE TABLE `deleted_patients` (
  `id` int(11) NOT NULL,
  `Patient_name` varchar(150) NOT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(20) DEFAULT NULL,
  `Marital_status` varchar(30) DEFAULT NULL,
  `Email` varchar(100) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address_line1` varchar(255) DEFAULT NULL,
  `Address_line2` varchar(255) DEFAULT NULL,
  `deletion_reason` text DEFAULT NULL,
  `deleted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `deleted_patients`
--

INSERT INTO `deleted_patients` (`id`, `Patient_name`, `DOB`, `Gender`, `Marital_status`, `Email`, `Phone`, `Address_line1`, `Address_line2`, `deletion_reason`, `deleted_at`) VALUES
(1, 'Kavitha v', '0000-00-00', '2000-06-15', 'kavitha@gmail.com', '9087651234', '34, Main road', 'Kancheepuram', 'kavi@123', 'Not yet booked appointments', '2025-08-21 10:03:19'),
(6, 'Amaljith', '0000-00-00', '2025-08-16', 'amal@gmail.com', '9870563421', '15 street', 'tiruppur', 'temp123', 'Fake Account', '2025-08-21 10:55:50');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_register`
--

CREATE TABLE `doctor_register` (
  `Id` int(11) NOT NULL,
  `Doctor_name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Confirm_password` varchar(100) NOT NULL,
  `Specialization` varchar(50) NOT NULL,
  `Experience` int(2) NOT NULL,
  `Dob` date NOT NULL,
  `Gender` varchar(20) NOT NULL,
  `Address_line1` varchar(500) NOT NULL,
  `Address_line2` varchar(500) NOT NULL,
  `Phone` bigint(10) NOT NULL,
  `Hospital_name` varchar(500) NOT NULL,
  `Hospital_address` varchar(500) NOT NULL,
  `About` varchar(4000) NOT NULL,
  `Profile_picture` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_register`
--

INSERT INTO `doctor_register` (`Id`, `Doctor_name`, `Email`, `Password`, `Confirm_password`, `Specialization`, `Experience`, `Dob`, `Gender`, `Address_line1`, `Address_line2`, `Phone`, `Hospital_name`, `Hospital_address`, `About`, `Profile_picture`) VALUES
(1, 'Dr. Malini', 'malini@gmail.com', 'Malini@123', 'Malini@123', 'Cardiologist', 5, '0000-00-00', 'Female', 'Main road', 'Chennai', 9087654321, 'Wellcare hospital', 'Coimbatore', 'Well trained', 'doc16.png'),
(2, 'Dr. Thiru', 'thiru@gmail.com', 'temp123', 'temp123', 'Oncologist', 5, '2025-08-15', 'Male', 'Kovil street', 'chennai', 8907654328, 'Jeyam Hospital', '17 C, First Avenue street, KanyaKumari', 'Well experienced', 'doc8.png'),
(4, 'Dr. Jeyam', 'jeyam@gmail.com', '1234', '1234', 'Endocrinologist', 4, '2025-08-13', 'Male', '17 C, First Avenue street, KanyaKumari', 'chennai', 7890543278, 'Jeyam Hospital', '17 C, First Avenue street, KanyaKumari', 'Well trained', 'doc6.png'),
(5, 'Dr. VijayKumar', 'vijaykumar09@gmail.com', 'vijay@123', 'vijay@123', 'Endocrinologist', 9, '1991-07-19', 'Male', '56-A , Arch Street', 'Thiruvaiyaar, Tiruppur', 9087654328, 'Bethel Hospital', '67(C)/112, Croos cut Street, NagarKoil', 'Well experienced and well trained', 'doc7.png'),
(8, 'Dr. Sneha', 'sneha1278@gmail.com', 'sneha123', 'sneha123', 'Neurologist', 3, '1994-06-22', 'Female', '254, T- Nagar , Thambaram', 'Chennai', 9012347865, 'NiceCare Hospital', 'Kancheepuram , Chennai', 'Dr. Sneha is a dedicated neurologist at NiceCare Hospital with 3 years of experience in diagnosing and treating neurological conditions. She is committed to providing compassionate care and ensuring the well-being of her patients through advanced medical practices and personalized treatment plans.', 'Sneha.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `patient_medical_records`
--

CREATE TABLE `patient_medical_records` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `record_name` varchar(255) DEFAULT NULL,
  `record_path` varchar(255) DEFAULT NULL,
  `uploaded_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_medical_records`
--

INSERT INTO `patient_medical_records` (`id`, `patient_id`, `record_name`, `record_path`, `uploaded_date`) VALUES
(1, 3, 'APTITUDE TEST-5.pdf', 'uploads/patient_records/APTITUDE TEST-5.pdf', '2025-09-01');

-- --------------------------------------------------------

--
-- Table structure for table `patient_register`
--

CREATE TABLE `patient_register` (
  `id` int(11) NOT NULL,
  `Patient_name` varchar(100) NOT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Dob` date DEFAULT NULL,
  `Email` varchar(100) NOT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `Address_line1` varchar(255) DEFAULT NULL,
  `Address_line2` varchar(255) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `Confirm_password` varchar(255) NOT NULL,
  `Profile_image` varchar(255) DEFAULT NULL,
  `Marital_Status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_register`
--

INSERT INTO `patient_register` (`id`, `Patient_name`, `Gender`, `Dob`, `Email`, `Phone`, `Address_line1`, `Address_line2`, `Password`, `Confirm_password`, `Profile_image`, `Marital_Status`) VALUES
(1, 'Pratheesh Vel K', 'Female', '2021-11-22', 'pratheesh@gmail.com', '8976543210', '6/112, East Street', 'Athisayapuram,tenksai', 'temp@123', 'temp@123', 'IMG_20210408_142220.jpg', 'Single'),
(2, 'Sugathesh K', 'Female', '2025-08-11', 'suga@gmail.com', '9087654321', 'Madurai main road', 'tenkasi', 'Suga@123', 'Suga@123', 'IMG_20230623_131030.jpg', 'Single'),
(3, 'Shalini', 'Female', '2025-08-20', 'shalini@gmail.com', '9087651234', '17 th Street, Anna Nagar', 'Tirunelveli', 'shalini@123', 'shalini@123', 'shalini.jpg', 'Single'),
(4, 'Karthick G', 'Male', '2005-05-20', 'karthi@gmail.com', '9870652341', '67(Q), First Cross street , Kamaraj nagar', 'KanyaKumari', 'Karthi@123', 'Karthi@123', 'karthick.jpg', 'Single');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appointment_history`
--
ALTER TABLE `appointment_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cancelled_appointments`
--
ALTER TABLE `cancelled_appointments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deleted_doctors`
--
ALTER TABLE `deleted_doctors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deleted_patients`
--
ALTER TABLE `deleted_patients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctor_register`
--
ALTER TABLE `doctor_register`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `patient_medical_records`
--
ALTER TABLE `patient_medical_records`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patient_register`
--
ALTER TABLE `patient_register`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `appointment_history`
--
ALTER TABLE `appointment_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `cancelled_appointments`
--
ALTER TABLE `cancelled_appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `deleted_doctors`
--
ALTER TABLE `deleted_doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `deleted_patients`
--
ALTER TABLE `deleted_patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `doctor_register`
--
ALTER TABLE `doctor_register`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `patient_medical_records`
--
ALTER TABLE `patient_medical_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `patient_register`
--
ALTER TABLE `patient_register`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

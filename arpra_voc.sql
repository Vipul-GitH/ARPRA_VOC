-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Jan 21, 2026 at 11:43 AM
-- Server version: 8.4.7
-- PHP Version: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `arpra_voc`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `bookingid` bigint NOT NULL,
  `customername` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `slot` varchar(100) DEFAULT NULL,
  `mobile` varchar(50) DEFAULT NULL,
  `isCampaingsend` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`bookingid`, `customername`, `dob`, `slot`, `mobile`, `isCampaingsend`) VALUES
(157593, 'DEEPAK KUMAR', '0001-01-01', '21/01/2026', '7991129661', 0),
(157788, 'SUNITA SHARMA', '2026-01-17', '21/01/2026', '8700191106', 0),
(157851, 'DINESH ', '2026-01-17', '21/01/2026', '8146945626 ', 0),
(157913, 'KARAN KUMAR  BHATIA  +1', '0001-01-01', '21/01/2026', '9999533753', 0),
(158003, 'RAJIV N SAHAYA ( EXPERT TECHNICIAN)', '2025-12-19', '21/01/2026', '9717200511', 0),
(158055, 'SUNITA ', '0001-01-01', '21/01/2026', '9899666270', 0),
(158071, 'ANITA + PARKASH ', '2026-01-19', '21/01/2026', '9810871473 ', 0),
(158072, 'BRIJ MOHAN +1', '2026-01-20', '21/01/2026', '8700378967', 0),
(158082, 'BIDYA GANGOPADHYAY', '0001-01-01', '21/01/2026', '9968406341', 0),
(158096, 'SUNIL KAPOOR    ', '2025-10-23', '21/01/2026', '9811514188', 0),
(158114, 'LAJJA WATI', '0001-01-01', '21/01/2026', '9911201605', 0),
(158118, 'REENA BHARTIA  (SEND EXPE TECH)', '2025-12-01', '21/01/2026', '9871472504', 0),
(158120, 'Muniraj meena', '0001-01-01', '21/01/2026', '8058502195', 0),
(158123, 'SANTRA DEVI', '0001-01-01', '21/01/2026', '8307527067 ', 0),
(158128, 'SUMAN MISHRA ', '2026-01-20', '21/01/2026', '8287020086', 0),
(158132, ' Bala devi+1', '2026-01-20', '21/01/2026', '9910125857', 0),
(158133, 'PAYAL', '0001-01-02', '21/01/2026', '8527505188', 0),
(158137, 'RAJVIR ', '2026-01-20', '21/01/2026', '8851773764', 0),
(158138, 'SEEMA ', '0001-01-01', '21/01/2026', '7982399853', 0),
(158139, 'BHOLA MAHTO ', '0001-01-01', '21/01/2026', '7982059777', 0),
(158140, 'SHIKHA ', '0001-01-01', '21/01/2026', '8384007098', 0),
(158142, 'SHEELA ', '0001-01-01', '21/01/2026', '8929260019', 0),
(158144, 'MATHI BAI  ', '0001-01-01', '21/01/2026', '9953333679', 0),
(158146, 'BALVINDER KAUR', '0001-01-01', '21/01/2026', '8076565757', 0),
(158147, 'AJAY PATWAL', '0001-01-01', '21/01/2026', '9999191494', 0),
(158148, 'RANI GANGULI + SERVANT ', '0001-01-01', '21/01/2026', '9873491814', 0),
(158150, 'Saurabh  9205353670', '0001-01-01', '21/01/2026', '9971057393', 0),
(158152, 'Devinder pal', '2026-01-20', '21/01/2026', '7042763050', 0),
(158155, 'MANOHAR LAL ', '2026-01-20', '21/01/2026', '8104788650', 0),
(158157, 'SUNITA DEVI', '0001-01-01', '21/01/2026', '9166202219', 0),
(158158, 'MANGAL VISHNU BITHARE', '0001-01-01', '21/01/2026', '9834353755', 0),
(158159, 'RAJENDRA KUMAR', '1985-06-05', '21/01/2026', '8527573113', 0),
(158161, 'SAVITRI  DEVI ', '0001-01-01', '21/01/2026', '9953826170', 0),
(158162, 'HIRA RAM', '0001-01-01', '21/01/2026', '9910126919', 0),
(158163, 'UMA passi  +', '0001-01-01', '21/01/2026', '9953113103', 0),
(158164, 'MRS. SHIVA PANDEY', '0001-01-01', '21/01/2026', '9312223857', 0),
(158166, 'SURESH MEHTA', '0001-01-01', '21/01/2026', '9310632864', 0),
(158168, 'SEEMA', '0001-01-01', '21/01/2026', '7303346038', 0),
(158171, 'SRIKALA ,S', '0001-01-01', '21/01/2026', '9868023348', 0),
(158173, 'BHARAT BHUSHAN KHANNA', '0001-01-01', '21/01/2026', '9818255034', 0),
(158174, 'SHILPA  KARIWALA', '0001-01-01', '21/01/2026', '9312962468', 0),
(158175, 'SHYAM SUNDAR', '0001-01-01', '21/01/2026', '8860794004', 0),
(158177, 'SURENDER SINGH MAHALWAL', '0001-01-01', '21/01/2026', '9999166896 ', 0),
(158179, 'JANKI DEVI ', '0001-01-01', '21/01/2026', '9968091842', 0),
(158180, 'C Neera', '2026-01-20', '21/01/2026', '9810083715', 0),
(158181, 'O P  WALECHA + RENU NAGPAL (DEEP VEINS ASSIGN VISHVENDER ONLY)', '2025-11-07', '21/01/2026', '9811673868', 0),
(158182, 'SUNIL KUMAR', '0001-01-01', '21/01/2026', '7703967105', 0),
(158183, 'Babita', '0001-01-01', '21/01/2026', '8595169675', 0),
(158185, 'Gelden Samdup Wangchuk/30 yrs/ M', '2025-09-23', '21/01/2026', '9717755296', 0),
(158186, 'SADHVI MRIGAWATI JI, + 2', '0001-01-01', '21/01/2026', '9810021581', 0),
(158187, 'NARENDER MAKKAR', '2025-11-29', '21/01/2026', '9871982508', 0),
(158189, 'Deepa', '0001-01-01', '21/01/2026', '9518104036', 0),
(158191, 'Vishnu  9718665055', '0001-01-01', '21/01/2026', '9971057393', 0),
(158193, 'SATYA  ', '0001-01-01', '21/01/2026', '8178847636', 0),
(158195, 'VED PRAKASH +1', '0001-01-01', '21/01/2026', '8800723972', 0),
(158196, 'APARNA ROY CHOUDHARY', '0001-01-01', '21/01/2026', '9911553281', 0),
(158197, 'Lajpat Nagar Evoke', '2026-01-13', '21/01/2026', '9205111408', 0),
(158198, 'KRITIKA TARUN', '0001-01-01', '21/01/2026', '9711183213', 0),
(158200, 'RANJIT KAPOOR ', '2025-11-06', '21/01/2026', '9891106461', 0),
(158201, 'CHARU  MEHTA ', '0001-01-01', '21/01/2026', '9811373990', 0),
(158202, 'NIRMALA  (EXP TECH)', '0001-01-01', '21/01/2026', '9910935201', 0),
(158203, 'KAMLESH CHANDRA ANEJA  ', '0001-01-01', '21/01/2026', '9818247979', 0),
(158205, 'RAMA RAINA ', '2025-10-24', '21/01/2026', '9871681980', 0),
(158207, 'DR YACHNA GROVER clinic', '2022-04-16', '21/01/2026', '9810116471', 0),
(158208, 'KIRAN KHANNA', '0001-01-01', '21/01/2026', '8826362926', 0),
(158209, 'Lilmani ratti ', '2026-01-20', '21/01/2026', '9217148355', 0),
(158212, 'Hadaya ', '1994-01-01', '21/01/2026', '9918433786', 0),
(158214, ' kript Kaur ', '2026-01-21', '21/01/2026', '9650204399', 0),
(158215, 'SAVITA BHATIA ', '2025-09-28', '21/01/2026', '9990072751', 0),
(158217, 'ASHIMA ', '1994-01-01', '21/01/2026', '9971365677', 0),
(158219, 'SUSHMA  CHOPRA +1', '2025-11-03', '21/01/2026', '9958607066', 0),
(158220, 'S C ROY AND ANITA ROY ', '1949-11-15', '21/01/2026', '9899804301', 0),
(158222, 'srishti manocha', '2025-10-24', '21/01/2026', '9958693600', 0),
(158224, 'RAKESH + SHANKUTLA ', '2026-01-20', '21/01/2026', '9582150331 ', 0),
(158226, 'RAJWATI ', '2025-09-27', '21/01/2026', '8447494474', 0),
(158228, 'SRIKALA ,S', '0001-01-01', '21/01/2026', '9868023348', 0),
(158229, 'C Neera', '2026-01-20', '2026-01-21', '9810083715', 0),
(158230, 'KAMLESH CHANDRA ANEJA  ', '0001-01-01', '21/01/2026', '9818247979', 0),
(158231, 'SUNIL KAPOOR    ', '2025-10-23', '21/01/2026', '9811514188', 0),
(158232, 'DINESH ', '2026-01-17', '21/01/2026', '8146945626 ', 0),
(158233, 'RAJENDRA KUMAR', '1985-06-05', '21/01/2026', '8527573113', 0),
(158234, 'LAJJA WATI', '0001-01-01', '21/01/2026', '9911201605', 0),
(158235, 'ANITA + PARKASH ', '2026-01-19', '21/01/2026', '9810871473 ', 0),
(158236, 'BHARAT BHUSHAN KHANNA', '0001-01-01', '21/01/2026', '9818255034', 0),
(158238, 'SUMAN MISHRA ', '2026-01-20', '2026-01-21', '8287020086', 0),
(158239, 'SEEMA ', '0001-01-01', '21/01/2026', '7982399853', 0),
(158240, 'BHOLA MAHTO ', '0001-01-01', '21/01/2026', '7982059777', 0),
(158241, ' pooja kumari ', '2026-01-21', '21/01/2026', '8210235352', 0),
(158242, 'SUNITA ', '0001-01-01', '21/01/2026', '9899666270', 0),
(158243, 'BALVINDER KAUR', '0001-01-01', '21/01/2026', '8076565757', 0),
(158244, 'APARNA ROY CHOUDHARY', '0001-01-01', '21/01/2026', '9911553281', 0),
(158245, 'SUNITA SHARMA', '2026-01-17', '21/01/2026', '8700191106', 0),
(158247, 'NIRMALA  (EXP TECH)', '0001-01-01', '21/01/2026', '9910935201', 0),
(158248, 'SANTRA DEVI', '0001-01-01', '21/01/2026', '8307527067 ', 0),
(158253, 'DURGA DEVI ', '2025-10-06', '21/01/2026', '8178137943', 0),
(158254, 'BRIJ MOHAN +1', '2026-01-20', '21/01/2026', '8700378967', 0),
(158255, 'D K THAKUR ', '0001-01-01', '21/01/2026', '9911302674', 0),
(158257, 'SHILPA  KARIWALA', '0001-01-01', '21/01/2026', '9312962468', 0),
(158258, 'KAMLESH GUPTA', '0001-01-01', '21/01/2026', '9899003979', 0),
(158259, 'RAMA RAINA ', '2025-10-24', '21/01/2026', '9871681980', 0),
(158262, 'CHANDERKANTA', '0001-01-01', '21/01/2026', '9871116232', 0),
(158264, 'Gelden Samdup Wangchuk/30 yrs/ M', '2025-09-23', '21/01/2026', '9717755296', 0),
(158266, 'SAVITRI  DEVI ', '0001-01-01', '21/01/2026', '9953826170', 0),
(158270, 'ABHIJEET SAHA ', '0001-01-01', '21/01/2026', '9899034655', 0),
(158271, 'MANJU ', '2026-01-21', '21/01/2026', '9910135944', 0),
(158273, 'ARVIND SHARMA', '2026-01-19', '21/01/2026', '7982276413', 0),
(158277, ' GITIKA ', '0001-01-01', '21/01/2026', '9819443843', 0),
(158285, 'B N MAGON ', '0001-01-01', '21/01/2026', '9718377513', 0),
(158287, 'NAMAN PANDEY ', '0001-01-01', '21/01/2026', '8700197447', 0),
(158288, 'R K  AGARWAL', '2025-11-15', '21/01/2026', '7542030167', 0),
(158293, 'HARI PAUL BHARI ', '2022-05-31', '21/01/2026', '9811238001', 0),
(158295, 'Shagun soni', '0001-01-01', '21/01/2026', '7289000663', 0),
(158296, 'MUKESH ', '2026-01-16', '21/01/2026', '9899683930', 0),
(158298, 'Shresth', '0001-01-01', '21/01/2026', '6386404163', 0),
(158302, 'MANGAL VISHNU BITHARE', '0001-01-01', '21/01/2026', '9834353755', 0),
(158303, 'LAXMI SINGH ', '0001-01-01', '21/01/2026', '9311212937', 0),
(158318, 'BONUS COLLECTION', '0001-01-01', '21/01/2026', '9311193111', 0);

-- --------------------------------------------------------

--
-- Table structure for table `campaigns`
--

CREATE TABLE `campaigns` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(100) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `campaign_type` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `primary_language` varchar(10) DEFAULT NULL,
  `available_languages` json DEFAULT NULL,
  `layout_type` varchar(50) DEFAULT NULL,
  `estimated_fill_time_seconds` int DEFAULT NULL,
  `header_title` varchar(255) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `is_forever` tinyint(1) DEFAULT NULL,
  `max_score` int DEFAULT NULL,
  `scoring_method` varchar(50) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `exp_flow_map` json DEFAULT NULL,
  `thank_you_title` varchar(255) DEFAULT NULL,
  `thank_you_message` text,
  `thank_you_image_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `campaigns`
--

INSERT INTO `campaigns` (`id`, `name`, `code`, `description`, `campaign_type`, `status`, `primary_language`, `available_languages`, `layout_type`, `estimated_fill_time_seconds`, `header_title`, `start_date`, `end_date`, `is_forever`, `max_score`, `scoring_method`, `created_by`, `created_at`, `updated_at`, `exp_flow_map`, `thank_you_title`, `thank_you_message`, `thank_you_image_url`) VALUES
(2, 'GK1 WALK IN ', 'FB001', 'None', 'walk_in', 'draft', 'en', '[\"en\"]', 'one_question_per_page', 60, NULL, NULL, NULL, 1, NULL, 'simple_avg', 1, '2025-12-23 07:30:13', '2025-12-24 06:18:14', '{\"1\": [8, 10, 14], \"2\": [14], \"3\": [12, 13, 14], \"4\": [8], \"5\": [4, 3, 5, 6, 7, 8]}', 'Thank You', 'Thank you for your honest feedback.\r\nYour voice helps us strengthen our commitment to care, accuracy, and empathy.\r\nWe’re grateful you chose Dr Bhasin’s Lab and trusted us with your health.', NULL),
(3, 'OVERALL EXPERIENCE', 'CODE_1', 'None', 'walk_in', 'draft', 'en', '[\"en\"]', 'one_question_per_page', 60, 'OVERALL EXPERIENCE', NULL, NULL, 1, NULL, 'simple_avg', 1, '2026-01-13 12:22:13', '2026-01-21 11:36:05', '{\"1\": [26, 27], \"2\": [26, 27], \"3\": [22, 23, 24, 25], \"4\": [16, 18, 19, 20, 21], \"5\": [16, 18, 19, 20, 21]}', 'Thank You', 'Thank you for taking the time to share your experience with us.\r\nYour feedback truly matters and helps us care better for every patient we serve.\r\nWe appreciate the trust you’ve placed in Dr Bhasin’s Lab.', NULL),
(4, ' HOME SAMPLE COLLECTION – PATIENT FEEDBACK', 'CODE_2', 'None', 'walk_in', 'draft', 'en', '[\"en\"]', 'one_question_per_page', 60, 'Patient Feedback', NULL, NULL, 1, NULL, 'simple_avg', 1, '2026-01-13 13:02:10', '2026-01-21 11:33:27', '{\"1\": [37, 38, 39], \"2\": [37, 38, 39], \"3\": [34, 35, 36], \"4\": [29, 30, 31, 33], \"5\": [29, 30, 31, 32, 33]}', 'Thank-You', 'Thank you for inviting us into your home and sharing your feedback.\r\nYour trust matters deeply to us, and your inputs help us improve how we care for you and other patients.', NULL),
(10, 't', 't', NULL, 'walk_in', 'draft', 'en', '[\"en\"]', 'one_question_per_page', 60, 't', NULL, NULL, 1, NULL, 'simple_avg', 1, '2026-01-21 11:39:24', '2026-01-21 11:41:37', '{\"1\": [57, 58, 59], \"2\": [57, 58, 59], \"3\": [57, 58, 59], \"4\": [57, 58, 59], \"5\": [57, 58, 59]}', NULL, 'ok', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `campaign_channels`
--

CREATE TABLE `campaign_channels` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `channel_id` int NOT NULL,
  `config` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `campaign_pii_fields`
--

CREATE TABLE `campaign_pii_fields` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `pii_field_id` int NOT NULL,
  `is_required` tinyint(1) DEFAULT NULL,
  `prefill_source` varchar(100) DEFAULT NULL,
  `display_label` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `campaign_questions`
--

CREATE TABLE `campaign_questions` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `master_question_id` int DEFAULT NULL,
  `question_text_en` varchar(1000) DEFAULT NULL,
  `question_text_hi` varchar(1000) DEFAULT NULL,
  `question_type` varchar(50) NOT NULL,
  `placeholder_en` varchar(255) DEFAULT NULL,
  `is_required` tinyint(1) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `page_number` int DEFAULT NULL,
  `is_master` tinyint(1) DEFAULT NULL,
  `is_overall_rating` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `campaign_questions`
--

INSERT INTO `campaign_questions` (`id`, `campaign_id`, `master_question_id`, `question_text_en`, `question_text_hi`, `question_type`, `placeholder_en`, `is_required`, `order_index`, `page_number`, `is_master`, `is_overall_rating`) VALUES
(2, 2, 1, 'Overall, how would you rate your experience with Dr Bhasin’s Lab?', NULL, 'rating_1_5', NULL, 1, 1, 1, 1, 1),
(3, 2, 3, 'How likely are you to recommend Dr Bhasin’s Lab for the care, comfort, and confidence you experienced?', NULL, 'mcq_single', NULL, 0, 3, 1, 1, 0),
(4, 2, NULL, 'Which part of your visit made you feel most comfortable or confident?', NULL, 'mcq_multi', NULL, 1, 2, 1, 0, 0),
(5, 2, NULL, 'Is there anything we could improve to make future visits even better for you?', NULL, 'mcq_multi', NULL, 1, 4, 1, 0, 0),
(6, 2, NULL, 'Is there any staff member or moment during your visit that you would like to acknowledge or appreciate?', NULL, 'text', NULL, 0, 5, 1, 0, 0),
(7, 2, NULL, 'If there’s anything at all you’d like us to know — big or small — please feel free to share it here.', NULL, 'text', NULL, 0, 6, 1, 0, 0),
(8, 2, NULL, 'Before today, which of the following services were you already aware that Dr Bhasin’s Lab provides?', NULL, 'mcq_multi', NULL, 1, 7, 1, 0, 0),
(9, 2, NULL, 'Which part of your visit could we improve to serve you better?', NULL, 'mcq_multi', NULL, 1, 8, 1, 0, 0),
(10, 2, NULL, 'During your visit, did you feel listened to and treated with care?', NULL, 'mcq_single', NULL, 0, 9, 1, 0, 0),
(11, 2, NULL, 'In your own words, how would you describe your experience with us today?', NULL, 'text', NULL, 0, 10, 1, 0, 0),
(12, 2, 3, 'How likely are you to recommend Dr Bhasin’s Lab for the care, comfort, and confidence you experienced?', NULL, 'mcq_multi', NULL, 1, 11, 1, 1, 0),
(13, 2, NULL, 'We’re really sorry your experience did not meet expectations. Could you please tell us what went wrong?', NULL, 'text', NULL, 1, 12, 1, 0, 0),
(14, 2, NULL, 'Which part of your experience caused the most concern?', NULL, 'mcq_multi', NULL, 1, 13, 1, 0, 0),
(16, 3, NULL, 'Which Part Of Your Visit Most Contributed To You Feeling Comfortable, Cared For, Or Confident In Us? ', NULL, 'mcq_multi', NULL, 1, 2, 1, 0, 0),
(17, 3, 4, 'Overall, how would you rate your experience of care, comfort, and trust at Dr Bhasin’s Lab?', NULL, 'mcq_single', NULL, 1, 1, 1, 1, 0),
(18, 3, NULL, 'Is There Anything We Could Do Better To Make Your Future Visits Even More Comfortable Or Convenient?', NULL, 'mcq_multi', NULL, 1, 3, 1, 0, 0),
(19, 3, NULL, 'Is There Any Staff Member Or Moment During Your Visit That You Would Like To Acknowledge Or Appreciate?', NULL, 'text', 'You may mention a staff member, department, or a small moment that stood out.', 0, 4, 1, 0, 0),
(20, 3, NULL, 'Before Today, Which Of The Following Services Were You Already Aware That Dr Bhasin’S Lab Provides? ', NULL, 'mcq_multi', NULL, 1, 5, 1, 0, 0),
(21, 3, NULL, 'How Likely Are You To Recommend Dr Bhasin’S Lab For The Care, Comfort, And Confidence You Experienced?', NULL, 'mcq_single', NULL, 1, 6, 1, 0, 0),
(22, 3, NULL, 'We’Re Sorry That Your Experience Wasn’T As Smooth As It Should Have Been. To Help Us Do Better, Which Part Of Your Visit Could We Improve?', NULL, 'mcq_multi', NULL, 1, 7, 1, 0, 0),
(23, 3, NULL, 'During Your Visit, Did You Feel Listened To And Treated With Care?', NULL, 'mcq_single', NULL, 1, 8, 1, 0, 0),
(24, 3, NULL, ' In Your Own Words, How Would You Describe Your Experience With Us Today?', NULL, 'text', 'Optional – a few words are enough', 0, 9, 1, 0, 0),
(25, 3, NULL, 'How Likely Are You To Recommend Dr Bhasin’S Lab For The Care, Comfort, And Confidence You Experienced?', NULL, 'mcq_single', NULL, 1, 10, 1, 0, 0),
(26, 3, NULL, ' We’Re Really Sorry Your Experience Did Not Meet Expectations. Could You Please Tell Us What Went Wrong?', NULL, 'text', 'You can share as much or as little as you like. We genuinely want to understand.', 0, 11, 1, 0, 0),
(27, 3, NULL, 'Which Part Of Your Experience Caused The Most Concern?', NULL, 'mcq_multi', NULL, 1, 12, 1, 0, 0),
(28, 4, 5, 'Thinking about your home sample collection experience, how would you rate the care and confidence you felt with Dr Bhasin’s Lab?', NULL, 'mcq_single', NULL, 1, 1, 1, 1, 0),
(29, 4, NULL, 'Which Part Of The Home Collection Experience Made You Feel Most Comfortable Or Confident?', NULL, 'mcq_multi', NULL, 1, 2, 1, 0, 0),
(30, 4, NULL, 'Is There Anything We Could Do Better To Make Future Home Collections Even More Comfortable Or Convenient For You?', NULL, 'mcq_multi', NULL, 1, 3, 1, 0, 0),
(31, 4, NULL, 'Is There Any Staff Member Or Moment During The Home Visit You Would Like To Acknowledge Or Appreciate?', NULL, 'text', 'You may mention the phlebotomist or any small gesture that stood out.', 0, 4, 1, 0, 0),
(32, 4, NULL, 'Before Today, Which Of The Following Services Were You Already Aware That Dr Bhasin’S Lab Provides?', NULL, 'mcq_multi', NULL, 1, 5, 1, 0, 0),
(33, 4, NULL, 'How Likely Are You To Recommend Dr Bhasin’S Lab’S Home Sample Collection Service To A Friend Or Family Member?', NULL, 'mcq_single', NULL, 1, 6, 1, 0, 0),
(34, 4, NULL, 'We’Re Sorry That Your Home Collection Experience Wasn’T As Smooth As It Should Have Been. To Help Us Improve, Which Part Of The Visit Could We Do Better?', NULL, 'mcq_multi', NULL, 1, 7, 1, 0, 0),
(35, 4, NULL, 'During The Home Visit, Did You Feel Comfortable And Treated With Care?', NULL, 'mcq_single', NULL, 1, 8, 1, 0, 0),
(36, 4, NULL, 'In Your Own Words, How Would You Describe Your Home Collection Experience?', NULL, 'text', NULL, 0, 9, 1, 0, 0),
(37, 4, NULL, 'We’Re Really Sorry Your Home Collection Experience Did Not Meet Expectations. Could You Please Tell Us What Went Wrong?', NULL, 'text', 'You can share as much or as little as you like. We genuinely want to understand.', 0, 10, 1, 0, 0),
(38, 4, NULL, 'Which Part Of The Home Visit Caused The Most Concern?”', NULL, 'mcq_multi', NULL, 1, 11, 1, 0, 0),
(39, 4, NULL, 'Would You Like Someone From Our Team To Contact You And Address This?', NULL, 'mcq_single', NULL, 1, 12, 1, 0, 0),
(56, 10, 4, 'Overall, how would you rate your experience of care, comfort, and trust at Dr Bhasin’s Lab?', NULL, 'mcq_single', NULL, 1, 1, 1, 1, 0),
(57, 10, NULL, 'Ok', NULL, 'mcq_multi', NULL, 0, 2, 1, 0, 0),
(58, 10, NULL, 'Yu', NULL, 'mcq_single', NULL, 0, 3, 1, 0, 0),
(59, 10, NULL, 'Tg', NULL, 'mcq_multi', NULL, 0, 4, 1, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `campaign_question_options`
--

CREATE TABLE `campaign_question_options` (
  `id` int NOT NULL,
  `campaign_question_id` int NOT NULL,
  `option_value` varchar(100) NOT NULL,
  `option_text_en` varchar(1000) DEFAULT NULL,
  `option_text_hi` varchar(1000) DEFAULT NULL,
  `sentiment` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `score_value` int DEFAULT NULL,
  `order_index` int DEFAULT '0',
  `follow_up_label` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `campaign_question_options`
--

INSERT INTO `campaign_question_options` (`id`, `campaign_question_id`, `option_value`, `option_text_en`, `option_text_hi`, `sentiment`, `department`, `area`, `score_value`, `order_index`, `follow_up_label`) VALUES
(8, 3, '5', 'Definitely – I would recommend', NULL, 'positive', NULL, NULL, 5, 8, NULL),
(9, 3, '3', 'Maybe – I’d consider it', NULL, 'neutral', NULL, NULL, 3, 9, NULL),
(10, 3, '1', 'Unlikely – I wouldn’t recommend', NULL, 'negative', NULL, NULL, 1, 10, NULL),
(11, 4, '5', 'Warmth and courtesy of the staff', NULL, 'positive', NULL, NULL, 0, 11, NULL),
(12, 4, '5', 'Clear explanation and communication', NULL, 'positive', NULL, NULL, 0, 12, NULL),
(13, 4, '5', 'Cleanliness and hygiene of the centre', NULL, 'positive', NULL, NULL, 0, 13, NULL),
(14, 4, '5', 'Professional and gentle sample collection', NULL, 'positive', NULL, NULL, 0, 14, NULL),
(16, 4, '5', 'Feeling reassured about accuracy and reports', NULL, 'positive', NULL, NULL, 0, 16, NULL),
(17, 4, '5', 'Ambience & Aesthetics of the centre', NULL, 'positive', NULL, NULL, 0, 17, NULL),
(19, 4, '5', 'Test Charges', NULL, 'positive', NULL, NULL, 0, 19, NULL),
(21, 4, '5', 'Report Turn Around Time/ Time to get reports', NULL, 'positive', NULL, NULL, 0, 21, NULL),
(22, 4, '5', 'Short waiting time / smooth process', NULL, 'positive', NULL, NULL, 0, 22, NULL),
(23, 4, '5', 'Location, Accessibility, Parking & Valet Service', NULL, 'positive', NULL, NULL, 0, 23, NULL),
(24, 5, '1', 'Waiting time at the centre', NULL, 'neutral', NULL, NULL, 0, 24, NULL),
(25, 5, '1', 'Clarity of information or explanations', NULL, 'negative', NULL, NULL, 0, 25, NULL),
(26, 5, '1', 'Ease of registration or billing', NULL, 'negative', NULL, NULL, 0, 26, NULL),
(28, 5, '1', 'Coordination or guidance during the visit', NULL, 'negative', NULL, NULL, 0, 28, NULL),
(29, 5, '1', 'Comfort of seating / environment', NULL, 'negative', NULL, NULL, 0, 29, NULL),
(30, 5, '1', 'Communication about reports / timelines', NULL, 'negative', NULL, NULL, 0, 30, NULL),
(31, 5, '5', 'Nothing — everything was fine', NULL, 'positive', NULL, NULL, 0, 31, NULL),
(32, 8, '5', 'Open 24×7 (round-the-clock services)', NULL, 'positive', NULL, NULL, 0, 32, NULL),
(33, 8, '5', 'Urgent / 2-3 Hour reporting when required', NULL, 'positive', NULL, NULL, 0, 33, NULL),
(34, 8, '5', 'Home sample collection in Delhi & NCR', NULL, 'positive', NULL, NULL, 0, 34, NULL),
(35, 8, '5', 'I was aware of all of these', NULL, 'positive', NULL, NULL, 0, 35, NULL),
(36, 8, '5', 'This is new information for me', NULL, 'positive', NULL, NULL, 0, 36, NULL),
(37, 9, '5', 'Waiting time at the centre', NULL, 'positive', NULL, NULL, 0, 37, NULL),
(38, 9, '5', 'Clarity of information or explanations', NULL, 'positive', NULL, NULL, 0, 38, NULL),
(39, 9, '5', 'Staff interaction or communication', NULL, 'positive', NULL, NULL, 0, 39, NULL),
(40, 9, '5', 'Comfort or cleanliness of the centre', NULL, 'positive', NULL, NULL, 0, 40, NULL),
(41, 9, '5', 'Guidance during the process', NULL, 'positive', NULL, NULL, 0, 41, NULL),
(42, 9, '5', 'Communication about reports / timelines', NULL, 'positive', NULL, NULL, 0, 42, NULL),
(43, 3, '5', 'Test Charges', NULL, 'positive', NULL, NULL, 0, 43, NULL),
(44, 9, '5', 'Report Turn Around Time', NULL, 'positive', NULL, NULL, 0, 44, NULL),
(45, 9, '5', 'Something else', NULL, 'positive', NULL, NULL, 0, 45, NULL),
(46, 10, '5', 'Yes', NULL, 'positive', NULL, NULL, 0, 46, NULL),
(47, 10, '3', 'Somewhat', NULL, 'neutral', NULL, NULL, 0, 47, NULL),
(48, 10, '1', 'No', NULL, 'negative', NULL, NULL, 0, 48, NULL),
(49, 12, '5', 'Definitely – I would recommend', NULL, 'positive', NULL, NULL, 5, 49, NULL),
(50, 12, '3', 'Maybe – I’d consider it', NULL, 'neutral', NULL, NULL, 3, 50, NULL),
(51, 12, '1', 'Unlikely – I wouldn’t recommend', NULL, 'negative', NULL, NULL, 1, 51, NULL),
(52, 14, '1', 'Long or unclear waiting time', NULL, 'negative', NULL, NULL, 0, 52, NULL),
(53, 14, '1', 'Staff behaviour or communication', NULL, 'negative', NULL, NULL, 0, 53, NULL),
(54, 14, '1', 'Lack of information or explanation', NULL, 'negative', NULL, NULL, 0, 54, NULL),
(55, 14, '1', 'Comfort, cleanliness, or hygiene', NULL, 'negative', NULL, NULL, 0, 55, NULL),
(56, 14, '1', 'Issues with reports or timelines', NULL, 'negative', NULL, NULL, 0, 56, NULL),
(57, 14, '1', 'Test Charges, Billing & Payment concerns', NULL, 'negative', NULL, NULL, 0, 57, NULL),
(58, 14, '1', 'Something Else', NULL, 'negative', NULL, NULL, 0, 58, NULL),
(59, 2, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5, 1, NULL),
(60, 2, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4, 2, NULL),
(61, 2, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3, 3, NULL),
(62, 2, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2, 4, NULL),
(63, 2, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1, 5, NULL),
(64, 16, '1', 'I Found The Staff Courteous, Caring, And Respectful Throughout My Visit', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(65, 16, '2', 'I Was Given Clear Information And Everything Was Explained To Me Transparently', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(66, 16, '3', 'The Sample Collection Was Handled Gently And Professionally, Which Put Me At Ease', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(67, 16, '4', 'The Centre Felt Clean, Hygienic, And Well Maintained', NULL, 'positive', NULL, NULL, 1, 4, NULL),
(68, 16, '5', 'The Process Was Quick And Smooth, With Minimal Waiting', NULL, 'positive', NULL, NULL, 1, 5, NULL),
(69, 16, '6', 'The Time Taken To Receive My Reports Was Satisfactory', NULL, 'positive', NULL, NULL, 1, 6, NULL),
(70, 16, '7', 'The Test Charges Felt Reasonable And Clearly Communicated', NULL, 'positive', NULL, NULL, 1, 7, NULL),
(71, 16, '8', 'The Centre Was Comfortable, Calm, And Felt Safe And Hygienic', NULL, 'positive', NULL, NULL, 1, 8, NULL),
(72, 17, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5, 1, NULL),
(73, 17, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4, 2, NULL),
(74, 17, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3, 3, NULL),
(75, 17, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2, 4, NULL),
(76, 17, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1, 5, NULL),
(77, 16, '9', 'The Location Was Easy To Access, And Facilities Like Parking/Valet Made The Visit Convenient', NULL, 'positive', NULL, NULL, 1, 9, NULL),
(78, 16, '10', 'Other ', NULL, 'positive', NULL, NULL, 1, 10, 'please specify'),
(79, 18, '1', 'Reducing The Waiting Time At The Centre', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(80, 18, '2', 'Providing Clearer Information Or Explanations When Needed', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(81, 18, '3', 'Making Registration Or Billing Simpler And Quicker', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(82, 18, '4', 'Improving Seating Comfort Or The Waiting Area Environment', NULL, 'positive', NULL, NULL, 1, 4, NULL),
(83, 18, '5', 'Better Guidance Or Coordination During The Visit', NULL, 'positive', NULL, NULL, 1, 5, NULL),
(84, 18, '6', 'Clearer Communication About Reports Or Expected Timelines', NULL, 'positive', NULL, NULL, 1, 6, NULL),
(85, 18, '7', 'Test Charges', NULL, 'positive', NULL, NULL, 1, 7, NULL),
(86, 18, '8', 'Reporting Time', NULL, 'positive', NULL, NULL, 1, 8, NULL),
(87, 18, '9', 'Nothing In Particular — Everything Was Satisfactory For Me', NULL, 'positive', NULL, NULL, 1, 9, NULL),
(88, 18, '10', 'Something Else I’D Like To Mention', NULL, 'positive', NULL, NULL, 1, 10, 'Please Mention'),
(89, 20, '1', 'Open 24×7 (Round-The-Clock Services)', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(90, 20, '2', 'Urgent / Same-Day Reporting When Required', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(91, 20, '3', 'Home Sample Collection', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(92, 20, '4', 'I Was Aware Of All Of These', NULL, 'positive', NULL, NULL, 1, 4, NULL),
(93, 20, '5', 'This Is New Information For Me', NULL, 'positive', NULL, NULL, 1, 5, NULL),
(94, 21, '1', 'Yes, Without Hesitation', NULL, 'positive', NULL, NULL, 2, 1, NULL),
(95, 21, '2', 'Yes, But With Some Reservations', NULL, 'neutral', NULL, NULL, 1, 2, 'can you tell us more'),
(96, 21, '3', 'No, Not Based On This Experience', NULL, 'negative', NULL, NULL, 0, 3, 'What can we do to change this ?'),
(97, 22, '1', 'Reducing The Waiting Time At The Centre', NULL, 'neutral', NULL, NULL, 1, 1, NULL),
(98, 22, '2', 'Providing Clearer Information Or Explanations', NULL, 'neutral', NULL, NULL, 1, 2, NULL),
(99, 22, '3', 'Improving Staff Interaction Or Communication', NULL, 'neutral', NULL, NULL, 1, 3, NULL),
(100, 22, '4', 'Enhancing Comfort Or Cleanliness Of The Centre', NULL, 'neutral', NULL, NULL, 1, 4, NULL),
(101, 22, '5', 'Better Guidance During Different Steps Of The Visit', NULL, 'neutral', NULL, NULL, 1, 5, NULL),
(102, 22, '6', 'Clearer Communication About Reports Or Expected Timelines', NULL, 'neutral', NULL, NULL, 1, 6, NULL),
(103, 22, '7', 'Reduce Test Charges', NULL, 'neutral', NULL, NULL, 1, 7, NULL),
(104, 22, '8', 'Something Else I’D Like To Share', NULL, 'neutral', NULL, NULL, 1, 8, 'Please Share'),
(105, 23, '1', 'Yes', NULL, 'positive', NULL, NULL, 2, 1, NULL),
(106, 23, '2', 'Somewhat', NULL, 'neutral', NULL, NULL, 1, 2, NULL),
(107, 23, '3', 'No', NULL, 'negative', NULL, NULL, 0, 3, NULL),
(108, 25, '1', 'Yes, Without Hesitation', NULL, 'positive', NULL, NULL, 2, 1, NULL),
(109, 25, '2', 'Yes, But With Some Reservations', NULL, 'neutral', NULL, NULL, 1, 2, 'can you tell us more'),
(110, 25, '3', 'No, Not Based On This Experience', NULL, 'negative', NULL, NULL, 0, 3, 'What can we do to change this ?'),
(111, 27, '1', 'Long Or Unclear Waiting Time', NULL, 'negative', NULL, NULL, 0, 1, NULL),
(112, 27, '2', 'Staff Behaviour Or Communication', NULL, 'negative', NULL, NULL, 0, 2, NULL),
(113, 27, '3', 'Lack Of Information Or Explanation', NULL, 'negative', NULL, NULL, 0, 3, NULL),
(114, 27, '4', 'Comfort, Cleanliness, Or Hygiene', NULL, 'neutral', NULL, NULL, 0, 4, NULL),
(115, 27, '5', 'Issues With Reports Or Timelines', NULL, 'negative', NULL, NULL, 0, 5, NULL),
(116, 27, '6', 'Billing Or Payment Concerns', NULL, 'negative', NULL, NULL, 0, 6, NULL),
(117, 27, '7', 'Something Else', NULL, 'negative', NULL, NULL, 0, 7, NULL),
(118, 28, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5, 1, NULL),
(119, 28, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4, 2, NULL),
(120, 28, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3, 3, NULL),
(121, 28, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2, 4, NULL),
(122, 28, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1, 5, NULL),
(123, 29, '1', 'The Phlebotomist Was Polite, Respectful, And Made Me Feel At Ease', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(124, 29, '2', 'I Was Informed Clearly About The Visit Timing And Arrival', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(125, 29, '3', 'The Sample Collection Was Gentle, Professional, And Well Handled', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(126, 29, '4', 'Safety, Hygiene, And Cleanliness Were Well Maintained During The Visit', NULL, 'positive', NULL, NULL, 1, 4, NULL),
(127, 29, '5', 'The Entire Process Was Smooth And Did Not Disrupt My Routine', NULL, 'positive', NULL, NULL, 1, 5, NULL),
(128, 29, '6', 'The Time Taken To Receive My Reports Was Satisfactory', NULL, 'positive', NULL, NULL, 1, 6, NULL),
(129, 29, '7', 'The Charges Were Reasonable And Explained Clearly', NULL, 'positive', NULL, NULL, 1, 7, NULL),
(130, 29, '8', 'Overall, The Experience At Home Felt Comfortable And Reassuring', NULL, 'positive', NULL, NULL, 1, 8, NULL),
(131, 29, '9', 'Other', NULL, 'positive', NULL, NULL, 1, 9, 'Please Specify'),
(132, 30, '1', 'More Accurate Or Timely Communication About Arrival Time', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(133, 30, '2', 'Clearer Instructions Before The Visit (Fasting, Preparation, Etc.)', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(134, 30, '3', 'Improved Coordination Or Punctuality Of The Visit', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(135, 30, '4', 'Better Communication About Reports Or Timelines', NULL, 'positive', NULL, NULL, 1, 4, NULL),
(136, 30, '5', 'Billing Or Payment-Related Clarity', NULL, 'positive', NULL, NULL, 1, 5, NULL),
(137, 30, '6', 'Nothing In Particular — Everything Was Satisfactory For Me', NULL, 'positive', NULL, NULL, 1, 6, NULL),
(138, 30, '7', 'Something Else I’D Like To Mention', NULL, 'positive', NULL, NULL, 1, 7, 'Please Mention'),
(139, 32, '1', 'Open 24×7 (Round-The-Clock Services)', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(140, 32, '2', 'Urgent / Same-Day Reporting When Required', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(141, 32, '3', 'Centre Walk-In Services', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(142, 32, '4', 'I Was Aware Of All Of These', NULL, 'positive', NULL, NULL, 1, 4, NULL),
(143, 32, '5', 'This Is New Information For Me', NULL, 'positive', NULL, NULL, 1, 5, NULL),
(144, 33, '1', 'Yes, Without Hesitation', NULL, 'positive', NULL, NULL, 1, 1, NULL),
(145, 33, '2', 'Yes, But With Some Reservations', NULL, 'positive', NULL, NULL, 1, 2, NULL),
(146, 33, '3', 'No, Not Based On This Experience', NULL, 'positive', NULL, NULL, 1, 3, NULL),
(147, 34, '1', 'Punctuality Or Arrival Timing', NULL, 'neutral', NULL, NULL, 1, 1, NULL),
(148, 34, '2', 'Clarity Of Instructions Or Communication Before The Visit', NULL, 'neutral', NULL, NULL, 1, 2, NULL),
(149, 34, '3', 'Staff Interaction Or Behaviour', NULL, 'neutral', NULL, NULL, 1, 3, NULL),
(150, 34, '4', 'Comfort Or Professionalism During Sample Collection', NULL, 'neutral', NULL, NULL, 1, 4, NULL),
(151, 34, '5', 'Hygiene Or Safety During The Visit', NULL, 'neutral', NULL, NULL, 1, 5, NULL),
(152, 34, '6', 'Communication About Reports Or Timelines', NULL, 'neutral', NULL, NULL, 1, 6, NULL),
(153, 34, '7', 'Something Else I’D Like To Share', NULL, 'neutral', NULL, NULL, 1, 7, 'Please Share'),
(154, 35, '1', 'Yes', NULL, 'neutral', NULL, NULL, 1, 1, NULL),
(155, 35, '2', 'Somewhat', NULL, 'neutral', NULL, NULL, 1, 2, NULL),
(156, 35, '3', 'No', NULL, 'neutral', NULL, NULL, 1, 3, NULL),
(157, 38, '1', 'Late Or Uncoordinated Arrival', NULL, 'negative', NULL, NULL, 1, 1, NULL),
(158, 38, '2', 'Staff Behaviour Or Professionalism', NULL, 'negative', NULL, NULL, 1, 2, NULL),
(159, 38, '3', 'Discomfort During Sample Collection', NULL, 'negative', NULL, NULL, 1, 3, NULL),
(160, 38, '4', 'Hygiene Or Safety Concerns', NULL, 'negative', NULL, NULL, 1, 4, NULL),
(161, 38, '5', 'Lack Of Information Or Instructions', NULL, 'negative', NULL, NULL, 1, 5, NULL),
(162, 38, '6', 'Report Delay Or Communication Issues', NULL, 'negative', NULL, NULL, 1, 6, NULL),
(163, 38, '7', 'Billing Or Payment Concerns', NULL, 'negative', NULL, NULL, 1, 7, NULL),
(164, 38, '8', 'Something Else', NULL, 'negative', NULL, NULL, 1, 8, NULL),
(165, 39, '1', 'Yes', NULL, 'negative', NULL, NULL, 1, 1, NULL),
(166, 39, '2', 'No', NULL, 'negative', NULL, NULL, 1, 2, NULL),
(227, 56, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5, 1, NULL),
(228, 56, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4, 2, NULL),
(229, 56, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3, 3, NULL),
(230, 56, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2, 4, NULL),
(231, 56, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1, 5, NULL),
(232, 57, '1', '123', NULL, 'neutral', NULL, NULL, 2, 1, NULL),
(233, 57, '2', '456', NULL, 'neutral', NULL, NULL, 2, 2, NULL),
(234, 58, '1', 'Pl', NULL, 'neutral', NULL, NULL, 0, 1, NULL),
(235, 58, '2', 'Lm', NULL, 'neutral', NULL, NULL, 0, 2, NULL),
(236, 59, '1', 'Ty', NULL, 'neutral', NULL, NULL, 0, 1, NULL),
(237, 59, '2', 'Yh', NULL, 'neutral', NULL, NULL, 0, 2, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `campaign_recipients`
--

CREATE TABLE `campaign_recipients` (
  `id` int NOT NULL,
  `recipient_list_id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `pii_data_json` json DEFAULT NULL,
  `personalized_link_token` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `campaign_recipients`
--

INSERT INTO `campaign_recipients` (`id`, `recipient_list_id`, `campaign_id`, `pii_data_json`, `personalized_link_token`, `status`) VALUES
(1, 1, 4, '{\"name\": \"rohit\", \"contact\": \"8126382045\"}', NULL, 'pending'),
(2, 2, 3, '{\"name\": \"rohit\", \"contact\": \"8126382045\"}', NULL, 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `campaign_recipient_lists`
--

CREATE TABLE `campaign_recipient_lists` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `source_type` varchar(100) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `campaign_recipient_lists`
--

INSERT INTO `campaign_recipient_lists` (`id`, `campaign_id`, `source_type`, `name`, `description`) VALUES
(1, 4, 'upload_excel', 'Upload 2026-01-15 13:03:00', 'Uploaded 1 contacts via send page'),
(2, 3, 'upload_excel', 'Upload 2026-01-15 13:05:08', 'Uploaded 1 contacts via send page');

-- --------------------------------------------------------

--
-- Table structure for table `campaign_send_schedules`
--

CREATE TABLE `campaign_send_schedules` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `trigger_type` varchar(50) DEFAULT NULL,
  `offset_minutes` int DEFAULT NULL,
  `channel_id` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `collection_channels`
--

CREATE TABLE `collection_channels` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(50) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_action_types`
--

CREATE TABLE `feedback_action_types` (
  `id` int NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_answers`
--

CREATE TABLE `feedback_answers` (
  `id` int NOT NULL,
  `response_id` int NOT NULL,
  `campaign_question_id` int NOT NULL,
  `answer_text` varchar(2000) DEFAULT NULL,
  `selected_option_values` json DEFAULT NULL,
  `sentiment` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `score_value` int DEFAULT NULL,
  `follow_up_text` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `feedback_answers`
--

INSERT INTO `feedback_answers` (`id`, `response_id`, `campaign_question_id`, `answer_text`, `selected_option_values`, `sentiment`, `department`, `area`, `score_value`, `follow_up_text`) VALUES
(7, 7, 2, NULL, '[\"1\"]', 'negative', NULL, NULL, 1, NULL),
(8, 7, 3, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(9, 7, 4, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(10, 7, 5, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(11, 7, 6, '', '[]', NULL, NULL, NULL, NULL, NULL),
(12, 7, 7, '', '[]', NULL, NULL, NULL, NULL, NULL),
(13, 7, 8, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(14, 7, 9, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(15, 7, 10, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(16, 7, 11, '', '[]', NULL, NULL, NULL, NULL, NULL),
(17, 7, 12, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(18, 7, 13, '', '[]', NULL, NULL, NULL, NULL, NULL),
(19, 7, 14, NULL, '[\"1\"]', 'negative', NULL, NULL, 0, NULL),
(20, 8, 2, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(21, 8, 3, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(22, 8, 4, NULL, '[\"5\", \"5\"]', 'positive', NULL, NULL, 0, NULL),
(23, 8, 5, NULL, '[\"1\"]', 'neutral', NULL, NULL, 0, NULL),
(24, 8, 6, 'rohit bisht', '[]', NULL, NULL, NULL, NULL, NULL),
(25, 8, 7, 'good IT', '[]', NULL, NULL, NULL, NULL, NULL),
(26, 8, 8, NULL, '[\"5\"]', 'positive', NULL, NULL, 0, NULL),
(27, 8, 9, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(28, 8, 10, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(29, 8, 11, '', '[]', NULL, NULL, NULL, NULL, NULL),
(30, 8, 12, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(31, 8, 13, '', '[]', NULL, NULL, NULL, NULL, NULL),
(32, 8, 14, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(33, 9, 28, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(34, 9, 29, NULL, '[\"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(35, 9, 30, NULL, '[\"1\"]', 'positive', NULL, NULL, 1, 'ok'),
(36, 9, 31, 'hi', '[]', NULL, NULL, NULL, NULL, NULL),
(37, 9, 32, NULL, '[\"1\"]', 'positive', NULL, NULL, 1, NULL),
(38, 9, 33, NULL, '[\"1\"]', 'positive', NULL, NULL, 1, NULL),
(39, 9, 34, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(40, 9, 35, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(41, 9, 36, '', '[]', NULL, NULL, NULL, NULL, NULL),
(42, 9, 37, '', '[]', NULL, NULL, NULL, NULL, NULL),
(43, 9, 38, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(44, 9, 39, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(45, 10, 28, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(46, 10, 29, NULL, '[\"1\", \"1\", \"1\", \"1\", \"1\", \"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(47, 10, 30, NULL, '[\"1\", \"1\", \"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(48, 10, 31, '', '[]', NULL, NULL, NULL, NULL, NULL),
(49, 10, 32, NULL, '[\"1\", \"1\", \"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(50, 10, 33, NULL, '[\"1\"]', 'positive', NULL, NULL, 1, NULL),
(51, 10, 34, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(52, 10, 35, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(53, 10, 36, '', '[]', NULL, NULL, NULL, NULL, NULL),
(54, 10, 37, '', '[]', NULL, NULL, NULL, NULL, NULL),
(55, 10, 38, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(56, 10, 39, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(58, 12, 28, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(59, 12, 29, NULL, '[\"1\", \"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(60, 12, 30, NULL, '[\"1\", \"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(61, 12, 31, 'okkkk', '[]', NULL, NULL, NULL, NULL, NULL),
(62, 12, 32, NULL, '[\"1\", \"1\", \"1\", \"1\"]', 'positive', NULL, NULL, 1, NULL),
(63, 12, 33, NULL, '[\"1\"]', 'positive', NULL, NULL, 1, NULL),
(64, 12, 34, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(65, 12, 35, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(66, 12, 36, '', '[]', NULL, NULL, NULL, NULL, NULL),
(67, 12, 37, '', '[]', NULL, NULL, NULL, NULL, NULL),
(68, 12, 38, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(69, 12, 39, NULL, '[]', NULL, NULL, NULL, NULL, NULL),
(70, 13, 28, NULL, '[\"4\"]', 'positive', NULL, NULL, 4, NULL),
(71, 13, 29, NULL, '[\"3\", \"5\"]', 'positive', NULL, NULL, 1, NULL),
(72, 13, 30, NULL, '[\"1\", \"2\", \"3\"]', 'positive', NULL, NULL, 1, NULL),
(73, 13, 31, 'f', '[]', NULL, NULL, NULL, NULL, NULL),
(74, 13, 32, NULL, '[\"2\", \"3\"]', 'positive', NULL, NULL, 1, NULL),
(75, 13, 33, NULL, '[\"2\"]', 'positive', NULL, NULL, 1, NULL),
(76, 13, 34, NULL, '[\"3\", \"6\"]', 'neutral', NULL, NULL, 1, NULL),
(77, 13, 35, NULL, '[\"2\"]', 'neutral', NULL, NULL, 1, NULL),
(78, 13, 36, 'h', '[]', NULL, NULL, NULL, NULL, NULL),
(79, 13, 37, 'g', '[]', NULL, NULL, NULL, NULL, NULL),
(80, 13, 38, NULL, '[\"3\", \"4\"]', 'negative', NULL, NULL, 1, NULL),
(81, 13, 39, NULL, '[\"2\"]', 'negative', NULL, NULL, 1, NULL),
(82, 14, 56, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(83, 14, 57, NULL, '[\"1\", \"2\"]', 'neutral', NULL, NULL, 2, NULL),
(84, 14, 58, NULL, '[\"2\"]', 'neutral', NULL, NULL, 0, NULL),
(85, 14, 59, NULL, '[\"1\", \"2\"]', 'neutral', NULL, NULL, 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `feedback_files`
--

CREATE TABLE `feedback_files` (
  `id` int NOT NULL,
  `response_id` int NOT NULL,
  `campaign_question_id` int DEFAULT NULL,
  `file_path` varchar(255) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_responses`
--

CREATE TABLE `feedback_responses` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `recipient_id` int DEFAULT NULL,
  `submission_time` datetime DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  `overall_score` int DEFAULT NULL,
  `overall_sentiment` varchar(50) DEFAULT NULL,
  `overall_rating_value` int DEFAULT NULL,
  `needs_manual_review` tinyint(1) DEFAULT NULL,
  `is_complaint` tinyint(1) DEFAULT NULL,
  `ticket_id` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `pii_data_json` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `feedback_responses`
--

INSERT INTO `feedback_responses` (`id`, `campaign_id`, `recipient_id`, `submission_time`, `language`, `overall_score`, `overall_sentiment`, `overall_rating_value`, `needs_manual_review`, `is_complaint`, `ticket_id`, `status`, `pii_data_json`) VALUES
(7, 2, NULL, '2025-12-23 10:10:23', 'en', 0, 'negative', NULL, 0, 1, 5, 'under_review', NULL),
(8, 2, NULL, '2025-12-24 06:20:56', 'en', 2, 'negative', 5, 0, 1, 6, 'under_review', '{\"name\": \"VISHU\", \"lab_id\": \"102511111\", \"visit_date\": \"0002-12-24\", \"mobile_number\": \"9810637037\", \"mobile_country\": \"+91\"}'),
(9, 4, NULL, '2026-01-15 08:00:15', 'en', 1, 'negative', NULL, 0, 1, 7, 'under_review', '{\"name\": \"rohit\", \"lab_id\": null, \"visit_date\": \"2026-01-15\", \"mobile_number\": \"8076968219\", \"mobile_country\": \"+91\"}'),
(10, 4, NULL, '2026-01-15 09:48:04', 'en', 1, 'negative', NULL, 0, 1, 8, 'under_review', '{\"name\": \"Rohit\", \"lab_id\": null, \"visit_date\": \"2026-01-15\", \"mobile_number\": \"8126382045\", \"mobile_country\": \"+91\"}'),
(12, 4, NULL, '2026-01-21 11:16:41', 'en', 1, 'negative', NULL, 0, 1, 10, 'under_review', '{\"name\": \"rohit\", \"lab_id\": null, \"visit_date\": \"2026-01-21\", \"mobile_number\": \"8126382045\", \"mobile_country\": \"+91\"}'),
(13, 4, NULL, '2026-01-21 11:38:00', 'en', 1, 'negative', NULL, 0, 1, 11, 'under_review', '{\"name\": \"d\", \"lab_id\": null, \"visit_date\": \"2026-01-21\", \"mobile_number\": \"8126382045\", \"mobile_country\": \"+91\"}'),
(14, 10, NULL, '2026-01-21 11:41:57', 'en', 1, 'negative', NULL, 0, 1, 12, 'under_review', '{\"name\": \"u\", \"lab_id\": null, \"visit_date\": \"2026-01-21\", \"mobile_number\": \"2154856535\", \"mobile_country\": \"+91\"}');

-- --------------------------------------------------------

--
-- Table structure for table `feedback_rewards`
--

CREATE TABLE `feedback_rewards` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `criteria_json` varchar(1000) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_tickets`
--

CREATE TABLE `feedback_tickets` (
  `id` int NOT NULL,
  `ticket_number` varchar(100) NOT NULL,
  `response_id` int DEFAULT NULL,
  `campaign_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `assigned_to_user_id` int DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `closure_mood` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `summary` varchar(500) DEFAULT NULL,
  `details` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `feedback_tickets`
--

INSERT INTO `feedback_tickets` (`id`, `ticket_number`, `response_id`, `campaign_id`, `created_at`, `created_by`, `assigned_to_user_id`, `severity`, `status`, `closure_mood`, `department`, `summary`, `details`) VALUES
(5, 'TKT-7', 7, 2, '2025-12-23 10:10:24', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(6, 'TKT-8', 8, 2, '2025-12-24 06:20:56', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(7, 'TKT-9', 9, 4, '2026-01-15 08:00:15', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(8, 'TKT-10', 10, 4, '2026-01-15 09:48:04', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(10, 'TKT-12', 12, 4, '2026-01-21 11:16:41', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(11, 'TKT-13', 13, 4, '2026-01-21 11:38:01', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(12, 'TKT-14', 14, 10, '2026-01-21 11:41:57', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint');

-- --------------------------------------------------------

--
-- Table structure for table `master_questions`
--

CREATE TABLE `master_questions` (
  `id` int NOT NULL,
  `code` varchar(100) NOT NULL,
  `default_text_en` varchar(1000) DEFAULT NULL,
  `default_text_hi` varchar(1000) DEFAULT NULL,
  `question_type` varchar(50) NOT NULL,
  `placeholder_en` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `master_questions`
--

INSERT INTO `master_questions` (`id`, `code`, `default_text_en`, `default_text_hi`, `question_type`, `placeholder_en`, `is_active`) VALUES
(1, 'Exp_Lab', 'Overall, how would you rate your experience with Dr Bhasin’s Lab?', NULL, 'rating_1_5', NULL, 1),
(3, 'NPS_Lab', 'How likely are you to recommend Dr Bhasin’s Lab for the care, comfort, and confidence you experienced?', NULL, 'mcq_multi', NULL, 1),
(4, 'NPS_OVERALL', 'Overall, how would you rate your experience of care, comfort, and trust at Dr Bhasin’s Lab?', NULL, 'mcq_single', NULL, 1),
(5, 'CODE_2', 'Thinking about your home sample collection experience, how would you rate the care and confidence you felt with Dr Bhasin’s Lab?', NULL, 'mcq_single', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `master_question_options`
--

CREATE TABLE `master_question_options` (
  `id` int NOT NULL,
  `master_question_id` int NOT NULL,
  `option_value` varchar(100) NOT NULL,
  `option_text_en` varchar(1000) DEFAULT NULL,
  `option_text_hi` varchar(1000) DEFAULT NULL,
  `sentiment` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `score_value` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `master_question_options`
--

INSERT INTO `master_question_options` (`id`, `master_question_id`, `option_value`, `option_text_en`, `option_text_hi`, `sentiment`, `department`, `area`, `score_value`) VALUES
(7, 3, '5', 'Definitely – I would recommend', NULL, 'positive', NULL, NULL, 5),
(8, 3, '3', 'Maybe – I’d consider it', NULL, 'neutral', NULL, NULL, 3),
(9, 3, '1', 'Unlikely – I wouldn’t recommend', NULL, 'negative', NULL, NULL, 1),
(12, 1, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5),
(13, 1, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4),
(14, 1, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3),
(15, 1, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2),
(16, 1, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1),
(17, 4, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5),
(18, 4, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4),
(19, 4, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3),
(20, 4, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2),
(21, 4, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1),
(22, 5, '5', 'Excellent – Felt truly cared for', NULL, 'positive', NULL, NULL, 5),
(23, 5, '4', 'Very Good – Mostly positive', NULL, 'positive', NULL, NULL, 4),
(24, 5, '3', 'Fair – Could have been better', NULL, 'neutral', NULL, NULL, 3),
(25, 5, '2', 'Poor – Disappointing experience', NULL, 'negative', NULL, NULL, 2),
(26, 5, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `pii_fields`
--

CREATE TABLE `pii_fields` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` varchar(50) NOT NULL,
  `field_type` varchar(50) NOT NULL,
  `is_required` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `question_flow_rules`
--

CREATE TABLE `question_flow_rules` (
  `id` int NOT NULL,
  `campaign_id` int NOT NULL,
  `source_question_id` int DEFAULT NULL,
  `source_option_value` varchar(100) DEFAULT NULL,
  `target_question_id` int DEFAULT NULL,
  `condition_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `question_flow_rules`
--

INSERT INTO `question_flow_rules` (`id`, `campaign_id`, `source_question_id`, `source_option_value`, `target_question_id`, `condition_type`) VALUES
(4, 2, 2, '1', 14, 'equals');

-- --------------------------------------------------------

--
-- Table structure for table `response_rewards`
--

CREATE TABLE `response_rewards` (
  `id` int NOT NULL,
  `response_id` int NOT NULL,
  `reward_id` int NOT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ticket_updates`
--

CREATE TABLE `ticket_updates` (
  `id` int NOT NULL,
  `ticket_id` int NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by_user_id` int DEFAULT NULL,
  `update_text` varchar(2000) DEFAULT NULL,
  `attachment_path` varchar(255) DEFAULT NULL,
  `next_action_due_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(50) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `mobile`, `role`, `department`, `username`, `password_hash`) VALUES
(1, 'Admin User', 'admin@example.com', '', 'admin', '', 'MGR', '56e2321b61fac819f060801eee7557b3d4f584e383a4511dbba261955b496c8b');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`bookingid`);

--
-- Indexes for table `campaigns`
--
ALTER TABLE `campaigns`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `campaign_channels`
--
ALTER TABLE `campaign_channels`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `channel_id` (`channel_id`);

--
-- Indexes for table `campaign_pii_fields`
--
ALTER TABLE `campaign_pii_fields`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `pii_field_id` (`pii_field_id`);

--
-- Indexes for table `campaign_questions`
--
ALTER TABLE `campaign_questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `master_question_id` (`master_question_id`);

--
-- Indexes for table `campaign_question_options`
--
ALTER TABLE `campaign_question_options`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_question_id` (`campaign_question_id`);

--
-- Indexes for table `campaign_recipients`
--
ALTER TABLE `campaign_recipients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personalized_link_token` (`personalized_link_token`),
  ADD KEY `recipient_list_id` (`recipient_list_id`),
  ADD KEY `campaign_id` (`campaign_id`);

--
-- Indexes for table `campaign_recipient_lists`
--
ALTER TABLE `campaign_recipient_lists`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`);

--
-- Indexes for table `campaign_send_schedules`
--
ALTER TABLE `campaign_send_schedules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `channel_id` (`channel_id`);

--
-- Indexes for table `collection_channels`
--
ALTER TABLE `collection_channels`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `feedback_action_types`
--
ALTER TABLE `feedback_action_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `feedback_answers`
--
ALTER TABLE `feedback_answers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `response_id` (`response_id`),
  ADD KEY `campaign_question_id` (`campaign_question_id`);

--
-- Indexes for table `feedback_files`
--
ALTER TABLE `feedback_files`
  ADD PRIMARY KEY (`id`),
  ADD KEY `response_id` (`response_id`),
  ADD KEY `campaign_question_id` (`campaign_question_id`);

--
-- Indexes for table `feedback_responses`
--
ALTER TABLE `feedback_responses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `ticket_id` (`ticket_id`),
  ADD KEY `recipient_id` (`recipient_id`);

--
-- Indexes for table `feedback_rewards`
--
ALTER TABLE `feedback_rewards`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feedback_tickets`
--
ALTER TABLE `feedback_tickets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticket_number` (`ticket_number`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `created_by` (`created_by`),
  ADD KEY `response_id` (`response_id`),
  ADD KEY `assigned_to_user_id` (`assigned_to_user_id`);

--
-- Indexes for table `master_questions`
--
ALTER TABLE `master_questions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `master_question_options`
--
ALTER TABLE `master_question_options`
  ADD PRIMARY KEY (`id`),
  ADD KEY `master_question_id` (`master_question_id`);

--
-- Indexes for table `pii_fields`
--
ALTER TABLE `pii_fields`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `question_flow_rules`
--
ALTER TABLE `question_flow_rules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `campaign_id` (`campaign_id`),
  ADD KEY `source_question_id` (`source_question_id`),
  ADD KEY `target_question_id` (`target_question_id`);

--
-- Indexes for table `response_rewards`
--
ALTER TABLE `response_rewards`
  ADD PRIMARY KEY (`id`),
  ADD KEY `response_id` (`response_id`),
  ADD KEY `reward_id` (`reward_id`);

--
-- Indexes for table `ticket_updates`
--
ALTER TABLE `ticket_updates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ticket_id` (`ticket_id`),
  ADD KEY `updated_by_user_id` (`updated_by_user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `ix_users_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `campaigns`
--
ALTER TABLE `campaigns`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `campaign_channels`
--
ALTER TABLE `campaign_channels`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `campaign_pii_fields`
--
ALTER TABLE `campaign_pii_fields`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `campaign_questions`
--
ALTER TABLE `campaign_questions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `campaign_question_options`
--
ALTER TABLE `campaign_question_options`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=238;

--
-- AUTO_INCREMENT for table `campaign_recipients`
--
ALTER TABLE `campaign_recipients`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `campaign_recipient_lists`
--
ALTER TABLE `campaign_recipient_lists`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `campaign_send_schedules`
--
ALTER TABLE `campaign_send_schedules`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `collection_channels`
--
ALTER TABLE `collection_channels`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback_action_types`
--
ALTER TABLE `feedback_action_types`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback_answers`
--
ALTER TABLE `feedback_answers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;

--
-- AUTO_INCREMENT for table `feedback_files`
--
ALTER TABLE `feedback_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback_responses`
--
ALTER TABLE `feedback_responses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `feedback_rewards`
--
ALTER TABLE `feedback_rewards`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback_tickets`
--
ALTER TABLE `feedback_tickets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `master_questions`
--
ALTER TABLE `master_questions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `master_question_options`
--
ALTER TABLE `master_question_options`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `pii_fields`
--
ALTER TABLE `pii_fields`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `question_flow_rules`
--
ALTER TABLE `question_flow_rules`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `response_rewards`
--
ALTER TABLE `response_rewards`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ticket_updates`
--
ALTER TABLE `ticket_updates`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `campaigns`
--
ALTER TABLE `campaigns`
  ADD CONSTRAINT `campaigns_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `campaign_channels`
--
ALTER TABLE `campaign_channels`
  ADD CONSTRAINT `campaign_channels_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `campaign_channels_ibfk_2` FOREIGN KEY (`channel_id`) REFERENCES `collection_channels` (`id`);

--
-- Constraints for table `campaign_pii_fields`
--
ALTER TABLE `campaign_pii_fields`
  ADD CONSTRAINT `campaign_pii_fields_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `campaign_pii_fields_ibfk_2` FOREIGN KEY (`pii_field_id`) REFERENCES `pii_fields` (`id`);

--
-- Constraints for table `campaign_questions`
--
ALTER TABLE `campaign_questions`
  ADD CONSTRAINT `campaign_questions_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `campaign_questions_ibfk_2` FOREIGN KEY (`master_question_id`) REFERENCES `master_questions` (`id`);

--
-- Constraints for table `campaign_question_options`
--
ALTER TABLE `campaign_question_options`
  ADD CONSTRAINT `campaign_question_options_ibfk_1` FOREIGN KEY (`campaign_question_id`) REFERENCES `campaign_questions` (`id`);

--
-- Constraints for table `campaign_recipients`
--
ALTER TABLE `campaign_recipients`
  ADD CONSTRAINT `campaign_recipients_ibfk_1` FOREIGN KEY (`recipient_list_id`) REFERENCES `campaign_recipient_lists` (`id`),
  ADD CONSTRAINT `campaign_recipients_ibfk_2` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`);

--
-- Constraints for table `campaign_recipient_lists`
--
ALTER TABLE `campaign_recipient_lists`
  ADD CONSTRAINT `campaign_recipient_lists_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`);

--
-- Constraints for table `campaign_send_schedules`
--
ALTER TABLE `campaign_send_schedules`
  ADD CONSTRAINT `campaign_send_schedules_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `campaign_send_schedules_ibfk_2` FOREIGN KEY (`channel_id`) REFERENCES `collection_channels` (`id`);

--
-- Constraints for table `feedback_answers`
--
ALTER TABLE `feedback_answers`
  ADD CONSTRAINT `feedback_answers_ibfk_1` FOREIGN KEY (`response_id`) REFERENCES `feedback_responses` (`id`),
  ADD CONSTRAINT `feedback_answers_ibfk_2` FOREIGN KEY (`campaign_question_id`) REFERENCES `campaign_questions` (`id`);

--
-- Constraints for table `feedback_files`
--
ALTER TABLE `feedback_files`
  ADD CONSTRAINT `feedback_files_ibfk_1` FOREIGN KEY (`response_id`) REFERENCES `feedback_responses` (`id`),
  ADD CONSTRAINT `feedback_files_ibfk_2` FOREIGN KEY (`campaign_question_id`) REFERENCES `campaign_questions` (`id`);

--
-- Constraints for table `feedback_responses`
--
ALTER TABLE `feedback_responses`
  ADD CONSTRAINT `feedback_responses_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `feedback_responses_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `feedback_tickets` (`id`),
  ADD CONSTRAINT `feedback_responses_ibfk_3` FOREIGN KEY (`recipient_id`) REFERENCES `campaign_recipients` (`id`);

--
-- Constraints for table `feedback_tickets`
--
ALTER TABLE `feedback_tickets`
  ADD CONSTRAINT `feedback_tickets_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `feedback_tickets_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `feedback_tickets_ibfk_3` FOREIGN KEY (`response_id`) REFERENCES `feedback_responses` (`id`),
  ADD CONSTRAINT `feedback_tickets_ibfk_4` FOREIGN KEY (`assigned_to_user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `master_question_options`
--
ALTER TABLE `master_question_options`
  ADD CONSTRAINT `master_question_options_ibfk_1` FOREIGN KEY (`master_question_id`) REFERENCES `master_questions` (`id`);

--
-- Constraints for table `question_flow_rules`
--
ALTER TABLE `question_flow_rules`
  ADD CONSTRAINT `question_flow_rules_ibfk_1` FOREIGN KEY (`campaign_id`) REFERENCES `campaigns` (`id`),
  ADD CONSTRAINT `question_flow_rules_ibfk_2` FOREIGN KEY (`source_question_id`) REFERENCES `campaign_questions` (`id`),
  ADD CONSTRAINT `question_flow_rules_ibfk_3` FOREIGN KEY (`target_question_id`) REFERENCES `campaign_questions` (`id`);

--
-- Constraints for table `response_rewards`
--
ALTER TABLE `response_rewards`
  ADD CONSTRAINT `response_rewards_ibfk_1` FOREIGN KEY (`response_id`) REFERENCES `feedback_responses` (`id`),
  ADD CONSTRAINT `response_rewards_ibfk_2` FOREIGN KEY (`reward_id`) REFERENCES `feedback_rewards` (`id`);

--
-- Constraints for table `ticket_updates`
--
ALTER TABLE `ticket_updates`
  ADD CONSTRAINT `ticket_updates_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `feedback_tickets` (`id`),
  ADD CONSTRAINT `ticket_updates_ibfk_2` FOREIGN KEY (`updated_by_user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

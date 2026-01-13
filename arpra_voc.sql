-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 24, 2025 at 06:53 AM
-- Server version: 8.4.7
-- PHP Version: 8.3.29

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

INSERT INTO `campaigns` (`id`, `name`, `code`, `description`, `campaign_type`, `status`, `primary_language`, `available_languages`, `layout_type`, `estimated_fill_time_seconds`, `start_date`, `end_date`, `is_forever`, `max_score`, `scoring_method`, `created_by`, `created_at`, `updated_at`, `exp_flow_map`, `thank_you_title`, `thank_you_message`, `thank_you_image_url`) VALUES
(1, 'TRIAL 1', 'TRL1', NULL, 'walk_in', 'draft', 'en', '[\"en\"]', 'one_question_per_page', 60, NULL, NULL, 1, NULL, 'simple_avg', 1, '2025-12-20 09:08:11', '2025-12-20 09:08:11', NULL, NULL, NULL, NULL),
(2, 'GK1 WALK IN ', 'FB001', 'None', 'walk_in', 'draft', 'en', '[\"en\"]', 'one_question_per_page', 60, NULL, NULL, 1, NULL, 'simple_avg', 1, '2025-12-23 07:30:13', '2025-12-24 06:18:14', '{\"1\": [8, 10, 14], \"2\": [14], \"3\": [12, 13, 14], \"4\": [8], \"5\": [4, 3, 5, 6, 7, 8]}', 'Thank You', 'Thank you for your honest feedback.\r\nYour voice helps us strengthen our commitment to care, accuracy, and empathy.\r\nWe’re grateful you chose Dr Bhasin’s Lab and trusted us with your health.', NULL);

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
  `is_required` tinyint(1) DEFAULT NULL,
  `order_index` int DEFAULT NULL,
  `page_number` int DEFAULT NULL,
  `is_master` tinyint(1) DEFAULT NULL,
  `is_overall_rating` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `campaign_questions`
--

INSERT INTO `campaign_questions` (`id`, `campaign_id`, `master_question_id`, `question_text_en`, `question_text_hi`, `question_type`, `is_required`, `order_index`, `page_number`, `is_master`, `is_overall_rating`) VALUES
(1, 1, NULL, 'KAISE HOH', NULL, 'rating_1_5', 1, 1, 1, 0, 0),
(2, 2, 1, 'Overall, how would you rate your experience with Dr Bhasin’s Lab?', NULL, 'rating_1_5', 1, 1, 1, 1, 1),
(3, 2, 3, 'How likely are you to recommend Dr Bhasin’s Lab for the care, comfort, and confidence you experienced?', NULL, 'mcq_single', 0, 3, 1, 1, 0),
(4, 2, NULL, 'Which part of your visit made you feel most comfortable or confident?', NULL, 'mcq_multi', 1, 2, 1, 0, 0),
(5, 2, NULL, 'Is there anything we could improve to make future visits even better for you?', NULL, 'mcq_multi', 1, 4, 1, 0, 0),
(6, 2, NULL, 'Is there any staff member or moment during your visit that you would like to acknowledge or appreciate?', NULL, 'text', 0, 5, 1, 0, 0),
(7, 2, NULL, 'If there’s anything at all you’d like us to know — big or small — please feel free to share it here.', NULL, 'text', 0, 6, 1, 0, 0),
(8, 2, NULL, 'Before today, which of the following services were you already aware that Dr Bhasin’s Lab provides?', NULL, 'mcq_multi', 1, 7, 1, 0, 0),
(9, 2, NULL, 'Which part of your visit could we improve to serve you better?', NULL, 'mcq_multi', 1, 8, 1, 0, 0),
(10, 2, NULL, 'During your visit, did you feel listened to and treated with care?', NULL, 'mcq_single', 0, 9, 1, 0, 0),
(11, 2, NULL, 'In your own words, how would you describe your experience with us today?', NULL, 'text', 0, 10, 1, 0, 0),
(12, 2, 3, 'How likely are you to recommend Dr Bhasin’s Lab for the care, comfort, and confidence you experienced?', NULL, 'mcq_multi', 1, 11, 1, 1, 0),
(13, 2, NULL, 'We’re really sorry your experience did not meet expectations. Could you please tell us what went wrong?', NULL, 'text', 1, 12, 1, 0, 0),
(14, 2, NULL, 'Which part of your experience caused the most concern?', NULL, 'mcq_multi', 1, 13, 1, 0, 0);

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
(1, 1, '5', 'BADIYA', NULL, 'positive', NULL, NULL, 5, 1, NULL),
(2, 1, '1', 'LAGE HUYE HAH', NULL, 'negative', NULL, NULL, 0, 2, NULL),
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
(63, 2, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1, 5, NULL);

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
(1, 1, 1, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(2, 2, 1, NULL, '[\"1\"]', 'negative', NULL, NULL, 0, NULL),
(3, 3, 1, NULL, '[\"1\"]', 'negative', NULL, NULL, 0, NULL),
(4, 4, 1, NULL, '[\"5\"]', 'positive', NULL, NULL, 5, NULL),
(5, 5, 1, NULL, '[\"1\"]', 'negative', NULL, NULL, 0, NULL),
(6, 6, 1, NULL, '[\"1\"]', 'negative', NULL, NULL, 0, NULL),
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
(32, 8, 14, NULL, '[]', NULL, NULL, NULL, NULL, NULL);

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
(1, 1, NULL, '2025-12-20 09:09:40', 'en', 5, 'positive', NULL, 0, 0, NULL, 'auto_processed', NULL),
(2, 1, NULL, '2025-12-20 09:10:07', 'en', 0, 'negative', NULL, 0, 1, 1, 'under_review', NULL),
(3, 1, NULL, '2025-12-22 12:54:38', 'en', 0, 'negative', NULL, 0, 1, 2, 'under_review', NULL),
(4, 1, NULL, '2025-12-23 06:22:39', 'en', 5, 'positive', NULL, 0, 0, NULL, 'auto_processed', NULL),
(5, 1, NULL, '2025-12-23 07:17:03', 'en', 0, 'negative', NULL, 0, 1, 3, 'under_review', NULL),
(6, 1, NULL, '2025-12-23 07:19:15', 'en', 0, 'negative', NULL, 0, 1, 4, 'under_review', NULL),
(7, 2, NULL, '2025-12-23 10:10:23', 'en', 0, 'negative', NULL, 0, 1, 5, 'under_review', NULL),
(8, 2, NULL, '2025-12-24 06:20:56', 'en', 2, 'negative', 5, 0, 1, 6, 'under_review', '{\"name\": \"VISHU\", \"lab_id\": \"102511111\", \"visit_date\": \"0002-12-24\", \"mobile_number\": \"9810637037\", \"mobile_country\": \"+91\"}');

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
(1, 'TKT-2', 2, 1, '2025-12-20 09:10:07', NULL, NULL, 'high', 'closed', 'happy', NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(2, 'TKT-3', 3, 1, '2025-12-22 12:54:39', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(3, 'TKT-5', 5, 1, '2025-12-23 07:17:04', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(4, 'TKT-6', 6, 1, '2025-12-23 07:19:16', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(5, 'TKT-7', 7, 2, '2025-12-23 10:10:24', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint'),
(6, 'TKT-8', 8, 2, '2025-12-24 06:20:56', NULL, NULL, 'high', 'open', NULL, NULL, 'Complaint triggered by low rating', 'System generated ticket for complaint');

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
  `is_active` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `master_questions`
--

INSERT INTO `master_questions` (`id`, `code`, `default_text_en`, `default_text_hi`, `question_type`, `is_active`) VALUES
(1, 'Exp_Lab', 'Overall, how would you rate your experience with Dr Bhasin’s Lab?', NULL, 'rating_1_5', 1),
(3, 'NPS_Lab', 'How likely are you to recommend Dr Bhasin’s Lab for the care, comfort, and confidence you experienced?', NULL, 'mcq_multi', 1);

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
(16, 1, '1', 'Very Poor – Unacceptable experience', NULL, 'negative', NULL, NULL, 1);

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

--
-- Dumping data for table `ticket_updates`
--

INSERT INTO `ticket_updates` (`id`, `ticket_id`, `updated_at`, `updated_by_user_id`, `update_text`, `attachment_path`, `next_action_due_date`) VALUES
(1, 1, '2025-12-20 09:10:40', 1, 'MAR JAA PHIR BC', NULL, NULL),
(2, 1, '2025-12-20 09:10:52', 1, 'MAR GAYA HAH BKL', NULL, NULL);

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
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `campaign_question_options`
--
ALTER TABLE `campaign_question_options`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `campaign_recipients`
--
ALTER TABLE `campaign_recipients`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `campaign_recipient_lists`
--
ALTER TABLE `campaign_recipient_lists`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `feedback_files`
--
ALTER TABLE `feedback_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback_responses`
--
ALTER TABLE `feedback_responses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `feedback_rewards`
--
ALTER TABLE `feedback_rewards`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `feedback_tickets`
--
ALTER TABLE `feedback_tickets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `master_questions`
--
ALTER TABLE `master_questions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `master_question_options`
--
ALTER TABLE `master_question_options`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

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

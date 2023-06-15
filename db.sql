-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: auction_db
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auctions_bid`
--

DROP TABLE IF EXISTS `auctions_bid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions_bid` (
  `id` int NOT NULL AUTO_INCREMENT,
  `highest_bid` decimal(10,2) NOT NULL,
  `added` datetime(6) NOT NULL,
  `listing_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_bids_user_id_ab75699a_fk_auctions_user_id` (`user_id`),
  KEY `auctions_bid_listing_id_4b09b47f_fk_auctions_listing_id` (`listing_id`),
  CONSTRAINT `auctions_bid_listing_id_4b09b47f_fk_auctions_listing_id` FOREIGN KEY (`listing_id`) REFERENCES `auctions_listing` (`id`),
  CONSTRAINT `auctions_bids_user_id_ab75699a_fk_auctions_user_id` FOREIGN KEY (`user_id`) REFERENCES `auctions_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_bid`
--

LOCK TABLES `auctions_bid` WRITE;
/*!40000 ALTER TABLE `auctions_bid` DISABLE KEYS */;
INSERT INTO `auctions_bid` VALUES (1,120.00,'2023-06-11 13:51:02.374735',1,4),(2,110.00,'2023-06-11 14:03:47.471175',6,5),(3,510.00,'2023-06-15 13:10:19.251071',7,6);
/*!40000 ALTER TABLE `auctions_bid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_comment`
--

DROP TABLE IF EXISTS `auctions_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` varchar(400) NOT NULL,
  `added` datetime(6) NOT NULL,
  `listing_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_comments_user_id_54638d2d_fk_auctions_user_id` (`user_id`),
  KEY `auctions_comment_listing_id_2f600ca5_fk_auctions_listing_id` (`listing_id`),
  CONSTRAINT `auctions_comment_listing_id_2f600ca5_fk_auctions_listing_id` FOREIGN KEY (`listing_id`) REFERENCES `auctions_listing` (`id`),
  CONSTRAINT `auctions_comments_user_id_54638d2d_fk_auctions_user_id` FOREIGN KEY (`user_id`) REFERENCES `auctions_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_comment`
--

LOCK TABLES `auctions_comment` WRITE;
/*!40000 ALTER TABLE `auctions_comment` DISABLE KEYS */;
INSERT INTO `auctions_comment` VALUES (1,'hello i am the owner of this auction\r\n','2023-06-10 19:41:25.218431',5,3),(2,'hi\r\n','2023-06-11 13:42:26.065650',1,4),(3,'hello\r\n','2023-06-11 18:22:41.917304',1,5),(4,'hi','2023-06-13 17:26:48.302016',6,4),(5,'hey','2023-06-15 13:11:45.129658',9,6),(6,'hello\r\n','2023-06-15 13:13:55.805422',9,6),(7,'','2023-06-15 13:16:03.442568',9,6),(8,'','2023-06-15 13:18:53.098758',9,6);
/*!40000 ALTER TABLE `auctions_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_listing`
--

DROP TABLE IF EXISTS `auctions_listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions_listing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `initial` decimal(10,2) NOT NULL,
  `image` varchar(100) NOT NULL,
  `created` date NOT NULL,
  `category` varchar(11) NOT NULL,
  `status` varchar(7) NOT NULL,
  `user_id` int NOT NULL,
  `description` longtext NOT NULL DEFAULT (_utf8mb3''),
  `auction_end_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auctions_listing_user_id_eea611cc_fk_auctions_user_id` (`user_id`),
  CONSTRAINT `auctions_listing_user_id_eea611cc_fk_auctions_user_id` FOREIGN KEY (`user_id`) REFERENCES `auctions_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_listing`
--

LOCK TABLES `auctions_listing` WRITE;
/*!40000 ALTER TABLE `auctions_listing` DISABLE KEYS */;
INSERT INTO `auctions_listing` VALUES (1,'Art',100.00,'photo-1579783902614-a3fb3927b6a5.png','2023-06-11','Antiques','Pending',3,'','2023-06-16 12:16:06.700213','2023-06-11 12:59:30.000000','2023-06-11 12:59:30.000000'),(2,'cozy art',150.00,'photo-1467646208740-18124b37eb58.png','2023-06-11','Antiques','Closed',3,'',NULL,'2023-06-11 12:59:30.189033','2023-06-11 12:59:30.515266'),(3,'Sneakers',140.00,'photo-1588099768531-a72d4a198538.png','2023-06-11','Other','Pending',3,'',NULL,'2023-06-11 12:59:30.189033','2023-06-11 12:59:30.515266'),(4,'Decoration',99.00,'photo-1567225557594-88d73e55f2cb.png','2023-06-11','Decoration','Pending',3,'',NULL,'2023-06-11 12:59:30.189033','2023-06-11 12:59:30.515266'),(5,'fancy art',500.00,'photo-1579783902614-a3fb3927b6a5_SaGE67K.png','2023-06-11','Antiques','Pending',3,'',NULL,'2023-06-11 12:59:30.189033','2023-06-11 12:59:30.515266'),(6,'Mug',100.00,'mug_76cP0Bp.jpg','2023-06-11','Decoration','Pending',4,'a mug for tea','2023-06-12 13:05:13.429881','2023-06-12 18:04:00.000000','2023-06-11 18:04:00.000000'),(7,'Cactus',500.00,'cactus-decor_3F7Yet7.jpeg','2023-06-14','Decoration','Pending',4,'Home decoration','2023-06-15 11:03:44.882437','2023-06-15 16:03:00.000000','2023-06-14 16:03:00.000000'),(8,'shoes pair',400.00,'sneakers-new_hj6pkUl.jpg','2023-06-15','Other','Closed',6,'Stylish and Comfortable pair of shoes to wear for men','2023-06-16 12:30:13.693452','2023-06-24 17:30:00.000000','2023-06-15 17:30:00.000000'),(9,'Camera  for decor',50.00,'camera-old_Yemnfbv.jpg','2023-06-15','Decoration','Pending',6,'decoration piece','2023-06-16 12:45:10.758511','2023-06-20 17:45:00.000000','2023-06-15 17:45:00.000000'),(10,'book',40.00,'CIR-book_A0wClQf.jpg','2023-06-15','Decoration','Closed',6,'book','2023-06-16 12:46:02.354781','2023-06-15 17:47:00.000000','2023-06-15 17:45:00.000000');
/*!40000 ALTER TABLE `auctions_listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_user`
--

DROP TABLE IF EXISTS `auctions_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_user`
--

LOCK TABLES `auctions_user` WRITE;
/*!40000 ALTER TABLE `auctions_user` DISABLE KEYS */;
INSERT INTO `auctions_user` VALUES (1,'pbkdf2_sha256$390000$OA2vAMniQQ8DqmB61133qp$ONY+PwoarTO0y5xDGIG1/Z94Go5+t6vkc+heGJV/SpU=','2023-06-10 17:57:12.352864',1,'hamza','','','hamzaazeem023@gmail.com',1,1,'2023-06-10 17:56:41.708453'),(3,'pbkdf2_sha256$390000$idh6QS259hhmrOdmk75wwU$XyaaXXuINLxLJl4ID+9lOsBOYmpRCH9bYUEekq2lTDw=','2023-06-10 19:25:00.194797',0,'Hamza Azeem','','','hamza@gmail.com',0,1,'2023-06-10 19:24:59.292477'),(4,'pbkdf2_sha256$390000$NSLYclg2p0JnqBpZUIQf5o$ihwHQWVDLFQ8qvIg4LJ9/pRr6FrtqCz4QVhh6v1sl5k=','2023-06-13 13:49:01.179091',0,'azeem','','','azeem@gmail.com',0,1,'2023-06-11 11:43:20.363526'),(5,'pbkdf2_sha256$390000$d4YrTlskh8AUzpgBMA8B0N$71p+QBF+bOkpWpMCD/I0intbD6In2JFsqTOGefcdvhI=','2023-06-11 14:02:45.623982',0,'zeeshan','','','zeeshan123@gmail.com',0,1,'2023-06-11 14:02:44.862829'),(6,'pbkdf2_sha256$390000$s0rExAOt16vN9rB4gvjjWk$o/SGEDETsMK/gGRsiXJRmJ4uVd13ZL0kPh7YmprG98M=','2023-06-14 13:06:07.513182',0,'HamzaAzeem','','','hamzaazeem023@gmail.com',0,1,'2023-06-14 13:06:04.597057');
/*!40000 ALTER TABLE `auctions_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_user_groups`
--

DROP TABLE IF EXISTS `auctions_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auctions_user_groups_user_id_group_id_1f941809_uniq` (`user_id`,`group_id`),
  KEY `auctions_user_groups_group_id_beef25ba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auctions_user_groups_group_id_beef25ba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auctions_user_groups_user_id_cdaa1ab3_fk_auctions_user_id` FOREIGN KEY (`user_id`) REFERENCES `auctions_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_user_groups`
--

LOCK TABLES `auctions_user_groups` WRITE;
/*!40000 ALTER TABLE `auctions_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auctions_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auctions_user_user_permissions`
--

DROP TABLE IF EXISTS `auctions_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auctions_user_user_permi_user_id_permission_id_f092bc2e_uniq` (`user_id`,`permission_id`),
  KEY `auctions_user_user_p_permission_id_6cab40d7_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auctions_user_user_p_permission_id_6cab40d7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auctions_user_user_p_user_id_fec24fe0_fk_auctions_` FOREIGN KEY (`user_id`) REFERENCES `auctions_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions_user_user_permissions`
--

LOCK TABLES `auctions_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auctions_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auctions_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_user'),(2,'Can change user',1,'change_user'),(3,'Can delete user',1,'delete_user'),(4,'Can view user',1,'view_user'),(5,'Can add bid',2,'add_bid'),(6,'Can change bid',2,'change_bid'),(7,'Can delete bid',2,'delete_bid'),(8,'Can view bid',2,'view_bid'),(9,'Can add comment',3,'add_comment'),(10,'Can change comment',3,'change_comment'),(11,'Can delete comment',3,'delete_comment'),(12,'Can view comment',3,'view_comment'),(13,'Can add listing',4,'add_listing'),(14,'Can change listing',4,'change_listing'),(15,'Can delete listing',4,'delete_listing'),(16,'Can view listing',4,'view_listing'),(17,'Can add log entry',5,'add_logentry'),(18,'Can change log entry',5,'change_logentry'),(19,'Can delete log entry',5,'delete_logentry'),(20,'Can view log entry',5,'view_logentry'),(21,'Can add permission',6,'add_permission'),(22,'Can change permission',6,'change_permission'),(23,'Can delete permission',6,'delete_permission'),(24,'Can view permission',6,'view_permission'),(25,'Can add group',7,'add_group'),(26,'Can change group',7,'change_group'),(27,'Can delete group',7,'delete_group'),(28,'Can view group',7,'view_group'),(29,'Can add content type',8,'add_contenttype'),(30,'Can change content type',8,'change_contenttype'),(31,'Can delete content type',8,'delete_contenttype'),(32,'Can view content type',8,'view_contenttype'),(33,'Can add session',9,'add_session'),(34,'Can change session',9,'change_session'),(35,'Can delete session',9,'delete_session'),(36,'Can view session',9,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auctions_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auctions_user_id` FOREIGN KEY (`user_id`) REFERENCES `auctions_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'admin','logentry'),(2,'auctions','bid'),(3,'auctions','comment'),(4,'auctions','listing'),(1,'auctions','user'),(7,'auth','group'),(6,'auth','permission'),(8,'contenttypes','contenttype'),(9,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-06-10 17:52:52.717641'),(2,'contenttypes','0002_remove_content_type_name','2023-06-10 17:52:53.619840'),(3,'auth','0001_initial','2023-06-10 17:52:55.720884'),(4,'auth','0002_alter_permission_name_max_length','2023-06-10 17:52:55.917096'),(5,'auth','0003_alter_user_email_max_length','2023-06-10 17:52:55.988404'),(6,'auth','0004_alter_user_username_opts','2023-06-10 17:52:56.026466'),(7,'auth','0005_alter_user_last_login_null','2023-06-10 17:52:56.059447'),(8,'auth','0006_require_contenttypes_0002','2023-06-10 17:52:56.082459'),(9,'auth','0007_alter_validators_add_error_messages','2023-06-10 17:52:56.115356'),(10,'auth','0008_alter_user_username_max_length','2023-06-10 17:52:56.148336'),(11,'auth','0009_alter_user_last_name_max_length','2023-06-10 17:52:56.205300'),(12,'auth','0010_alter_group_name_max_length','2023-06-10 17:52:56.372104'),(13,'auth','0011_update_proxy_permissions','2023-06-10 17:52:56.433695'),(14,'auctions','0001_initial','2023-06-10 17:53:03.386829'),(15,'admin','0001_initial','2023-06-10 17:53:06.455953'),(16,'admin','0002_logentry_remove_auto_add','2023-06-10 17:53:06.597006'),(17,'admin','0003_logentry_add_action_flag_choices','2023-06-10 17:53:06.670958'),(18,'auctions','0002_bids_comments_listings','2023-06-10 17:53:08.756022'),(19,'auctions','0003_auto_20201101_1743','2023-06-10 17:53:10.546915'),(20,'auctions','0004_auto_20201102_0012','2023-06-10 17:53:10.676733'),(21,'auctions','0005_auto_20201102_0020','2023-06-10 17:53:10.920425'),(22,'auctions','0006_auto_20201102_0042','2023-06-10 17:53:11.493056'),(23,'auctions','0007_auto_20201104_1446','2023-06-10 17:53:12.231005'),(24,'auctions','0008_listing_user','2023-06-10 17:53:12.874807'),(25,'auctions','0009_auto_20201105_0012','2023-06-10 17:53:12.975881'),(26,'auctions','0010_auto_20201105_0015','2023-06-10 17:53:13.030941'),(27,'auth','0012_alter_user_first_name_max_length','2023-06-10 17:53:13.096784'),(28,'sessions','0001_initial','2023-06-10 17:53:13.484923'),(29,'auctions','0011_listing_description_alter_listing_category','2023-06-11 12:10:30.746331'),(30,'auctions','0012_listing_auction_end_time','2023-06-11 12:55:09.218986'),(31,'auctions','0013_listing_end_time_listing_start_time','2023-06-11 12:59:30.843392');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('gf59ht3h7sc16syowiktblufguuuvz8p','.eJxVjMsOwiAQRf-FtSG8poBL934DGWCQqoGktCvjv2uTLnR7zzn3xQJuaw3boCXMmZ3ZxE6_W8T0oLaDfMd26zz1ti5z5LvCDzr4tWd6Xg7376DiqN9aGUda-kJGggF0WihbTHZEHqOKkxdJUnHWFg2kMZmUchRgi4QSrQD2_gDdSjgP:1q9QCO:JVkVZ4q_IIhca0B9wYT5TpWAf2rjg4_tRCXP54gjho0','2023-06-28 13:06:08.558234');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-16  1:25:33

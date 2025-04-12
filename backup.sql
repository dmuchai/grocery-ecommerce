-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: grocery_db
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('1b103ac2a525');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `session_id` varchar(50) DEFAULT NULL,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,NULL,'5011f23e-7a07-4125-9045-e5cdb51a9165',1,4),(2,NULL,'5011f23e-7a07-4125-9045-e5cdb51a9165',13,1),(3,NULL,'5011f23e-7a07-4125-9045-e5cdb51a9165',3,1),(4,NULL,'5011f23e-7a07-4125-9045-e5cdb51a9165',2,1),(5,NULL,'5011f23e-7a07-4125-9045-e5cdb51a9165',4,1),(6,NULL,'d4f6682c-aacb-4fb4-b903-c63cb4e7a333',8,1),(7,NULL,'31b75fed-be3f-4f91-85d7-59ed1cd914f5',1,3),(8,NULL,'31b75fed-be3f-4f91-85d7-59ed1cd914f5',13,2),(9,NULL,'60a6dd32-4141-4220-86c0-7235af0cdec4',3,1),(10,NULL,'60a6dd32-4141-4220-86c0-7235af0cdec4',4,1),(11,NULL,'31b75fed-be3f-4f91-85d7-59ed1cd914f5',2,2),(12,NULL,'31b75fed-be3f-4f91-85d7-59ed1cd914f5',3,1);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Eggs'),(3,'Fruits'),(2,'Vegetables');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,1,2,450),(2,1,13,1,439),(3,1,3,1,70),(4,1,8,1,120),(5,2,1,1,450),(6,2,13,1,439),(7,3,1,1,450),(8,3,2,1,80),(9,3,3,1,70),(10,4,3,1,70),(11,4,1,1,450),(12,5,3,1,70),(13,5,13,1,439),(14,6,3,1,70),(15,6,4,1,80),(16,6,7,1,99),(17,7,1,1,450),(18,7,3,1,70),(19,7,9,1,60),(20,8,1,1,450),(21,8,2,1,80),(22,8,13,1,439),(23,9,1,1,450),(24,9,2,1,80),(25,9,6,1,60),(26,10,4,2,80),(27,11,5,1,85),(28,11,8,1,120),(29,12,4,1,80),(30,12,7,1,99),(31,13,10,1,80),(32,13,9,1,60),(33,14,3,1,70),(34,14,4,1,80),(35,14,5,1,85),(36,15,6,1,60),(37,15,12,1,85),(38,16,11,1,70),(39,16,8,1,120),(40,17,4,1,80),(41,17,12,1,85),(42,18,2,1,80),(43,18,6,1,60),(44,19,9,3,60),(45,19,6,2,60),(46,19,12,2,85),(47,20,3,2,70),(48,20,8,2,120),(49,21,2,3,80),(50,21,4,1,80),(51,21,3,1,70),(52,22,3,2,70),(53,22,9,2,60),(54,23,2,4,80),(55,23,13,3,439),(56,23,6,2,60),(57,24,3,1,70),(58,24,9,3,60),(59,24,8,4,120),(60,25,4,5,80),(61,25,5,4,85),(62,26,6,3,60),(63,26,13,3,439),(64,26,12,4,85),(65,27,5,2,85),(66,27,10,2,80),(67,27,4,3,80),(68,28,2,1,80),(69,28,1,1,450),(70,28,3,1,70),(71,28,4,1,80),(72,29,9,6,60),(73,29,4,4,80),(74,29,5,10,85),(75,29,3,5,70);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total_price` float NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `guest_identifier` varchar(36) DEFAULT NULL,
  `email` varchar(128) NOT NULL,
  `customer_name` varchar(128) NOT NULL,
  `address` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,0,1529,'Pending','2025-03-19 16:38:02',NULL,'dmmuchai@gmail.com','Dennis Muniu Muchai',''),(2,0,889,'Pending','2025-03-19 16:57:33',NULL,'dmmuchai@gmail.com','Catherine Wambui Kamau',''),(3,0,600,'Pending','2025-03-19 17:28:42',NULL,'johndoe12025@gmail.com','John Doe',''),(4,0,520,'Pending','2025-03-19 21:01:52',NULL,'johnydoh@gmail.com','Johny Doh',''),(5,0,509,'Pending','2025-03-20 00:44:21',NULL,'dmmuchai@gmail.com','Dennis Muniu Muchai',''),(6,0,249,'Pending','2025-03-20 07:21:41',NULL,'dmmuchai@gmail.com','Dennis Muniu Muchai',''),(7,0,580,'Pending','2025-03-21 16:11:11',NULL,'dmmuchai@gmail.com','Dennis Muchai','750 Clopper Rd'),(8,0,969,'Pending','2025-03-21 16:24:19',NULL,'dmmuchai@gmail.com','Dennis Muchai','750 Clopper Rd'),(9,0,590,'Pending','2025-03-21 16:43:22',NULL,'dmmuchai@gmail.com','Catherine Wambui Kamau','Wangige'),(10,0,160,'Pending','2025-03-21 16:58:50',NULL,'catekama69@gmail.com','Catherine Wambui Kamau','Getathuru Road'),(11,0,205,'Pending','2025-03-21 17:06:24',NULL,'janedoh@gmail.com','Jane doh','Jane Doh Road'),(12,0,179,'Pending','2025-03-21 18:05:35',NULL,'jonht@gmail.com','Johnny Doh','Haile Selassie Avenue, Nairobi'),(13,0,140,'Pending','2025-03-21 19:40:32',NULL,'jaynedoe@gmail.com','Jayne Doe','Jayne D Street'),(14,0,235,'Pending','2025-03-21 22:49:47',NULL,'pcartney@gmail.com','Paul Mcartney','PCartney Wangige Rd'),(15,0,145,'Pending','2025-03-22 12:40:57',NULL,'janitadow@gmail.com','Janita Dow','Kabete rd'),(16,0,190,'Pending','2025-03-22 13:21:38',NULL,'janettedoeh@gmail.com','Janette Doeh','Kitisuru rd'),(17,0,165,'Pending','2025-03-22 13:24:24',NULL,'johniedow@gmail.com','Johnie Dow','Ruaka Rd'),(18,0,140,'Pending','2025-03-22 13:26:57',NULL,'joedoh@gmail.com','Joe Doh','Ndenderu rd'),(19,0,470,'Pending','2025-03-25 10:34:17',NULL,'johniedoe@gmail.com','Johnie Doe Jnr','Gatanga Road'),(20,0,380,'Pending','2025-03-25 10:39:07',NULL,'johniedoesr@gmail.com','Johnie Doe Snr','Mararo Road'),(21,0,390,'Pending','2025-03-27 17:05:14',NULL,'johniedoew@gmail.com','Johnie Doew','Getathuru Road'),(22,0,260,'Pending','2025-03-27 17:15:51',NULL,'catherinedoe@gmail.com','Catherine Doe','Getathuru Road'),(23,2,1757,'Pending','2025-04-04 18:31:01',NULL,'rickjunior@gmail.com','Richard Junior','Kangundo Rd'),(24,2,730,'Pending','2025-04-06 13:36:41',NULL,'sophiawanjiku2016@gmail.com','Sophia Wanjiku','Wangige'),(25,3,740,'Pending','2025-04-06 17:13:05',NULL,'dannymacharia5000@gmail.com','Danny Macharia','City Park'),(26,5,1837,'Pending','2025-04-06 21:07:12',NULL,'patrickmuchai20000@gmail.com','Patrick Muchai','Kasarani Rd'),(27,0,570,'Pending','2025-04-06 21:10:42','9fc55c14-b807-4e22-b17f-dd1c45b250f2','hkimani20000@gmail.com','Harry Kim','Muthaiga Avenue'),(28,2,680,'Pending','2025-04-09 15:28:47',NULL,'sophiawanjiku2016@gmail.com','Sophia Wanjiku','Wangige'),(29,5,1880,'Pending','2025-04-09 19:57:16',NULL,'patrickmuchai20000@gmail.com','Patrick Muchai','Ngecha Road');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `price` float NOT NULL,
  `stock` int NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Eggs','Eggs crate 30 pack',450,50,'eggs.jpg',1),(2,'Pineapples','Fresh tropical pineapples per Kg',80,30,'pineapples.jpg',3),(3,'Tomatoes','Fresh tomatoes per Kg',70,50,'tomatoes.jpg',2),(4,'Red Onions','Fresh red onions per Kg',80,30,'onions.jpg',2),(5,'Irish Potatoes','Farm Fresh Irish Potatoes per Kg',85,40,'potatoes.jpg',2),(6,'Water Melon','Farm Fresh Water Melon per Kg',60,60,'watermelon.jpg',3),(7,'Pawpaw','Pawpaw per kg',99,50,'pawpaw.jpg',3),(8,'Arrowroots','Arrowroot per kg',120,30,'arrowroot.jpg',2),(9,'Carrots','Carrot per kg',60,40,'carrot.jpg',2),(10,'Matoke','Matoke per kg',80,60,'matoke.jpg',2),(11,'Sweet Potatoes','Sweet Potatoes per kg',70,50,'sweetpotatoes.jpg',2),(12,'Ripe Bananas','Ripe Bananas per kg',85,30,'banana.jpg',3),(13,'Apples Red','Crisp Red Apples per Kg',439,25,'apples.jpg',3);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(200) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'testuser','testuser@example.com','pbkdf2:sha256:1000000$YDJh3n7vY8htqQf5$171e667380be30acb54c03c8c02b8173054de9c5f006904bb5df9a48d0595a81','2025-03-11 01:22:30'),(2,'swanjiku','sophiawanjiku2016@gmail.com','pbkdf2:sha256:1000000$Z0nEUU1fsDvTPIYq$93a21e0914a8e269a63f4e3c6dd2db8387d8d0d5edcc7fb56c40115edd405913','2025-04-02 20:54:13'),(3,'DannyM','dannymacharia5000@gmail.com','pbkdf2:sha256:1000000$dHAO2tpFpyzdM5o7$34502300630acc29f2bd57da2316ad9efa49e78c9bd144f35668e72c5798d57b','2025-04-06 16:09:12'),(4,'DKamau','derrickkamau20000@gmail.com','pbkdf2:sha256:1000000$PlVUTkK45rd5EyFe$ffb8201f09e55f5efe70bdb7926b186809111855e7e897bd02004eb99a9b01d2','2025-04-06 17:47:19'),(5,'PMuchai','patrickmuchai20000@gmail.com','pbkdf2:sha256:1000000$iCpTZ9BpzCEXSUxT$9ac2e963e36aaab77325780eda655c60bec9c5469abeaeb707dcaeb012ef4a33','2025-04-06 17:58:02');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-11 18:04:40

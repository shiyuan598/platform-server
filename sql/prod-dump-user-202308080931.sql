-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 172.16.12.84    Database: user
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `app`
--

DROP TABLE IF EXISTS `app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app`
--

LOCK TABLES `app` WRITE;
/*!40000 ALTER TABLE `app` DISABLE KEYS */;
INSERT INTO `app` VALUES (1,'user','用户管理平台',NULL),(2,'vehicle','车辆管理平台',NULL),(3,'integration','集成平台',NULL),(4,'data','数据平台',NULL),(5,'monitor','数据上传监控',NULL);
/*!40000 ALTER TABLE `app` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knex_migrations`
--

DROP TABLE IF EXISTS `knex_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knex_migrations` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `batch` int DEFAULT NULL,
  `migration_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knex_migrations`
--

LOCK TABLES `knex_migrations` WRITE;
/*!40000 ALTER TABLE `knex_migrations` DISABLE KEYS */;
INSERT INTO `knex_migrations` VALUES (4,'20230801083129_add_sex_to_user.js',1,'2023-08-02 09:45:40');
/*!40000 ALTER TABLE `knex_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knex_migrations_lock`
--

DROP TABLE IF EXISTS `knex_migrations_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knex_migrations_lock` (
  `index` int unsigned NOT NULL AUTO_INCREMENT,
  `is_locked` int DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knex_migrations_lock`
--

LOCK TABLES `knex_migrations_lock` WRITE;
/*!40000 ALTER TABLE `knex_migrations_lock` DISABLE KEYS */;
INSERT INTO `knex_migrations_lock` VALUES (1,0);
/*!40000 ALTER TABLE `knex_migrations_lock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'super','平台管理员','平台管理员，负责权限管理'),(2,'admin','应用管理员','应用系统的管理员，负责审批、编辑数据'),(3,'member','普通用户','普通用户，使用系统的所有功能'),(4,'driver','司机','特殊用户');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '姓名',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(50) NOT NULL COMMENT '密码',
  `telephone` varchar(50) NOT NULL COMMENT '电话号码',
  `desc` varchar(100) DEFAULT NULL COMMENT '描述',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'王士远','wangshiyuan','123','13161507755',NULL,'2023-07-20 06:26:23','2023-05-23 06:04:02'),(2,'杨多多','yhdodo','123','15239177793','不错不错','2023-07-21 09:34:55','2023-05-04 14:32:44'),(3,'马万里','mawanli','123456','17600132186',NULL,'2023-05-23 08:05:52','2023-05-04 14:32:44'),(4,'刘春秋','liuchunqiu','123456','18625168309',NULL,'2023-05-06 09:13:14','2023-05-04 14:32:44'),(5,'薛渊','xueyuan','123456','15605197103',NULL,'2023-05-04 14:32:43','2023-05-04 14:32:44'),(6,'刘清','liuqing','123456','18180827731',NULL,'2023-05-23 05:44:30','2023-05-23 05:43:34'),(7,'孙鹏浩','sunpenghao','123456','19906723916',NULL,'2023-07-07 09:37:54','2023-05-23 07:36:15'),(8,'唐舒放','tangshufang','123456','18795888068',NULL,'2023-07-07 02:30:09','2023-05-23 07:37:23'),(9,'李明星','limingxing','123456','15250955337',NULL,'2023-07-11 08:13:57','2023-05-23 07:37:58'),(10,'杨福威','yangfuwei','123456','18810575382',NULL,'2023-06-26 01:51:12','2023-05-23 07:38:55'),(11,'张浩宇','zhanghaoyu','123456','15810979502',NULL,'2023-07-10 03:10:17','2023-05-23 07:40:27'),(12,'杨巧','yangqiao','123456','13584816399',NULL,'2023-05-23 07:41:00','2023-05-23 07:41:00'),(13,'夏建明','xiajianming','123456','17751271737',NULL,'2023-07-10 01:19:20','2023-05-23 07:41:42'),(14,'周亿文','zhouyiwen','123456','13914056204',NULL,'2023-05-23 08:08:14','2023-05-23 08:08:14'),(15,'集成','integration','123456','1',NULL,'2023-07-11 09:15:46','2023-05-23 08:20:02'),(16,'张希玉','zhangxiyu','123456','18930861132',NULL,'2023-07-10 01:14:44','2023-05-23 09:00:08'),(17,'徐传骆','xuchuanluo','123456','17625802392',NULL,'2023-07-11 01:44:46','2023-05-30 05:58:09'),(18,'代爽','daishuang','533412','13661849554',NULL,'2023-07-03 02:03:07','2023-06-08 08:06:28'),(19,'王鹏飞','wangpengfei','123456','17673055199',NULL,'2023-06-26 01:46:20','2023-06-26 01:46:20'),(20,'平台管理员','root','123','13161507755',NULL,'2023-07-13 01:47:44','2023-07-12 08:14:41'),(54,'杨沉沉','yhifif','123','15239177793','不错不错','2023-08-07 07:22:08','2023-08-07 07:22:08');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_role_UN` (`user_id`,`role_id`,`app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES (1,1,1,1),(2,1,1,2),(3,1,1,3),(4,1,1,4),(5,2,2,2),(6,2,2,3),(7,2,2,4);
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'user'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-08  9:31:28

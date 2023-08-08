-- monitor.logs definition

CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` bigint NOT NULL COMMENT '时间戳',
  `ip` varchar(50) NOT NULL COMMENT 'ip地址',
  `type` int NOT NULL DEFAULT '1' COMMENT '类型：info, error, warn',
  `content` text COMMENT '内容',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
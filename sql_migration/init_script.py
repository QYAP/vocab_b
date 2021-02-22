INIT_SQL = \
    """
SET NAMES utf8mb4;

-- ----------------------------
-- Database structure for vocab
-- ----------------------------
CREATE DATABASE IF NOT EXISTS vocab DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE vocab;
-- ----------------------------
-- Table structure for user
-- ----------------------------
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` varchar(64) NOT NULL COMMENT "用户ID",
    `phone` varchar(11) UNIQUE NOT NULL COMMENT "手机号码",
    `nickname` varchar(30) NOT NULL COMMENT "昵称",
    `password` varchar(64) NOT NULL COMMENT "密码",
    `created_timestamp` bigint NOT NULL COMMENT "创建时间戳",
    `last_updated_timestamp` bigint NOT NULL COMMENT "更新时间戳",
    PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = "用户信息表";

-- ----------------------------
-- Table structure for vocab_book
-- ----------------------------
CREATE TABLE IF NOT EXISTS `vocab_book` (
    `vocab_book_id` varchar(64) NOT NULL COMMENT "生词本ID",
    `user_id` varchar(64) NOT NULL COMMENT "用户ID",
    `vocab_book_name` varchar(50) NOT NULL COMMENT "生词本名称",
    `position` tinyint unsigned NOT NULL COMMENT "生词本位序",
    `desc` varchar(300) NOT NULL DEFAULT "" COMMENT "生词本描述",
    `cover` varchar(300) NOT NULL COMMENT "生词本封面",
    `daily_plan_pass_word` smallint NOT NULL default 10 COMMENT "每日计划词数",
    `remind_or_not` tinyint NOT NULL default -1 COMMENT "是否提醒",
    `created_timestamp` bigint NOT NULL COMMENT "创建时间戳",
    `last_updated_timestamp` bigint NOT NULL COMMENT "更新时间戳",
    PRIMARY KEY (`vocab_book_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = "生词本信息表";

-- ----------------------------
-- Table structure for vocab_word
-- ----------------------------
CREATE TABLE IF NOT EXISTS `vocab_word` (
    `vocab_word_id` varchar(64) NOT NULL COMMENT "生词ID",
    `vocab_book_id` varchar(64) NOT NULL COMMENT "生词本ID",
    `english` varchar(50) NOT NULL COMMENT "英语意思",
    `chinese` varchar(150) NOT NULL DEFAULT "" COMMENT "中文意思",
    `created_timestamp` bigint NOT NULL COMMENT "创建时间戳",
    `last_updated_timestamp` bigint NOT NULL COMMENT "更新时间戳",
    PRIMARY KEY (`vocab_word_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = "生词信息表";

-- ----------------------------
-- Table structure for vocab_word
-- ----------------------------
CREATE TABLE IF NOT EXISTS `review_record` (
    `review_id` varchar(64) NOT NULL COMMENT "复习记录ID",
    `vocab_word_id` varchar(64) NOT NULL COMMENT "生词ID",
    `vocab_book_id` varchar(64) NOT NULL COMMENT "生词本ID",
    `pass_or_not` tinyint NOT NULL default 0 COMMENT "是否通过",
    `created_timestamp` bigint NOT NULL COMMENT "创建时间戳",
    `last_updated_timestamp` bigint NOT NULL COMMENT "更新时间戳",
    PRIMARY KEY (`review_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = "生词复习记录表";
"""

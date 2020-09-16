-- ----------------------------
-- Table structure for users
-- ----------------------------
CREATE TABLE `users` (
  `NO` int(11) NOT NULL AUTO_INCREMENT COMMENT '회원번호',
  `TYPE` tinyint(1) DEFAULT NULL COMMENT '회원타입',
  `NAME` varchar(30) DEFAULT NULL COMMENT '이름',
  `BIRTHDAY` date DEFAULT NULL COMMENT '생년월일',
  `GENDER` tinyint(1) DEFAULT NULL COMMENT '성별',
  `ID` varchar(45) DEFAULT NULL COMMENT '아이디',
  `PW` varchar(60) DEFAULT NULL COMMENT '비밀번호',
  `EMAIL` varchar(45) DEFAULT NULL COMMENT '이메일',
  `REQ_AGE` tinyint(2) DEFAULT NULL COMMENT '케어를원하는아이나이',
  `REQ_DETAIL` varchar(255) DEFAULT NULL COMMENT '신청내용',
  `POSSIBLE_AGE` tinyint(2) DEFAULT NULL COMMENT '케어가능한아이최소연령',
  `SELF_INTRO` varchar(255) DEFAULT NULL COMMENT '자기소개',
  `JOIN_DATE` datetime DEFAULT NULL COMMENT '가입일시',
  PRIMARY KEY (`NO`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='회원테이블';

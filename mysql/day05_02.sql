-- -----------------------------约束------------------------------------------------
-- 添加列级约束
/*

语法：
直接在字段名和类型后面追加 约束类型即可。
只支持：默认、非空、主键、唯一
*/

CREATE DATABASE student;
USE student;

-- 创建学生表
CREATE TABLE stuinfo(
  id INT PRIMARY KEY,  -- 主键
  stuName VARCHAR(20) NOT NULL ,  -- 非空约束
  gender char(1) CHECK(gender='男'OR gender='女'), -- 检查，5.x不生效，8.x生效
  seat INT UNIQUE, -- 职位 唯一
  age INT DEFAULT 18, -- 默认约束
  majorId INT REFERENCES major(id) -- REFERENCES 外键  不生效
);

CREATE TABLE major(
  id INT PRIMARY KEY,
  majorName VARCHAR(20)
);


DESC stuinfo
DESC major

-- 查看stuinfo中的所有索引，包括主键、外键、唯一
SHOW INDEX FROM stuinfo;


INSERT INTO stuinfo(id,stuName,gender,seat,majorId) VALUES
(1,'张三','女',1001,2001)


-- 添加表级约束
/*
语法：
在各个字段的最下面
【constraint 约束名】约束类型（字段名）
*/
-- 表级约束第一种方式
DROP TABLE if EXISTS stuinfo;
-- 创建学生表
CREATE TABLE stuinfo(
  id INT,  
  stuName VARCHAR(20), 
  gender char(1), 
  seat INT, 
  age INT, 
  majorid INT,
  constraint pk PRIMARY KEY(id),  # 主键
  constraint uq UNIQUE(seat),  # 唯一值
  constraint ck CHECK(gender='男'OR gender='女'),  # 检查  foreign
  constraint fk_stuinfo_major FOREIGN KEY(majorid) REFERENCES major(id)   # 外键
  
);

DROP TABLE if EXISTS stuinfo;
-- 表级约束第二种方式
-- 创建学生表
CREATE TABLE stuinfo(
  id INT,  
  stuName VARCHAR(20), 
  gender char(1), 
  seat INT, 
  age INT, 
  majorid INT,
  PRIMARY KEY(id),  # 主键
  UNIQUE(seat),  # 唯一值
  CHECK(gender='男'OR gender='女'),  # 检查  foreign
  FOREIGN KEY(majorid) REFERENCES major(id)   # 外键
);




-- 修改表时添加约束
/*
1、添加列级约束
alter table 表名 modify column 字段名 字段类型 新约束；
2、添加表级约束
alter table 表名 add 【constraint 约束名】 约束类型（字段名） 【外键的引用】;

*/
DROP TABLE if EXISTS stuinfo;
-- 创建学生表
CREATE TABLE stuinfo(
  id INT,  
  stuName VARCHAR(20), 
  gender char(1), 
  seat INT, 
  age INT, 
  majorid INT
);

-- 查看stuinfo中的所有索引，包括主键、外键、唯一
SHOW INDEX FROM stuinfo;

# 1、添加非空约束
ALTER TABLE stuinfo modify column stuName VARCHAR(20) NOT NULL;

# 2、添加默认约束
ALTER TABLE stuinfo modify column age int DEFAULT 18;

# 3、添加主键
  # （3.1）列级约束
  ALTER TABLE stuinfo modify column id int PRIMARY KEY;
  # （3.2）表级约束
--   ALTER TABLE stuinfo ADD PRIMARY KEY(id);

# 4、添加唯一
  #（4.1）列级约束
  ALTER TABLE stuinfo modify column seat INT UNIQUE;
  # （4.2）表级约束
  ALTER TABLE stuinfo ADD UNIQUE(seat);

# 5、添加外键
ALTER TABLE stuinfo ADD constraint fk_stuinfo_major FOREIGN KEY(majorid) REFERENCES major(id);




-- 标识列
/*
又称为自增长列
含义：可以不用手动的插入值，系统提供默认的序列值
特点：
1、标识列必须和主键搭配？不一定，但要求是一个key
2、一个表可以有几个标识列？至多一个
3、标识列的类型只能是数值型
4、标识列可以通过SET auto_increment_increment = 3；设置步长
可以通过手动插入值，设置起始值
*/


CREATE TABLE tab_stu(
  id INT PRIMARY KEY auto_increment,
  name VARCHAR(20)
)

INSERT INTO tab_stu VALUES 
(NULL,'lanzhi')

SHOW VARIABLES LIKE '%auto_increment%'; 

-- 设置步长

SET auto_increment_increment = 3;

TRUNCATE TABLE tab_stu;


-- 修改表时设置标识列

ALTER	TABLE tab_stu MODIFY COLUMN id INT PRIMARY KEY auto_increment;

-- 修改表时删除标识列

ALTER TABLE tab_stu MODIFY COLUMN id INT;

















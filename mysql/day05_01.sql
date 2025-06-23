/*
DDL语言（数据定义语言）
对库和表的管理
1、库的管理
创建、修改、删除
2、表的管理
创建、修改、删除

创建 create
修改 alter
删除 drop
1、库的创建
语法：
create database [if not exists]库名；
2、表的管理
（1）表的创建（*）
语法：
create table 表名（
列名 列的类型 [(长度) 约束],
列名 列的类型 [(长度) 约束],
列名 列的类型 [(长度) 约束],
...
列名 列的类型 [(长度) 约束],
）


*/
-- --------------------------------数据库操作---------------------------------------------
-- 创建数据库 books
CREATE DATABASE if not exists books;


-- 创建
CREATE DATABASE if not exists test;
-- 修改  -- 一般不修改  mysql 5.x版本支持RENAME DATABASE
RENAME DATABASE test TO bigdata35;

-- 更改库的字符集
ALTER DATABASE books CHARACTER SET 'utf8';

-- 删除数据库
DROP DATABASE if EXISTS test;

DROP DATABASE if EXISTS stu;



-- --------------------------------表的创建----------------------------------------
-- 创建book表
CREATE TABLE if NOT EXISTS books.book(
  id INT,  -- 编号
  bName VARCHAR(20) ,  -- 图书的名字
  price DOUBLE,  -- 价格
  authorId INT, -- 作者的编号
  publishDate DATETIME

);

-- 查看表的结构
DESC book;

-- 创建作者表
CREATE TABLE if NOT EXISTS author(
  id INT,
  au_name VARCHAR(20),
  nation VARCHAR(10)
);
-- 查看表的结构
DESC author;


-- 表的修改
/*
语法：
  alter table 表名 add|drop|modify|change column 列名 [列的类型 约束]
*/

# (1)修改列名

DESC book;
ALTER TABLE book change column publishDate pubDate datetime;


# (2)修改列的类型或者是约束

-- datetime 修改成时间戳格式
ALTER TABLE book modify column pubDate timestamp;

# (3)添加新列
ALTER TABLE book add column age int;

# (4)删除列
ALTER TABLE book drop column age;

# (5)修改表名
ALTER TABLE author RENAME TO book_author;



-- 表的删除
/*
语法：
  drop table [if exists] 表名;
*/
DROP TABLE if EXISTS book_author;

SHOW tables;
/*
通用写法
DROP DATABASE IF EXISTS 旧库名;
CREATE DATABASE 新库名;

DROP TABLE IF EXISTS 旧表名;
CREATE TABLE 表名();
*/


-- 表的复制
# （1）插入内容至作者表
INSERT INTO author VALUES
(1,'鲁迅','中国'),
(2,'莫言','中国'),
(3,'孔子','中国'),
(4,'村上春树','日本');

SELECT * from author;
# 第一种 仅仅复制表的结构
CREATE TABLE copy LIKE author;
CREATE TABLE copy_author LIKE author;

# 第二种 复制表的结构 + 数据
CREATE TABLE copy2
SELECT * FROM author;


# 第三种 只复制部分数据
CREATE TABLE copy4
SELECT
  id,
  nation
FROM
  author
WHERE
  nation = '中国';


# 第四种 仅仅复制某些字段
CREATE TABLE copy5
SELECT
  id,
  au_name
FROM
  author
WHERE 0;



CREATE TABLE copy6
SELECT
  id,
  au_name
FROM
  author
WHERE 1;

-- where 1=1 where 1=0
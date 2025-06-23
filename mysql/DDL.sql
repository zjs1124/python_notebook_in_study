/*
DDL语言(数据定义语言)
对库和表的管理
1、库的管理
创建、修改、删除
2、表的管理
创建、修改、删除

创建 create
修改 alter
删除 drop
1、库的创建
语法:
create database [if not exists]库名;
2、表的创建
create table 表名(
列名 列的类型 [(长度)约束]),
列名 列的类型 [(长度) 约束],
列名 列的类型 [(长度) 约束],
列名 列的类型 [(长度) 约束],
...
列名 列的类型 [(长度) 约束],
*/

-- ---------------------数据库操作-------------------------
-- 创建数据库 books
create database if not exists books;

show databases;

-- 创建
create database if not exists test;

-- 修改 --一般不修改 mysql 5.x版本支持RENAME DATABASE
rename database test to bigdata35;

-- 更改库的字符集
alter database books character set 'utf8';

-- 删除数据库
drop database if exists test;

-- -------------------------表的创建-------------------------
-- 创建book表

create table if not exists books.book (
    id int, -- 编号
    bName varchar(20), -- 图书的名字
    price double, -- 价格
    authorId int, -- 作者的编号
    publishDate datetime
);

use books;

show tables;

-- 查看表的结构
desc book;

-- 创建作者表
CREATE TABLE if NOT EXISTS author (
    id INT,
    au_name VARCHAR(20),
    nation VARCHAR(10)
);
-- 查看表的结构
DESC author;
-- 表的修改
/*
语法:
alter table 表名 add|drop|modify|change column 列名[列的类型 约束]

*/

# (1)修改列名
DESC book;

alter table book change column publishDate pubDate datetime;

#(2) 修改列的类型或者是约束

-- datetime 修改成时间戳格式
alter table book modify column pubDate timestamp;

#(3) 添加新列
alter table book add column age int;

#(4) 删除列
alter table book drop column age;

#(5) 修改表名
alter table author rename to book_author;

show tables;

-- 表的删除
/*
语法:
drop table [if exists] 表名;
*/

drop table if exists book_author;

/*
通用写法
drop database if exists 旧库名;
create database 新库名;

drop table if exists 旧表名;
create table 表名();

*/

-- 表的复制
# (1) 插入内容至作者表
insert into author
values(1,'鲁迅','中国'),
(2,'莫言','中国'),
(3,'孔子','中国'),
(4,'村上春树','日本');

SELECT * from author;

show tables;

desc copy

# 第一种 仅仅复制表的结构
create table copy like author;

select * from copy2

# 第二种 复制表的结构 + 数据
create table copy2
select * from author;

use books;
# 第三种 只复制部分数据
CREATE TABLE copy4
SELECT id, nation
FROM author
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

select * from copy5
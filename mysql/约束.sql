-- ---------------------约束--------------------------
-- 添加列级约束
/*

语法:
直接在字段名和类型后面追加 约束类型即可
只支持： 默认、非空、主键、唯一
*/
CREATE DATABASE student;

USE student;

create table stuinfo (
    id int primary key, -- 主键
    stuName varchar(20) not null, -- 非空约束
    gender char(1) check (
        gender = '男'
        or gender = '女'
    ), -- 检查,5.x不生效,8.x生效
    seat int unique, -- 职位 唯一
    age int default 18, -- 默认约束
    majorId int -- references major(id) ---references 外键  不生效
)

desc stuinfo

show index from stuinfo

INSERT INTO
    stuinfo (
        id,
        stuName,
        gender,
        seat,
        majorId
    )
VALUES (1, '张三', '女', 1001, 2001)

-- 添加表级约束
/*
语法：
在各个字段的最下面
【constraint 约束名】约束类型（字段名）
*/
-- 表级约束第一种方式

drop table if exists stuinfo;

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

CREATE TABLE major ( id INT PRIMARY KEY, majorName VARCHAR(20) );

show tables;

show index from stuinfo

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
CREATE TABLE stuinfo (
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
alter table stuinfo modify column  stuName varchar(20) not null;

# 2、添加默认约束
alter table stuinfo modify column age int default 18;

# 3、添加主键
# （3.1）列级约束
alter table stuinfo modify column id int primary key;
# （3.2）表级约束
--   ALTER TABLE stuinfo ADD PRIMARY KEY(id);

# 4、添加唯一
#（4.1）列级约束
alter table stuinfo modify column seat int unique;
# （4.2）表级约束
use student

alter table stuinfo add unique (seat);

# 5、添加外键

alter table stuinfo add constraint fk_stuinfo_major foreign key(majorid) references major(id);

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

create table tab_stu (
    id int primary key auto_increment,
    name varchar(20)
)

-- TCL语言(事务控制语言)
/*
事务:一个或一组sql语句组成的一个执行单元,这个执行单元要么全部执行,要么全部不执行。


案例：转账
兰智	1000
数加	1000

伪SQL
update 表 set 兰智的余额=500 where name = '兰智';

意外 update 表 set 数加的余额 = 1500 where name = '数加';

事务特性：ACID
ACID
原子性：一个事务不可再分割，要么都执行，要么全都不执行
一致性：一个事务执行会使数据从一个一致状态切换到另外一个一致状态
隔离性: 一个事务的执行不受其他事务的干扰
持久性: 一个事务一旦提交，则会永久改变数据库的数据

# mysql的引擎
show engines;

*/
# 查看mysql 事务是否开启

show variables like 'autocommit';

use student;

-- 数据准备
CREATE TABLE if not EXISTS account (
    id int PRIMARY KEY auto_increment,
    username VARCHAR(20),
    balance DOUBLE
);

-- 插入数据
INSERT INTO
    account (username, balance)
VALUES ('兰智', 1000),
    ('数加', 1000);

select * from account

/*
事务创建
分类：
（1）隐式事务：事务没有明显的开启和结束标记
比如：insert、update、delete语句
（2）显示事务:事务有明显的开启和结束标记
show VARIABLES LIKE 'autocommit';  -- 查看
步骤：
注意：（前提）必须先设置自动提交功能禁用
set autocommit=0;
(1)开启事务
set autocommit=0;
start transaction;   -- 可选
(2)编写事务中的sql语句（select、insert、update、delete....）
语法1;
语法2;
....
(3)结束事务
commit;  -- 提交事务
rollback; -- 回调事务
savepoint; -- 节点名，设置保存点   


开启事务;
update 表 set 兰智的余额=500 where name = '兰智';
update 表 set 数加的余额=1500 where name = '数加';
结束事务;

*/

show variables like 'autocommit';

# 演示事务
# (1) 开启事务
set autocommit = 0;

start transaction;
#(2) 编写一组事务的sql语句
-- SELECT * FROM account
-- 兰智向数加转账500元

update account set balance = 500 where username = '兰智';

update account set balance = 1500 where username = '数加';

select * from account;

# (3)结束事务(提交)
-- commit;
-- 提交
-- 回滚
rollback;
-- 提交
commit;

-- 事务隔离级别
/*
脏读					不可重复读					幻读
read uncommitted		✅						✅							✅
read committed			❌						✅							✅
repeatable read			❌						❌							✅
serializable 				❌						❌							❌

mysql中默认 第三个隔离级别 repeatable read
查看隔离级别
select @@transaction_isolation;
设置隔离级别
set session|global transaction isolation level 隔离级别； 
*/

select @@transaction_isolation;

set session transaction isolation level serializable;

select @@transaction_isolation;

set session transaction isolation level repeatable read;

-- 视图
/*
含义：虚拟表，和普通表一样使用。
mysql5.1版本出现的新特性，是通过表动态生成的数据。
*/

# eg 查询姓张的学生名和专业名

INSERT INTO stuinfo VALUES
(1,'张三','男',1001,NULL,2001),
(2,'张五','男',1002,20,2002),
(3,'张六','男',1003,21,2003),
(4,'王三','男',1004,22,2004),
(5,'王四','男',1005,23,2002);

INSERT INTO
    major
VALUES (2001, '计科'),
    (2002, '统计'),
    (2003, '大数据'),
    (2004, '软工');

SELECT * FROM stuinfo

SELECT * FROM major

SELECT stuName, majorName
FROM stuinfo s
    INNER JOIN major m ON s.majorid = m.id
WHERE
    s.stuName LIKE '张%';

-- 将经常使用的封装起来
create view v1;

-- 根据视图筛选出姓张的学生
SELECT * FROM v1 where stuName LIKE '张%'

/*
创建视图
语法：
create view 视图名
as 
查询语句;

*/

-- eg 查询姓中包含a字符的员工名、部门名和工种信息
show databases;

use myemployee;
-- 创建视图
CREATE VIEW v2 -- stuinfo_view
AS
SELECT
    last_name,
    department_name,
    job_title
from
    employees e
    JOIN departments d ON e.department_id = d.department_id
    JOIN jobs j ON j.job_id = e.job_id;

SELECT * FROM v2 WHERE last_name like '%a%'

/*
修改视图
方式一：
create or replace view 视图名
as 
查询语句；

方式二：
alter view 视图名
as 
查询语句；
*/

create or replace view v2 as
SELECT last_name, department_name
from employees e
    JOIN departments d ON e.department_id = d.department_id

alter view v2 as
SELECT
    last_name,
    department_name,
    job_title
from
    employees e
    JOIN departments d ON e.department_id = d.department_id
    JOIN jobs j ON j.job_id = e.job_id;

/*
删除视图
语法：
drop view 视图名，视图名......;

*/
DROP VIEW v2;

select database();
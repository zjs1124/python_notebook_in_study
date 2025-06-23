-- TCL语言（事务控制语言）
/*
事务：一个或一组sql语句组成一个执行单元，这个执行单元要么全部执行，要么全部不执行。


案例：转账
兰智	1000
数加	1000

伪SQL
update 表 set 兰智的余额=500 where name = '兰智';
意外
update 表 set 数加的余额=1500 where name = '数加';



事务特性：ACID
ACID
原子性：一个事务不可再分割，要么都执行要么都不执行
一致性：一个事务执行会使数据从一个一致状态切换到另一外一个一致状态
隔离性（*）：一个事务的执行不受其他事务的干扰
持久性：一个事务一旦提交，则会永久的改变数据库的数据



# mysql的引擎

show engines;
*/

# 查看mysql事务是否开启
show VARIABLES LIKE 'autocommit';


-- 数据准备
CREATE TABLE if not EXISTS account(

  id int PRIMARY KEY auto_increment,
  username VARCHAR(20),
  balance DOUBLE
);

-- 插入数据
INSERT INTO account(username,balance) VALUES
('兰智',1000),
('数加',1000);

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


show VARIABLES LIKE 'autocommit';
# 演示事务
# (1)开启事务
set autocommit=0;
start transaction;  -- 可选

# (2)编写一组事务的sql语句
-- SELECT * FROM account
-- 兰智向数加转账500元
UPDATE account SET balance = 500 WHERE username='兰智';
UPDATE account SET balance = 1500 WHERE username='数加';
SELECT * FROM account
# (3)结束事务（提交）
-- COMMIT;
-- 回滚
ROLLBACK;
-- 提交
COMMIT;



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

set session transaction isolation level read committed;


show VARIABLES LIKE 'autocommit';
-- savepoint 节点名; 设置保存点
set autocommit=0;
START TRANSACTION;
DELETE FROM account WHERE id= 1;
SAVEPOINT a; -- 设置保存点 
DELETE FROM account WHERE id= 2;
ROLLBACK TO a; -- 回滚到保存点 

SELECT * FROM account



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

INSERT INTO major VALUES
(2001,'计科'),
(2002,'统计'),
(2003,'大数据'),
(2004,'软工');


SELECT * FROM stuinfo
SELECT * FROM major



SELECT
  stuName,
  majorName
FROM
  stuinfo s 
INNER JOIN major m 
ON s.majorid = m.id
WHERE
  s.stuName LIKE '张%';


-- 将经常使用的封装起来
CREATE VIEW v1

-- 根据视图筛选出姓张的学生
SELECT * FROM v1 where stuName LIKE '张%'


/*
创建视图
语法：
create view 视图名
as
查询语句；

*/



-- eg 查询姓中包含a字符的员工名、部门名和工种信息

-- 创建视图
CREATE VIEW v2   -- stuinfo_view
AS
SELECT
  last_name,
  department_name,
  job_title
from
  employees e 
JOIN departments d 
ON e.department_id = d.department_id
JOIN jobs j 
ON j.job_id = e.job_id;



-- 过滤

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


CREATE or replace  VIEW v2   -- stuinfo_view
AS
SELECT
  last_name,
  department_name
from
  employees e 
JOIN departments d 
ON e.department_id = d.department_id



alter view v2   -- stuinfo_view
AS
SELECT
  last_name,
  department_name,
  job_title
from
  employees e 
JOIN departments d 
ON e.department_id = d.department_id
JOIN jobs j 
ON j.job_id = e.job_id;


/*
删除视图
语法：
drop view 视图名，视图名......;

*/


DROP VIEW v2;

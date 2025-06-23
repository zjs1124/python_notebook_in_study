-- 创建数据库
CREATE DATABASE stu;



-- 创建女神表
CREATE TABLE beauty(
  id INT,
  name VARCHAR(50),
  sex CHAR(1) DEFAULT('女'),
  boyfriend_id INT

)


SELECT * FROM beauty;


-- 创建男神表
CREATE TABLE boys(
  id INT,
  boyName VARCHAR(50),
  userCP INT DEFAULT NULL
)


SELECT * FROM boys;




-- 查询所有女明星对应的男朋友
SELECT name,boyName FROM beauty,boys;
-- 产生笛卡尔积   错误情况

SELECT * FROM beauty;   -- 12 行
SELECT * FROM boys;   --  4行
-- 12 * 4  = 48 行



-- 加入有效的连接条件
SELECT 
  `NAME`,
  boyName 
FROM
  beauty,
  boys 
WHERE
  beauty.boyfriend_id = boys.id;



/*
笛卡尔积：两个或多个表之间的连接操作
笛卡尔积的现象：表1有m行，表2有n行，那么结果是m*n行
笛卡尔积产生的条件：
  （1）省略连接条件
  （2）连接条件无效
  （3）所有表中的所有行互相连接
注意：为了避免笛卡尔积，可以在where条件加入有效的连接条件即可。

*/


/*
连接查询

概念：又称多表查询，当查询的字段来自多个表时，就会用到连接查询。
分类：
（1）按年代分类：
sql92标准：仅仅支持内连接
sql99标准（推荐）：支持内连接+外连接（左外、右外）+交叉连接
（2）按功能分类：
内连接：
  等值连接
  非等值连接
  自连接
外连接：
  左外连接
  右外连接
  全外连接
  交叉连接

*/

/*
sql92标准
-- 1、等值连接
# 多表等职连接的结果为多表的交集部分
# n表连接，至少需要n-1个连接条件
# 多表的顺序是没有要求的
# 一般需要为表起别名
# 可以搭配钱买你介绍的所有子句，比如排序、分组、筛选

*/
# eg：查询女神名和对应的男神名
SELECT
  `name`,
  boyName
FROM
  beauty,
  boys
WHERE
  beauty.boyfriend_id = boys.id;
  
  
# eg:查询员工名和对应的部门名

/*
分析：
      查询的表名： employees departments
      查询的字段： first_name department_name
      查询条件： employees.department_id = departments.department_id

*/
SELECT
  first_name,
  department_name
FROM
  employees,
  departments
WHERE
  employees.department_id = departments.department_id;


# (1)为表起别名
# eg：查询员工名、工种号、工种名
/*
(1)提高语句的简洁度
(2)区分多个重名字段
注意：如果为表起了别名，则查询的字段就不能使用原来的表名取限定。

*/
SELECT
  first_name,
  e.job_id,
  job_title
FROM
  employees AS e,
  jobs as j
WHERE
  e.job_id = j.job_id



# (2)两个表的顺序是否可以调换

SELECT
  e.first_name,
  e.job_id,
  j.job_title
FROM
  jobs as j,
  employees AS e
  
WHERE
  e.job_id = j.job_id



# (3)可以加筛选条件
# eg 查询有奖金率的员工名、部门名
SELECT  
  first_name,
  department_name,
  commission_pct
FROM
  employees e,
  departments d
WHERE
  e.department_id = d.department_id
  AND
  e.commission_pct IS NOT NULL;


# eg:查询城市名中第二个字符为o的部门和城市名
SELECT
  l.city,
  d.department_name
FROM
  locations l,
  departments d
WHERE
  l.location_id = d.location_id
  AND
  l.city LIKE '_o%';
  

# (4)可以加分组
# eg 查询每个城市的部门个数
SELECT
  city,
  COUNT(*) AS num
FROM
  departments d,
  locations l
WHERE
  d.location_id = l.location_id
GROUP BY
  city;


# eg:查询没有奖金率的每个部门的 部门名 和 部门的领导编号和 该部门的最低工资
SELECT
  d.department_name,
  e.manager_id,
  MIN(e.salary)
FROM
  departments d,
  employees e
WHERE
  d.department_id = e.department_id
  AND
  e.commission_pct IS NULL
GROUP BY
  d.department_name,
  e.manager_id

# (5)可以加排序
# eg 查询每个工种的工种名和员工的个数，并且按员工个数降序
SELECT
  j.job_title,
  COUNT(*) AS num
FROM
  employees e,
  jobs j
WHERE
  e.job_id = j.job_id
GROUP BY
  j.job_title
ORDER BY
  num DESC;




# (6) 可以实现三张表连接
# eg 查询员工名、部门名和所在的城市
SELECT
  e.first_name,
  d.department_name,
  l.city
FROM
  employees e,
  departments d,
  locations l
WHERE
  e.department_id = d.department_id
  AND
  d.location_id = l.location_id
  AND
  l.city LIKE '%s%'
ORDER BY
  d.department_name DESC


-- CREATE TABLE job_grades
-- (grade_level VARCHAR(3),
--  lowest_sal  int,
--  highest_sal int);
-- 

/*
非等值连接
表与表之间没有相等的字段
*/

-- # eg 查询员工的工资和工资级别
SELECT
  salary,
  grade_level 
FROM
  employees e,
  job_grades j 
WHERE
  salary BETWEEN j.lowest_sal 
  AND j.highest_sal
  AND
    j.grade_level = 'A'
ORDER BY
  salary DESC;



-- 自连接
# 同一张表查两次
# eg 查询员工名和上级领导的名
SELECT
  e.employee_id ,
  m.employee_id,
  e.first_name,
  m.first_name
FROM
  employees e,
  employees m
WHERE
  e.manager_id = m.manager_id



-- 1. 显示所有员工的名，部门号和部门名称。
-- 2. 查询 90 号部门员工的 job_id 和 90 号部门的 location_id
-- 3. 选择所有有奖金的员工的
-- last_name , department_name , location_id , city
-- 4. 选择city在Toronto工作的员工的
-- last_name , job_id , department_id , department_name 
-- 5.查询每个工种、每个部门的部门名、工种名和最低工资
-- 6.查询每个国家下的部门个数大于 2 的国家编号
SELECT
  country_id,
  COUNT(*) AS 部门个数
FROM
  departments d,
  locations l
WHERE
  d.location_id = l.location_id
GROUP BY
  country_id
HAVING
  部门个数 > 2;


-- 7、选择指定员工的姓名，员工号，以及他的管理者的姓名和员工号，结果类似于下面的格式
# employees Emp# manager Mgr#
# kochhar 101 K_ing 100

SELECT
  e.last_name AS employees,
  e.employee_id AS 'Emp#',
  
  m.last_name AS manager,
  m.employee_id AS 'Mgr#'
  
FROM
  employees e,   -- 员工   -- 经理
  employees m   -- 经理    -- 员工
WHERE 
  e.manager_id = m.employee_id
  AND
  e.last_name = 'kochhar'



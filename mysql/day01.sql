# 单行注释
-- 单行注释
/*
多行注释
*/


-- 创建员工数据库
CREATE DATABASE myemployees;


/*
DQL语言
*/

-- 基础查询
-- select * from tablename;   select 查询列表 from 表名；
-- select 标识选择哪些列
-- from 标识从哪个表中去选择

-- 特点：
  --  查询的列表可以是：表中的字段、常量值、表达式、函数
  -- 查询的结果是一个虚拟表格


-- 0、查询employees表的所有信息
SELECT * FROM myemployees.employees;

-- 1、查询employees表中的单个字段 first_name
SELECT
  first_name 
FROM
  myemployees.employees;

-- 2、查询employees表中的多个字段
SELECT
  employee_id,
  email,
  first_name,
  phone_number,
  job_id,
  salary
FROM
  employees;


-- 3、查询employees表中的所有字段
-- 方式一：
SELECT
  employee_id,
  first_name,
  last_name,
  email,
  phone_number,
  job_id,
  salary,
  commission_pct,
  manager_id,
  department_id,
  hiredate
FROM
  employees;

-- 方式二：
SELECT * FROM employees;


-- 4、查询常量值
SELECT "bigdata";

-- 5、查询表达式
SELECT 100 * 2;


-- 6、查询函数
SELECT VERSION()

-- 7、起别名
/*
1、便于理解
2、如果查询的字段有重名情况，使用别名是可以区分开来的
*/
-- 使用as （取别名）
SELECT 100 * 2 as "结果";

SELECT
  last_name AS 姓,
  first_name AS 名
FROM
  employees;

-- 使用空格（取别名）
SELECT
  last_name  姓,
  first_name  名
FROM
  employees;
  
  
-- 查询employees表的salary字段，显示结果为：“out put”
SELECT
  salary as "out put"
FROM
  employees;



-- 去重
# eg：查询员工中涉及到的所有部门id。
SELECT
  DISTINCT department_id
FROM 
  employees;



-- + 号的作用
/*
mysql中的 +号，只有一个功能：运算符！
注意：
  （1）两个操作数都为数值型，则做加法运算，如：select 1 + 2;
  （2）只要其中一方为字符型，试图将字符型数值转换成数值型：select '99' + 9;
  如果转换成功，则继续做加法运算；如果转换失败，则将字符型数值转换成0再做运算select 'A' + 'A'
  （3）只要有一方为null，则结果肯定为null。

*/

-- eg：查询员工名和姓，连成一个字段，并显示为姓名。
/*
分析： 查询的表employees
       查询的字段：first_name、last_name
       输出结果：姓名
*/
-- 错误，mysql中+号只有运算符的功能。
SELECT
  last_name + first_name as 姓名
FROM
  employees;
  
-- CONCAT()函数   做拼接

SELECT CONCAT('h','e','l','l','o') as 结果;

SELECT
  CONCAT(last_name,first_name) as 姓名
FROM
  employees;



-- 练习
-- 1、下面的语句是否可以执行成功
SELECT
  last_name,
  job_id,
  salary AS sal 
FROM
  employees;

-- 2、下面的语句是否可以执行成功 
select * from employees;


-- 3、找出下面语句中的错误

select employee_id , last_name,
salary * 12 AS "ANNUAL SALARY"
from employees;

-- 4、显示表 departments 的结构，并查询其中的全部数据
DESC departments;
SELECT * FROM departments;
-- 5、显示出表 employees 中的全部 job_id（不能重复）
SELECT DISTINCT job_id FROM employees;

-- 6、显示出表 employees 的first_name、last_name、job_id、commission_pct列，各个列之间用逗号连接，列头显示成 OUT_PUT

SELECT
  CONCAT(first_name,',',last_name,',',job_id,',',IFNULL(commission_pct,0)) AS 'OUT_PUT'
FROM
  employees;




/*

条件查询

SELECT * | {[DISTINCT] column | expression [alias],...}
FROM table
[WHERE condition(s)];

select 
查询列表（3）
from
表名 （1）
where
筛选条件 （2）；

筛选条件分类：
● 按条件表达式筛选
  ○ 简单条件运算符： >、<、=、!= (<>)、>=、<=
● 按逻辑表达式筛选
  ○ 逻辑运算符： &&（and）、|| （or）、!（not）
  ○ &&（and）：两个条件都为true，结果为true，反之为false
  ○ ||（or）：只要有一个条件为true，结果为true，反之为false
  ○ !（not）：如果连接的条件本身为false，结果为true，反之为false
● 模糊查询

  ○ like、between and、in、is null
  ○ like
    ■ 特点：一般和通配符搭配使用。
      ● 通配符：
        ○ % 任意多个字符，包含0个字符
        ○ _ 任意单个字符
        
  ○ between and    
    ■ 使用between and可以提高语句的简洁度
    ■ 包含临界值
    ■ 两个临界值不要调换顺序
    
  ○ in 判断某个字段的值是否属于in列表中的某一项
    ■ 使用in提高语句简洁度
    ■ in列表的值类型必须一致或兼容
    
    
  ○ is null
    ■ =或者<> 不能用于判断null值
    ■ is null 或 is not null 可以判断null值
*/

-- ----------------------------------------------------------------------------------------
-- 1、按条件表达式筛选
# 简单条件运算符： >、<、=、!= (<>)、>=、<=
# eg：查询工资大于12000 的员工信息
/*
分析： 查询表：employees
       查询的字段：所有字段
       查询条件： salary > 12000
*/
SELECT
  *
FROM
  employees

WHERE
  salary > 12000;
  
  
  
-- eg:查询部门编号不等于90号的员工名和部门编号。

/*
分析： 查询表：employees
       查询的字段：first_name department_id
       查询条件： department_id != 90
*/
SELECT
  first_name,
  department_id
FROM
  employees
WHERE
  department_id <> 90;    -- department_id != 90
-- -------------------------------------------------------------------------------------------------

-- -------------------------------------------------------------------------------------------------

-- 按逻辑表达式筛选
--   逻辑运算符： &&（and）、|| （or）、!（not）

# eg:查询工资在10000到20000之间的员工名、工资以及奖金。
/*
分析： 查询表：employees
       查询的字段：first_name salary commission_pct
       查询条件： salary >= 10000 and salary <=20000
*/

SELECT
  first_name,
  salary,
  commission_pct
FROM
  employees
WHERE
  salary >= 10000 and salary <=20000;




-- eg:查询部门编号不是在90到110之间，或者工资高于15000的员工信息。
/*
分析： 查询表：employees
       查询的字段：*
       查询条件： not (department_id > 90 and department_id < 110)  or salary > 15000
       (department_id < 90 or department_id > 110)

*/

SELECT
  *
FROM
  employees
WHERE
   (department_id < 90 or department_id > 110) or salary > 15000;

-- -------------------------------------------------------------------------------------------------


-- -------------------------------------------------------------------------------------------------
-- 模糊查询
-- like、between and、in、is null
# like
# eg:查询员工名中包含a的员工信息

/*
分析： 查询表：employees
       查询的字段：*
       查询条件： eg:'Diana'   first_name like '%a%'

*/


SELECT
  *
FROM
  employees
WHERE
  first_name like '%a%';
  


-- eg：查询员工名中第三个字符为e,第五个字符为a的员工名和工资
/*
分析： 查询表：employees
       查询的字段：first_name   salary
       查询条件： eg:'Diena'   first_name like '__e_a%'
*/


SELECT
  first_name,
  salary
FROM
  employees
WHERE
  first_name like '__e_a%';
  
  
-- eg:查询员工姓中第二个字符为_的员工名

/*
分析： 查询表：employees
       查询的字段：last_name  first_name
       查询条件：   last_name like '_\_%'     -- \_ 
*/

SELECT
  first_name,
  last_name
FROM
  employees
WHERE
  last_name like '_\_%';
  

-- eg:查询员工编号在100 到 120之间的员工信息。

/*
分析： 查询表：employees
       查询的字段：*
       查询条件：   employee_id >=100 and employee_id<=120  
                    employee_id between 100 and  120

*/
SELECT
  *
FROM
  employees
WHERE
  employee_id between 100 and  120;



# eg:查询员工的工种编号是IT_PROG、AD_VP、AD_PRES中的一个员工名和工种编号。

/*
分析： 查询表：employees
       查询的字段：first_name job_id
       查询条件：   job_id = 'IT_PROG' or job_id = 'AD_VP' or job_id = 'AD_PRES'
                    job_id in ('IT_PROG','AD_VP','AD_PRES')
*/


SELECT
  first_name,
  job_id
FROM
  employees
WHERE
  job_id in ('IT_PROG','AD_VP','AD_PRES');


-- eg: 查询没有奖金的员工名和奖金率

/*
分析： 查询表：employees
       查询的字段：first_name commission_pct
       查询条件：  commission_pct is null
*/
SELECT
  first_name,
  commission_pct
FROM
  employees
WHERE
   commission_pct IS NULL;    --  commission_pct is 0.40; 能否运行？   不可以运行
   
   
   
 -- 安全等于   <=>
 
 # eg: 查询没有奖金的员工名和奖金率

SELECT
  first_name,
  commission_pct
FROM
  employees
WHERE
   commission_pct  <=> null; 
   
   

# eg 查询工资为12000的员工信息
SELECT
  *
FROM
  employees
WHERE
  salary <=> 12000;

/*

is null vs <=>
is null 仅仅可以判断null值，可读性较高建议使用
<=> 既可以判断null值，又可以判断普通数值，可读性低
*/
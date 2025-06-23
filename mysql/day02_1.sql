/*
排序查询
select 查询列表 （3）
from  表名 （1）
[where 筛选条件] （2）
order by 排序列表 [asc | desc] （4）
特点：
1、asc代表的是升序，desc代表的是降序，如果不写，默认是升序。
2、order by 子句中可以支持单个字段、多个字段、表达式、函数、别名
3、order by 子句一般是放在查询语句的最后面，limit子句除外
*/
-- 
-- SELECT
--   *
-- FROM
--   employees;


# eg:查询员工信息，要求工资从高到底排序
/*
分析：
    查询的表：employees
    查询的字段：*
    查询条件：无
    排序条件： salary desc
*/
SELECT
  *
FROM
  employees
ORDER BY salary DESC;

SELECT
  *
FROM
  employees
ORDER BY salary ASC;




# eg：查询部门编号大于等于90的员工信息，按入职日期的先后进行排序（添加筛选条件）
/*
分析：
    查询的表：employees
    查询的字段：*
    查询条件：department_id >= 90
    排序条件： hiredate asc
*/
SELECT
  *
FROM
  employees
WHERE department_id >= 90
ORDER BY hiredate asc;



# eg:按年薪的高低显示员工的信息和年薪（按表达式排序）
/*
分析：
    查询的表：employees
    查询的字段：* 年薪       年薪 = salary * 12 *(1 + ifnull(commission_pct,0))
    查询条件：无
    排序条件： salary * 12 *(1 + ifnull(commission_pct,0)) desc
*/
SELECT
  *,
  salary * 12 *(1 + ifnull(commission_pct,0)) AS 年薪
FROM
  employees
ORDER BY salary * 12 *(1 + ifnull(commission_pct,0)) DESC;


SELECT
  *,
  salary * 12 *(1 + ifnull(commission_pct,0)) AS 年薪
FROM
  employees
ORDER BY 年薪 DESC;


# eg:按姓名的长度显示员工的姓名和工资（按函数排序）
/*
分析：
    查询的表：employees
    查询的字段：姓名的长度 length( concat(last_name,first_name)) as 姓名的长度 
                员工的姓名   concat(last_name,first_name) as 姓名
                工资salary
    查询条件：无
    排序条件： length( concat(last_name,first_name)) desc
*/
SELECT
  length( concat(last_name,first_name)) as "姓名的长度",
  concat(last_name,first_name) as "姓名",
  salary
FROM
  employees
ORDER BY length( concat(last_name,first_name)) desc;

# eg:查询员工信息，要求先按工资升序、再按员工编号降序（按多个字段进行排序）
/*
分析：
    查询的表：employees
    查询的字段：*
    查询条件：无
    排序条件： salary asc,employee_id desc
*/
SELECT
  *
FROM
  employees
ORDER BY salary asc,employee_id desc;


-- ---------------------------------------------------------------
/*
测试
*/

-- 1. 查询员工的姓名和部门号和年薪，按年薪降序 按姓名升序
/*
分析：
    查询的表名 ：employees
    查询的字段：  concat(last_name,first_name) as 姓名
                  department_id
                  salary * 12 *(1 + ifnull(commission_pct,0)) AS 年薪  
    查询的条件：无
    排序的条件：年薪 desc,姓名 asc
*/
SELECT
  concat(last_name,first_name) as 姓名,
  department_id,
  salary * 12 *(1 + ifnull(commission_pct,0)) AS 年薪
FROM
  employees
ORDER BY 年薪 desc,姓名 asc;



-- 2. 选择工资不在 8000 到 17000 的员工的姓名和工资，按工资降序
/*
分析：
    查询的表名 ：employees
    查询的字段：  concat(last_name,first_name) as 姓名
                  salary
    查询的条件：salary  not between 8000 and 17000
    排序的条件：salary desc
*/
SELECT
  concat(last_name,first_name) as 姓名,
  salary
FROM
  employees
WHERE salary  not between 8000 and 17000
ORDER BY salary desc;


-- 3. 查询邮箱中包含 e 的员工信息，并先按邮箱的字节数降序，再按部门号升序
/*
分析：
    查询的表名 ：employees
    查询的字段：  *,length(email)
    查询的条件：email like '%e%'
    排序的条件：length(email) desc,department_id asc
*/
SELECT
  *,
  length( email ) AS email_len 
FROM
  employees 
WHERE
  email LIKE '%e%' 
ORDER BY
  length( email ) DESC,
  department_id ASC;
















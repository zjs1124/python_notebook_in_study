/*
分组函数
功能：用作统计使用，又称为聚合函数或统计函数或组函数
分类：
（1）sum 求和
（2）avg 平均值
（3）max 最大值
（4）min 最小值
（5）count 计算个数
特点：
（1）sum、avg一般用于处理数值型，max、min、count可以处理任何类型
（2）以上分组函数都忽略null值
（3）可以和distinct搭配实现去重的运算
（4）一般使用count(*)做统计函数
（5）和分组函数一同查询的字段要求是group by后的字段

*/

/*
sum：函数用于计算数值列的总和
语法：SUM(expr)      参数expr ：要求和的列或者表达式
*/

SELECT 
  SUM(salary) AS sum_salary
FROM
  employees;
  
/*
avg:函数用于计算数值列的平均值
语法：AVG([DISTINCT] expr)   参数expr：要求平均值的列或表达式   [DISTINCT]：去重
*/
SELECT
  AVG(salary) AS avg_salary
FROM
  employees;

/*
max:函数用于计算数值列的最大值。
语法：MAX(expr)   参数expr：要找最大值的列或表达式
*/

SELECT
  MAX(salary)
FROM
  employees;



/*
min:函数用于计算数值列的最小值
语法：MIN(expr)   参数expr：要找最小值的列或表达式

*/

SELECT
  MIN(salary)
FROM
  employees;


/*
count:函数用于计算行数或者满足指定条件的行数
语法：COUNT(DISTINCT expr,[expr...])   DISTINCT expr  去重后的要计算的列或表达式
*/

SELECT
  COUNT(salary)
FROM 
  employees;

-- eg:查询所有员工的工资总和、平均值、最高值、最低值以及总个数
SELECT
  SUM(salary) AS 工资总和,
  AVG(salary) AS avg_salary,
  MAX(salary) AS max_salary,
  MIN(salary) AS min_salary,
  COUNT(*) AS 总个数
FROM
  employees;


-- SELECT
--   *
-- FROM
--   employees;


-- 统计函数
# 注意：sum/avg 计算非数值类型的列返回的结果是0
SELECT SUM(last_name) FROM employees;
SELECT AVG(last_name) FROM employees;
SELECT MAX(last_name) FROM employees;
SELECT MIN(last_name) FROM employees;
SELECT COUNT(last_name) FROM employees;
SELECT COUNT(salary) FROM employees;

#注意： count 不会计算null行
SELECT  COUNT(commission_pct) FROM employees;


-- 可以和distinct搭配实现去重的运算
SELECT
  SUM(DISTINCT salary),
  SUM(salary)
FROM
  employees;


SELECT
  COUNT(DISTINCT salary),
  COUNT(salary)
FROM
  employees;
  
  
  
-- count 详细说明
SELECT COUNT(salary) FROM employees;
SELECT COUNT(*) FROM employees;
SELECT COUNT(2) FROM employees;

/*
测试
*/

-- 1. 查询公司员工工资的最大值，最小值，平均值，总和
-- 2. 查询员工表中的最大入职时间和最小入职时间的相差天数 （DATEDIFF）

-- DIFFERENCE   被弃用，mysql8弃用，现在用 DATEDIFF
SELECT
  DATEDIFF(MAX(hiredate),MIN(hiredate)) AS diff_day
FROM
  employees;


-- 3. 查询部门编号为 90 的员工个数

SELECT 
  COUNT(*) AS num_dept
FROM
  employees
WHERE
  department_id = 90;

-- eg：查询每个部门的平均工资
/*
分组查询
语法：
SELECT column, group_function(column)      4
FROM table                                 1
[WHERE condition]                          2
[GROUP BY group_by_expression]             3       
[ORDER BY column];                         5

select 分组函数，列（要求出现在group by的后面）
from 表名
[where 筛选条件]
group by 分组的列表
[order by 子句]
特点：
1、分组查询中的筛选条件分为两类
数据源                    位置				关键字
     分组前筛选	    	  原始表		   group by子句的前面		    where
     分组后筛选	        分组后的结果集	   group by子句的后面		    having
   （1）分组函数做条件肯定是放在having子句中
    (2) 能用分组前筛选的，就优先考虑使用分组前筛选
2、group by 子句支持单个字段分组，多个字段分组（多个字段之间用逗号隔开没有顺序要求），
表达式或函数（用的较少）
3、也可以添加排序（排序放在整个分组查询的最后）

*/


-- eg:查询邮箱中包含a字符，每个部门的平均工资。
/*
分析：
    查询表名：employees
    查询字段: salary department_id
    查询的条件： email like '%a%'
    分组条件：department_id
*/

SELECT
  AVG(salary) AS avg_salary,
  department_id
FROM
  employees
WHERE
  email like '%a%'
GROUP BY
  department_id;


SELECT
  AVG(salary) AS avg_salary,
  department_id
FROM
  employees
-- WHERE
--   email like '%a%'
GROUP BY
  department_id;


-- eg:查询有奖金的每个领导手下员工的最高工资。
/*

分析：
    查询表名：employees
    查询字段: max(salary)  manager_id
    查询的条件： commission_pct is not null
    分组条件：manager_id

*/
SELECT
  max(salary) AS max_salary,
  manager_id
FROM
  employees
WHERE
  commission_pct is not null
GROUP BY
  manager_id;

-- 添加复杂的筛选条件
# eg： 查询哪个部门的员工个数大于2
/*
分析：
  （1）查询每个部门的员工个数
  
  
  （2）根据（1）结果进行筛选，查询哪个部门的员工个数大于2
  
*/

-- （1）查询每个部门的员工个数
SELECT
  COUNT(*),
  department_id
FROM
  employees
GROUP BY
  department_id;

-- （2）根据（1）结果进行筛选，查询哪个部门的员工个数大于2

SELECT
  COUNT(*),
  department_id
FROM
  employees
GROUP BY
  department_id
HAVING   -- 分组后筛选   
   COUNT(*) > 2;


-- eg: 查询每个工种有奖金的员工的最高工资大于12000的工种编号和最高工资。
/*
分析：
  （1）查询每个工种有奖金的员工的最高工资
  
  
  （2）对（1）的结果进行筛选，最高工资大于12000

*/
#  （1）查询每个工种有奖金的员工的最高工资
SELECT
  MAX(salary),
  job_id
FROM
  employees
WHERE
  commission_pct IS NOT NULL
GROUP BY
  job_id

# （2）对（1）的结果进行筛选，最高工资大于12000

SELECT
  MAX(salary),
  job_id
FROM
  employees
WHERE
  commission_pct IS NOT NULL
GROUP BY
  job_id
HAVING
   MAX(salary) > 12000;


-- eg: 查询领导编号大于102的每个领导手下的最低工资大于5000的领导编号是哪个以及其最低工资。

/*
分析：
  （1）查询每个领导手下的员工固定最低工资
  
  
  （2） 根据（1）的结果添加筛选条件 编号大于102
  
  
  （3）根据（2）的结果 添加筛选条件 最低工资大于5000
*/

# （1）查询每个领导手下的员工固定最低工资
SELECT
  MIN(salary) AS min_salary,
  manager_id
FROM
  employees
GROUP BY
  manager_id

# （2） 根据（1）的结果添加筛选条件 编号大于102
SELECT
  MIN(salary) AS min_salary,
  manager_id
FROM
  employees
WHERE
  manager_id > 102
GROUP BY
  manager_id


#  （3）根据（2）的结果 添加筛选条件 最低工资大于5000
SELECT                 
  MIN(salary) AS min_salary,
  manager_id
FROM                   
  employees                    
WHERE                  
  manager_id > 102
GROUP BY               
  manager_id
HAVING                 
  min_salary > 5000;  
   
/*
细分：
第一步： FROM
第二步： WHERE
第三步:  GROUP BY
第四步： MIN(salary) AS min_salary
第五步： HAVING
第六步： SELECT

*/   


SELECT                
  MIN(salary) AS min_salary,
  manager_id
FROM                   
  employees                    
WHERE                  
  manager_id > 102
GROUP BY               
  manager_id
HAVING                 
  min_salary > 5000;  
   



-- 按表达式或者函数分组

-- eg：按员工姓名的长度分组，查询每一组的员工个数，筛选员工个数大于5的有哪些。

# （1）查询每个长度的员工个数
SELECT
  COUNT(*) AS num,
  LENGTH(CONCAT(last_name,first_name)) AS len_name
FROM
  employees
GROUP BY
   LENGTH(CONCAT(last_name,first_name))



# （2）添加筛选条件
SELECT
  COUNT(*) AS num,
  LENGTH(CONCAT(last_name,first_name)) AS len_name
FROM
  employees
GROUP BY
  LENGTH(CONCAT(last_name,first_name))
HAVING
  num > 5;


-- 按多个字段分组
# eg：查询每个部门每个工种的员工的平均工资。

SELECT
  AVG(salary ) AS avg_salary,
  department_id,
  job_id
FROM
  employees
WHERE
  department_id IS NOT NULL
GROUP BY
  job_id,
  department_id
HAVING
  avg_salary > 10000
ORDER BY
  avg_salary DESC;



-- 1. 查询各 job_id 的员工工资的最大值，最小值，平均值，总和，并按 job_id 升序
SELECT
  job_id,
  MAX(salary) as max_salary,
  MIN(salary) as min_salary,
  AVG(salary) as avg_salary,
  SUM(salary) as sum_salary
FROM
  employees
GROUP BY
  job_id
ORDER BY
  job_id ASC;



-- 2. 查询员工最高工资和最低工资的差距
SELECT
  MAX(salary) - MIN(salary) AS '工资的差距'
FROM
  employees;


-- 3. 查询各个管理者手下员工的最低工资，其中最低工资不能低于 6000，没有管理者的员工不计算在内
SELECT
  manager_id,
  MIN(salary) AS '最低工资'
FROM
  employees
WHERE
  manager_id IS NOT NULL
GROUP BY
  manager_id
HAVING
  MIN(salary) >= 6000;


-- 4. 查询所有部门的编号，员工数量和工资平均值,并按平均工资降序
SELECT
  department_id AS '部门编号',
  COUNT(*) AS '员工数量',
  AVG(salary) AS '平均工资'
FROM
  employees
GROUP BY
  department_id  -- 不建议使用别名
ORDER BY
  AVG(salary)  DESC;



-- 5. 选择具有各个 job_id 的员工人数
SELECT
  job_id,
  COUNT(*)
FROM
  employees
GROUP BY
  job_id;











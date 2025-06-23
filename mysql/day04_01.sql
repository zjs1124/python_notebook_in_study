-- sql99标准
/*
语法：
  select 查询列表
  from 表1 别名 [连接类型]
  join 表2 别名
  on 连接条件
  [where 筛选条件]
  [group by 分组]
  [having 筛选条件]
  [order by 排序列表]

分类：
  内连接 * inner
  外连接
    左外 * left[outer]
    右外 * right[outer]
    全外 full[outer]
  交叉连接 cross

*/

-- 内连接 * inner
/*
语法：
  select 查询列表
  from 表1 别名
  inner join 表2 别名
  on 连接条件；
分类：
等值连接
非等值连接
自连接

特点：
（1）添加排序、分组、筛选
（2）inner 可以省略
（3）筛选条件放在where后面，连接条件放在on后面，提高分离性，便于阅读
（4）inner join连接和sql92语法中的等值连接效果是一样的，都是查询多表的交集
*/
-- ----------------------------内连接----------------------------------------
-- 等值连接
# eg: 查询员工名、部门名
SELECT
  first_name,
  department_name 
FROM
  employees AS e
  INNER JOIN departments AS d -- INNER可省略
  ON e.department_id = d.department_id


# eg:查询名字中包含e的员工名和工种名
SELECT
  first_name,
  job_title
FROM
  employees e 
  INNER JOIN jobs j 
  ON e.job_id = j.job_id
WHERE
  e.first_name LIKE "%e%";

# eg:查询部门个数大于3的城市名和部门个数（添加分组+筛选）
# （1）查询每个城市的部门个数
SELECT
  city,
  COUNT(*) AS 部门个数
FROM
  departments d 
  INNER JOIN locations l 
  ON d.location_id = l.location_id
GROUP BY
  city


# （2）在（1）结果上筛选出满足的条件

SELECT
  city,
  COUNT(*) AS 部门个数
FROM
  departments d 
  INNER JOIN locations l 
  ON d.location_id = l.location_id
GROUP BY
  city
HAVING
  COUNT(*) > 3;


# eg 查询哪个部门的员工个数大于3的部门名和员工个数，并按个数降序（添加排序）
SELECT
  count(*) AS 员工个数,
  department_name
FROM
  employees e 
  INNER JOIN departments d 
  ON e.department_id = d.department_id
GROUP BY
  department_name
HAVING
   count(*)  > 3
ORDER BY
 count(*) DESC







# eg 查询员工名、部门名、工种名，并按部门名降序
SELECT
  first_name,
  department_name,
  job_title
FROM
  employees e 
  INNER JOIN departments d 
  ON e.department_id = d.department_id
  INNER JOIN jobs j 
  ON e.job_id = j.job_id
ORDER BY
  department_name DESC;
  
  
  
-- 非等值连接
# eg 查询员工的工资级别
SELECT
  salary,
  grade_level
FROM
  employees e 
  INNER JOIN job_grades g 
  ON e.salary BETWEEN g.lowest_sal AND g.highest_sal ;
  
# eg 查询工资级别的个数大于20 的个数，并且按工资级别降序
SELECT
  COUNT(*) AS 个数,
  g.grade_level
FROM
  employees e 
  INNER JOIN job_grades g 
  ON e.salary BETWEEN g.lowest_sal AND g.highest_sal 
GROUP BY
  g.grade_level
HAVING
  COUNT(*) > 20
ORDER BY
  g.grade_level DESC


-- 自连接
# 查询员工的名字、上级的名字
SELECT
  e.first_name,
  m.first_name
FROM
  employees e 
  INNER JOIN employees m 
  ON e.manager_id = m.employee_id


# 查询名中包含字符e的员工的名字、上级的名字

SELECT
  e.first_name,
  m.first_name
FROM
  employees e 
  INNER JOIN employees m 
  ON e.manager_id = m.employee_id
WHERE
  e.first_name LIKE '%e%'
  
-- ----------------------------------外连接-------------------------------------------
/*
应用场景：用于查询一个表中有，另一个表中没有的记录。
特点：
  （1）外连接的查询结果为主表中的所有记录，如果从表中有和它匹配的，则显示匹配的值，如果
  从表中没有和它匹配的，则显示null。
  外连接查询结果 = 内连接结果 + 主表中有而从表中没有的记录
  （2）左外连接，left join左边的是主表；右外连接，right join右边的是主表
  （3）左外和右外交换两个表的顺序，可以实现同样的效果
  （4）全外连接 = 内连接的结果 + 表1中有但表2中没有的+表2中有但表1中没有的
*/

# eg 查询哪个部门没有员工
-- 左外   -- 左边的表为主表
SELECT
  *
FROM
  departments d 
  LEFT JOIN employees e 
  ON d.department_id = e.department_id
WHERE
  employee_id IS NULL

-- 右外   -- 右边表为主表
SELECT
  *
FROM
  employees e 
  RIGHT JOIN departments d 
  ON d.department_id = e.department_id
WHERE
  e.employee_id IS NULL;


-- 全外连接
-- FULL JOIN
-- 注意：mysql中没有提供full jion操作符来进行全表连接查询，无法直接使用。
-- union联合查询解决
-- 错误示范
-- SELECT
--   *
-- FROM
--   departments d 
--   FULL JOIN employees e 
--   ON d.department_id = e.department_id


-- --------------------------------交叉连接----------------------------------------
/*
交叉连接，就是笛卡尔积。
表1有m个字段，表2有n个字段   结果：m * n
*/
-- cross join
SELECT
  *
FROM
  employees e 
  CROSS JOIN departments d 
--   ON d.department_id = e.department_id




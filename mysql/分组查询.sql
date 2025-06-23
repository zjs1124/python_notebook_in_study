/*
笛卡尔积: 两个或多个表之间的连接操作
笛卡尔积的现象: 表1有m行,表2有n行，那么结果是m*n行
笛卡尔积产生的条件:
(1) 省略连接条件
(2) 连接条件无效
(3) 所有表中的所有行互相连接
注意: 为了避免笛卡尔积,可以在where条件加入有效的连接条件即可
*/

/*
连接查询

概念: 又称多表查询，当查询的字段来自多个表时,就会用到连接查询。
分类:
(1) 按年代分类:
sql92标准: 仅仅支持内连接
sql99标准(推荐): 支持内连接和外连接(左外、右外) + 交叉连接
(2) 按功能分类:
内连接:
等值连接
非等值连接
自连接
外连接:
左外连接
右外连接
全外连接
交叉连接

*/

/*
sql92标准
-- 1、等值连接
# 多表等值连接的结果为多表的交集部分
# n表连接,至少需要n-1个连接条件
# 多表的顺序是没有要求的
# 一般需要为表起别名
# 可以搭配前面介绍的所有子句，比如排序、分组、筛选
*/

# 三表连接
# eg 查询员工名、部门名和所在的城市

select
    e.first_name,
    d.department_name,
    l.city
from
    employees e,
    departments d,
    locations l
where
    e.department_id = d.department_id
    and
    d.location_id = l.location_id
    and
    l.city like '%s%'
order by
    d.department_name desc;

/*
非等值连接
表与表之间没有相等的字段
*/

-- eg 查询员工的工资和工资级别

select salary, grade_level
from employees e, job_grades j
where
    salary between j.lowest_sal and j.highest_sal
    and j.grade_level = 'A'
order by salary desc;

-- 自连接
# 同一张表查两次
# eg 查询员工名和上级领导的名

select
    e.employee_id as employee_id,
    e.last_name as employee_name,
    m.employee_id as manager_id,
    m.last_name as manager_name
from
    employees e,
    employees m
where
    e.manager_id = m.employee_id
order by
    manager_id;

--  -----------
show tables;
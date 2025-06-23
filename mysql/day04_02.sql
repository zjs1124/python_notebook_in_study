/*
子查询
含义：出现在其他语句中的select语句，称为子查询或内查询；外部的查询语句，称为主查询或外查询
分类：
  按子查询出现的位置：
    select后面
        仅仅支持标量子查询
    where或having后面
        标量子查询 （单行）
        列子查询 （多行）
        行子查询
    exists后面（相关子查询）
         表子查询
按结果集的行列数不同：
      标量子查询（结果集只有一行一列）
      列子查询（结果集只有一列多行）
      行子查询（结果集有一行多列）
      表子查询（结果集一般为多行多列）
*/
-- --------------------------按子查询出现的位置---------------------------------------------
-- where或having后面
/*
1、标量子查询（单行子查询）
2、列子查询（多行子查询）
3、行子查询（一行多列）
特点：
（1）子查询放在小括号内
（2）子查询一般放在条件的右侧
（3）标量子查询，一般搭配着单行操作符使用：> < >= <= <>
（4）列子查询，一般搭配着多行操作符使用： in any/some all
（5）子查询的执行优先于主查询执行，主查询的条件用到了子查询的结果
*/

-- 标量子查询（单行子查询）
# eg 谁的工资比Abel高
-- （1）查询Abel工资
SELECT
  salary
FROM
  employees
WHERE
  last_name = 'Abel'
-- (2)查询员工的信息，满足salary大于（1）的结果
SELECT
  * 
FROM
  employees 
WHERE
  salary > ( SELECT salary FROM employees WHERE last_name = 'Abel' )



# eg: 返回job_id与141号员工相同，salary比143号员工多的员工名、job_id和工资
-- (1)查询141号员工的job_id
SELECT
  job_id
FROM
  employees
WHERE
  employee_id = 141

-- (2)查询143号员工的工资
SELECT
  salary
FROM
  employees
WHERE
  employee_id = 143

-- (2)查询员工的名、job_id和工资，要求job_id=(1)并且salary > (2)
SELECT
  first_name,
  job_id,
  salary 
FROM
  employees 
WHERE
  job_id = ( SELECT job_id FROM employees WHERE employee_id = 141 ) 
  AND salary > ( SELECT salary FROM employees WHERE employee_id = 143 )

# eg 返回公司工资最少的员工的last_name,job_id和salary
-- (1)查询公司最低工资
SELECT
  MIN(salary)
FROM
  employees

-- (2)查询last_name,job_id和salary，要求salary = (1)
SELECT
  last_name,
  job_id,
  salary 
FROM
  employees 
WHERE
  salary = ( SELECT MIN( salary ) FROM employees )

#  eg 查询最低工资大于50号部门最低工资低的部门id和其最低工资
-- (1)查询50号部门最低工资
SELECT
  MIN(salary)
FROM
  employees
WHERE
  department_id = 50

-- (2)查询每个部门最低工资
SELECT
  MIN(salary),
  department_id
FROM
  employees
GROUP BY
  department_id

-- (3)在(2)基础上筛选，满足 min(salary) > (1)

SELECT
  MIN( salary ),
  department_id 
FROM
  employees 
GROUP BY
  department_id 
HAVING
  MIN( salary ) > ( SELECT MIN( salary ) FROM employees WHERE department_id = 50 )

# 非法使用标量子查询
-- SELECT
-- 	min( salary ),
-- 	department_id 
-- FROM
-- 	employees 
-- GROUP BY
-- 	department_id 
-- HAVING
-- 	MIN( salary ) > ( SELECT salary  FROM employees WHERE department_id = 50 );

-- 列子查询
/*
IN/NOT IN 等于列表中的任意一个
ANY|SOME 和子查询返回的某一个值比较
ALL 和子查询返回的所有值比较
*/
# eg 返回location_id是1400或1700的部门中的所有员工名

-- (1)查询location_id是1400或1700的部门编号
SELECT
   department_id
FROM
  departments
WHERE
  location_id IN (1400,1700)


-- (2)查询员工名，要求部门号是（1）结果中的某一个
SELECT
  first_name 
FROM
  employees 
WHERE
  department_id IN ( SELECT department_id FROM departments WHERE location_id IN ( 1400, 1700 ) )
  
  

# eg 返回其它工种中比 job_id为‘IT_PROG’工种任一工资 低的员工的工号、名、job_id以及salary
-- (1)查询job_id为‘IT_PROG’工种任一工资
SELECT
  salary
FROM
  employees
WHERE
  job_id = 'IT_PROG'

-- (2)查询员工的工号、名、job_id以及salary，要求 salary < (1)结果中的任意一个

SELECT
  employee_id,
  first_name,
  job_id,
  salary 
FROM
  employees 
WHERE
  salary < ANY ( SELECT salary FROM employees WHERE job_id = 'IT_PROG' ) AND  job_id <> 'IT_PROG'



SELECT
  employee_id,
  first_name,
  job_id,
  salary 
FROM
  employees 
WHERE
  salary <  ( SELECT MAX(salary) FROM employees WHERE job_id = 'IT_PROG' ) AND  job_id <> 'IT_PROG'


-- 行子查询（一行多列）

# eg 查询员工编号最小并且工资最高的员工信息
-- (1)查询最小的员工编号
SELECT
  MIN(employee_id)
FROM
  employees

-- (2) 查询最高工资
SELECT
  MAX(salary)
FROM
  employees
  

-- (3)查询员工信息
SELECT
  * 
FROM
  employees 
WHERE
  employee_id = ( SELECT MIN( employee_id ) FROM employees ) 
  AND salary = ( SELECT MAX( salary ) FROM employees )


-- select 后面
/*
仅仅支持标量子查询
*/

# eg :查询每个部门的员工个数
-- SELECT
--   COUNT(*),
--   department_id
-- FROM
--   employees
-- GROUP BY
--   department_id
-- 



SELECT
  d.*,
  ( SELECT count( * ) FROM employees e WHERE e.department_id = d.department_id ) 个数 
FROM
  departments d;

# eg 查询员工号等于102的部门名
SELECT
  (SELECT
    department_name
  FROM
    departments d 
  INNER JOIN employees e 
  ON d.department_id = e.department_id
  WHERE
    e.employee_id = 102) AS 部门名;


-- from 后面
/*
将子查询结果充当一张表，要求必须起别名
*/
# eg 查询每个部门的平均工资的工资等级
-- (1)查询每个部门的平均工资
SELECT
  AVG(salary),
  department_id
FROM
  employees
GROUP BY
  department_id



-- (2)连接(1)的结果集和job_grades表 筛选条件平均工资 
SELECT
  a.*,
  g.grade_level 
FROM
  ( SELECT AVG( salary ) AS ag, department_id FROM employees GROUP BY department_id ) AS a 
  INNER JOIN job_grades g 
  ON a.ag BETWEEN g.lowest_sal AND g.highest_sal




-- exists后面（相关子查询）
/*
语法：
exists（完整的查询语句）
结果：1或0
*/
SELECT EXISTS(SELECT employee_id FROM employees WHERE salary = 10000);
SELECT EXISTS(SELECT employee_id FROM employees WHERE salary = 30000);



/*
分页查询
应用场景：当要显示的数据，一页显示不全，需要分页提交sql请求
语法：
  select 查询列表 （7）
  from 表名 （1）
  [
    join type join 表2 （2）
    on 连接条件。（3）
    where 筛选条件 （4）
    group by 分组字段 （5）
    having 分组后的筛选 （6）
    order by 排序的字段 （8）
  ]
  limit [offset] ,size; （9）
  其中：
  offset 要显示条目的起始索引（起始索引从0开始）
  size 要显示的条目个数
*/


/*
特点：
  （1）limit语句放在查询语句的最后
  （2）公式
    要显示的页数（page），每页的条目数（size）
    select 查询列表
    from 表名
    limit (page - 1) * size,size;
    size = 10
    page    
      1			0
      2			10
      3			20
*/


# eg 查询前五条员工的信息
SELECT
  *
FROM 
  employees
LIMIT 0 , 5;


# eg 查询第11条到第25条员工的信息
SELECT
  *
FROM 
  employees
LIMIT 10 , 15;

# eg 有奖金率的员工信息，并且工资较高的前10名显示出来
SELECT
  *
FROM
  employees
WHERE
  commission_pct IS NOT NULL
ORDER BY
  salary DESC
LIMIT 10;



/*
union联合查询
union联合（合并）：将多条查询语句的结果合并成一个结果
语法：
查询语句1
union
查询语句2
union
...
应用场景：要查询的结果来自于多个表，且多个表没有直接的连接关系，但查询的信息一致时。
特点：
1、要求多条查询语句的查询列数是一致的。
2、要求多条查询语句的查询的每一列的类型和顺序最好一致。
3、union关键字默认去重，如果使用union all可以包含重复项。
*/

# eg 查询部门编号大于90或邮箱包含a的员工信息
SELECT
  *
FROM
  employees
WHERE
  email LIKE '%a%'
  OR
  department_id > 90



SELECT * FROM employees WHERE email LIKE '%a%' 
UNION
SELECT * FROM employees WHERE department_id > 90







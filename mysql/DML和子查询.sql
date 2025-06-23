-- 列子查询
/*
in/not in 等于列表中的任意一个
any/some 和子查询返回的某一个值进行比较
all 和子查询返回的左右值进行比较
*/

# eg 返回location_id是1400或1700的部门中的所有员工名

-- (1) 查询location_id是1400或者1700中的部门编号
select department_id, location_id
from departments
where
    location_id in (1400, 1700)

-- (2)查询员工名,要求部门号是(1)结果中的某一个

select first_name
from employees
where
    department_id in (
        select department_id
        from departments
        where
            location_id in (1400, 1700)
    )

# eg 返回其他工种中比job_id 为'IT_ PROG'工种任一工资低的员工的工号、名、job_id以及salary
-- (1)查询job_id为'IT_PROG'工种任一工资

select salary from employees where job_id = 'IT_PROG'

-- (2)查询员工的工号、名、job_id以及salary,要求salary < (1)结果中的任意一个

select
    employee_id,
    first_name,
    job_id,
    salary
from employees
where
    salary < any (
        SELECT salary
        FROM employees
        WHERE
            job_id = 'IT_PROG'
    )
    and job_id <> 'IT_prog'

select
    employee_id,
    first_name,
    job_id,
    salary
from employees
where
    salary < (
        select max(salary)
        from employees
        where
            job_id = 'IT_PROG'
    )
    and job_id <> 'IT_PROG'

-- SELECT 后面
/*
仅仅支持标量子查询
*/

# eg:查询每个部门的员工个数

select 
    d.*,
    (select count(*) from employees e where e.department_id = d.department_id) 个数
from
    departments d;

# eg 查询员工号等于102的部门名
select
(select
    department_name
from
    departments d
    inner join 
    employees e
    on
    d.department_id = e.department_id
where
    e.employee_id = 102) as 部门名;

-- from 后面
/*
将子查询结果充当一张表,要求必须起别名
*/

# eg 查询每个部门的平均工资的工资等级
-- (1) 查询每个部门的平均工资

select avg(salary), department_id
from employees
group by
    department_id

-- (2)链接(1)的结果集和job_grades 表 筛选条件平均工资
select a.*, g.grade_level
from (
        SELECT AVG(salary) AS ag, department_id
        FROM employees
        GROUP BY
            department_id
    ) as a
    inner join job_grades g on a.ag between g.lowest_sal and g.highest_sal

-- exists后面(相关子查询)
/*
语法:
exists(完整的查询语句)
结果 1或0
*/
select exists (
        select employee_id
        from employees
        where
            salary = 10000
    );

SELECT EXISTS (
        SELECT employee_id
        FROM employees
        WHERE
            salary = 30000
    );

/*
分页查询
应用场景:当要显示的数据一页显示不全,需要分页提交sql请求
语法:
select 查询列表
from 表名
[
join type join 表2
on 链接条件
where 筛选条件
group by 分组字段
having 分组后的筛选
order by 筛选字段
]
limit [offset] ,size;
其中:
offset 要显示条目的起始索引(起始索引从0开始)
size 要显示的条目个数
*/

/*
特点:
(1) limit语句放在查询语句的最后
(2) 公式
要显示的页数(page),每页的条目数(size)
select 查询列表
from 表名
limit (page - 1) * size,size;
size = 10
page
1        0
2        10
3        20

*/

# eg 查询前五条员工的信息
select
    *
from
    employees
limit
    0, 5;

# eg 查询第11条道第25条员工的信息

select 
    *
FROM
    employees
limit
    10, 15;

# eg 有奖金率的员工信息,并且工资较高的前10名显示出来

select 
    *
from
    employees
where
    commission_pct is not null
order by
    salary desc
limit 10;

/*
union 联合查询
union 联合(合并):将多条查询语句的结果合并成一个结果
语法:
查询语句1
union
查询语句2
union
...
应用场景: 要查询的结果来自于多个表,且多个表没有直接的链接关系,但查询的信息一致时。
特点:
1. 要求多条查询语句的查询列数是一致的
2. 要求多条查询语句的查询的每一列的类型和顺序最好一致
3. union关键字默认去重,如果使用union all 可以包含重复项。
*/

# eg 查询部门编号大于90或邮箱包含a的员工信息

select 
    *
from
    employees
where
    email like '%a%'
    or
    department_id > 90

select *
from employees
where
    email like '%a%'
union
select *
from employees
where
    department_id > 90

/*
DML语言
插入: insert
修改: update
删除: delete

1.插入语句
方式一:经典的插入语句
语法:
insert into 表名(列名,...) values(值1,...);

方式二:
语法:
insert into 表名
set 列名=值,列名=值,....

方式一和方式二对比:
(1) 方式一支持插入多行,方式二不支持
(2) 方式一支持子查询,方式二不支持

2、修改语句
(1) 修改单表的记录
语法:
update 表名
set 列=新值，列=新值,.....
where 筛选条件
(2) 修改多表的记录
sql92语法:
update 表1 别名，表2 别名 set 列=值,...... where 连接条件 and 筛选条件；

sql99 语法:
update 表1 别名
inner |left|right join 表2 别名
on 链接条件
set 列=值
where 筛选条件;

3、删除语句
方式一:delete

(1) 单表删除(*)
语法:
delete from 表名 where 筛选条件；
（2） 多表删除 (补充)
sql92语法： delete 表1的别名，表2的别名 from 表1 别名，表2 别名 where 连接条件 and 筛选条件；

sql99 语法:
delete 表1的别名,表2的别名
from 表1 别名
Inner |left|right join 表2 别名 on 链接条件
where 筛选条件;

方式二： truncate
语法:
truncate table 表名;

delete 和 truncate对比:
(1) delete可以加where条件,truncate不能加
(2) truncate删除,效率高一点
(3) 加入要删除的表中有自增长列,如果用delete删除后,再插入数据,自增长列的值从断点开始
而truncate删除后,再插入数据自增长列的值从1开始
(4)truncate 删除后没有返回值,delete删除后有返回值
(5) truncate 删除后不能回滚,delete删除后可以回滚


*/

# 插入语句
# 插入的值类型要与列的类型一致或者兼容

insert into beauty(id,`name`,sex,boyfriend_id,borndate,phone,photo)
values(1,'章子怡','女',1,'1979-02-09','13888888888',null)

# 不可以为null的列必须插入值,可以为null的列如何插入值?

insert into beauty(id,`name`,sex,boyfriend_id,phone)
values(2,'唐艺昕','女',1,'15288888888')

# 列的顺序是可以调换的
insert into beauty (`name`,sex,phone,id)
values('毛晓彤','女','19888888888',3)

# 列数和值的个数必须一致,不然报错

# 可以省列名、默认所有列,而且列的顺序和表中列的顺序一致

insert into beauty (id,`name`,sex,boyfriend_id,borndate,phone,photo)
values(4,'关晓彤','女',2,null,'19888888888',null)

insert into beauty values ( 6, '张静怡', '女', 3, null, '1528888888', null )

-- ------------------方式二--------------------------

insert into beauty set id = 5, `name` = '金晨', phone = '15277777777';

-- 方式一和方式二对比
# 1、方式一支持插入多行,方式二不支持
insert into beauty
values (7,'章子怡1','女',1,'1979-02-09','13888888888',null),
(8,'章子怡2','女',1,'1979-02-09','13888888888',null),
( 9, '章子怡2', '女', 1, '1979-02-09', '13888888888', null )

# 方式一支持子查询,方式二不支持

insert into beauty(id,name,phone)
select 22,'辛梓蕾','17888888888';

-- -----------------------修改------------------------
-- 修改单表的记录
# eg 修改beauty表中姓章的女神电话为:19988888881

update beauty
set phone = '19988888881'
where
    `name` like '章%'

# 修改没有男朋友的女神的男朋友编号都为3

update beauty
set boyfriend_id = 3
where
    boyfriend_id is null

-- ----------------------删除-------------------------------
-- 方式一 delete
# 单表删除
# eg 删除手机号以19开头的女神信息

delete from beauty where phone like '19%'

-- 方式二 truncate
# eg 清空beauty表
truncate table beauty
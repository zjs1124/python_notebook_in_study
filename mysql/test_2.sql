-- Active: 1750085304813@@master@10000@ex
-- 单表查询
-- 1
select ename, hiredate
from ex.emp
where
    month(date_add(hiredate, 4)) = month(hiredate) + 1;

-- 2
select ename, hiredate
from ex.emp
where
    year(hiredate) < year(current_date) - 12;

-- 3
select ename
from ex.emp
where
    substring(ename, 1) regexp '[A-Z]';

-- 5
select ename from ex.emp where ename not regexp '[R|A]';

-- 6
select substring(ename, 1, 3) as e from ex.emp;

-- 7
select regexp_replace(ename, 'A', 'a') as e from ex.emp;

-- 8
select ename, hiredate
from ex.emp
where
    year(hiredate) + 10 < year(current_date);

-- 9 显示员工的详细资料,按姓名排序
select ename from ex.emp order by ename;

-- 10显示员工的姓名和受雇日期,根据其服务年限,将最老的员工排在最前面.
select ename, hiredate
from ex.emp
order by (current_date - hiredate) desc;

-- 11显示所有员工的姓名、工作和薪金,按工作的降序排序,若工作相同则按薪金排序.
select ename, job, sal from ex.emp order by job desc, sal desc;

-- 12 显所有员工的姓名、加入公司的年份和月份,按受雇日期所在月排序,若月份相同则将最早年份的员工排在最前面
select ename, year(hiredate), month(hiredate)
from ex.emp
order by month(hiredate) desc, year(hiredate) asc;

-- 13找出在(任何年份的)2月受聘的所有员工。
select ename from ex.emp where month(hiredate) = 2;

-- 14 对于每个员工,显示其加入公司的天数.
select ename, day((current_date - hiredate)) as d from ex.emp;

-- 15 显示姓名字段的任何位置包含 "A" 的所有员工的姓名
select ename from ex.emp where ename regexp '[A]';

-- 多表关联查询
### 01,列出至少有一个员工的所有部门
select
    dname
from
    dept d inner join emp e
    on d.deptno = e.deptno
group by dname
having count(*) >= 1;

### 02,列出薪金比“MARTIN”多的所有员工。（大于最大薪水MARTIN员工）

select
    ename
from
    ex.emp
where sal >(select sal from ex.emp where ename = 'MARTIN') and ename != 'MARTIN';

### 03,列出所有员工的姓名及其直接上级的姓名
select
    e.ename,
    m.ename
from
    emp e inner join emp m
    on e.mgr = m.empno;

### 04,列出受雇日期早于其直接上级的所有员工
select e.ename, m.ename,e.hiredate,m.hiredate
from emp e
    inner join emp m on e.mgr = m.empno
where e.hiredate < m.hiredate;

### 05,列出部门名称和这些部门的员工信息，包括那些没有员工的部门
select
    dname,
    ename
from
    dept d right join emp e
    on d.deptno = e.deptno;

show tables;

### 06,列出所有job为“CLERK”（办事员）的姓名及其部门名称
select
    dname,
    ename
from
    dept d inner join emp e
    on d.deptno = e.deptno
where job = 'CLERK';

### 07,列出最低薪金大于1500的各种工作。
select
    e.job,
    min(e.sal)
from
    dept d inner join emp e
    on d.deptno = e.deptno
group by e.job
having min(e.sal) > 1500;

### 08,列出在部门“SALES”（销售部）工作的员工的姓名，假定不知道销售部的部门编号
select
    ename
from
    dept d inner join emp e
    on d.deptno = e.deptno
where
    dname = 'SALES';

### 09,列出薪金高于公司平均薪金的所有员工。
select
    ename
from
    dept d inner join emp e
    on d.deptno = e.deptno
where sal>(select avg(sal) from emp);

select avg(sal) from emp;

### 10,列出与“SCOTT”从事相同工作的所有员工。
select
    ename
from
    dept d inner join emp e
    on d.deptno = e.deptno
where job = (select job from emp where ename = 'SCOTT');

### 11,列出薪金等于部门30中员工的薪金的所有员工的姓名和薪金
select sal,ename from(emp)
where sal in(
select
    sal
from
    emp
where deptno = 30);

### 12,列出薪金高于在部门30工作的所有员工的薪金的员工姓名和薪金。
select
    ename,
    sal
from
    emp
where sal>(select max(sal) from emp where deptno =30);

### 13,列出在每个部门工作的员工数量、平均工资和平均服务期限
select
    count(*) as `number`,
    avg( sal + if(comm is null, 0, comm) ) as ang_sal,
    round(avg((unix_timestamp(current_date) - unix_timestamp(hiredate))/(60*60*24*365)),2) as avg_year
from
    emp
group by deptno;

### 14,列出所有员工的姓名、部门名称和工资。
select
    ename,
    dname,
    ( sal + if(comm is null, 0, comm) )
from
    dept d inner join emp e
    on d.deptno = e.deptno;

### 15,列出从事同一种工作但属于不同部门的员工的一种组合
select
    distinct
    (case when e.ename > d.ename then concat(e.ename,' ',d.ename)
    else concat(d.ename,' ',e.ename) end) as n,
    (case when e.deptno > d.deptno then concat(e.deptno,' ',d.deptno)
    else concat(d.deptno,' ',e.deptno) end) as deptno,
    concat(e.job,' ',d.job) as job
from
    emp e cross join emp d
where e.job = d.job and e.deptno != d.deptno
order by n;

### 16,列出所有部门的详细信息和部门人数
select
    distinct
    d.deptno,
    dname,
    loc,
    count(*) over (partition by d.deptno) 
from
    dept d inner join emp e
    on d.deptno = e.deptno;

### 17,列出各种工作的最低工资
select
    distinct
    min( sal + if(comm is null, 0, comm) ) over (partition by job)
from
    emp;

### 18,列出各个部门的MANAGER（经理）的最低薪金（job为MANAGER）
select
    distinct
    min( sal + if(comm is null, 0, comm) ) over ( partition by deptno )
from
    emp
where job = 'MANAGER';

### 19,列出所有员工的年工资，按年薪从低到高排序。
select
    (sal+if(comm is null,0,comm)) as year_money
from
    emp
order by year_money desc;

### 20,列出所有job=‘CLERK’ 的员工平均薪资

select
    ename
from
    emp
where job = 'CLERK';

### 21,列出job=‘CLERK’员工的平均薪资 按照部门分组

select ename, avg(sal) over ( partition by deptno)
from emp
where
    job = 'CLERK';
### 22,列出job=‘CLERK’员工的平均薪资 按照部门分组 并且部门编号 in(10,30) 按照平均薪资 降序排列
select ename, avg(sal) over ( partition by deptno) as avg_sal
from emp
where
    job = 'CLERK'
order by avg_sal desc;

### 23,列出job=‘CLERK’员工的平均薪资 按照部门分组 并且部门编号 in(20,30) 并且部门员工数量>=2人 按照平均薪资 降序排列
select
    ename,
    avg_sal
from(
select ename, avg(sal) over (partition by deptno) as avg_sal,count(*) over ( partition by deptno ) as count_number
from emp
where
    job = 'CLERK'  and deptno in (20,30)
order by avg_sal desc) as a
where count_number >=2;

## 2、公司收入
create table ex.burks (
    burk STRING,
    `year` STRING,
    tsl01 DOUBLE,
    tsl02 DOUBLE,
    tsl03 DOUBLE,
    tsl04 DOUBLE,
    tsl05 DOUBLE,
    tsl06 DOUBLE,
    tsl07 DOUBLE,
    tsl08 DOUBLE,
    tsl09 DOUBLE,
    tsl10 DOUBLE,
    tsl11 DOUBLE,
    tsl12 DOUBLE
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

load data local inpath
    '/root/burks.csv'
overwrite into table
    ex.burks;

select * from ex.burks limit 10;

### 1、统计每个公司每年按月累计收入

### 输出结果
###  公司代码,年度,月份,当月收入,累计收入
select
    burk as `公司代码`,
    `year` as `年度`,
    1 as `月份`,
    tsl01 as `当月收入`,
    tsl01 as `累计收入`,
    2 as `月份`,
    tsl02 `当月收入`,
    (tsl01+tsl02) as `累计收入`,
    3 as `月份`,
    tsl03 `当月收入`,
    (tsl01+tsl02 + tsl03) as `累计收入`,
    4 as `月份`,
    tsl04 `当月收入`,
    (tsl01 + tsl02 + tsl03+ tsl04) as `累计收入`,
    5 as `月份`,
    tsl05 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05) as `累计收入`,
    6 as `月份`,
    tsl06 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05+ tsl06) as `累计收入` ,
    7 as `月份`,
    tsl07 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06+ tsl07) as `累计收入`,
    8 as `月份`,
    tsl08 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08) as `累计收入`,
    9 as `月份`,
    tsl09 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08+ tsl09) as `累计收入`,
    10 as `月份`,
    tsl10 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08 + tsl09+ tsl10) as `累计收入`,
    11 as `月份`,
    tsl11 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08 + tsl09 + tsl10+ tsl11) as `累计收入`,
    12 as `月份`,
    tsl12 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08 + tsl09 + tsl10 + tsl11+ tsl12) as `累计收入`
from
    ex.burks

select
    burk,
    `year`,
    index + 1 as month,
    tsl,
    -- 累计求和
    sum(tsl) over (
        partition by
            burk,
            `year`
        order by index + 1
    ) as lj_tsl
from ex.burks lateral view posexplode(
        array(
            tsl01, tsl02, tsl03, tsl04, tsl05, tsl06, tsl07, tsl08, tsl09, tsl10, tsl11, tsl12
        )
    ) T as index, tsl;

### 2、统计每个公司当月比上年同期增长率
### 公司代码,年度,月度,增长率（当月收入/上年当月收入 - 1）

select
    `公司代码`,
    `年度`,
    `月份`
from (



select
    burk as `公司代码`,
    `year` as `年度`,
    1 as `月份`,
    tsl01 as `当月收入`,
    tsl01 as `累计收入`,
    2 as `月份`,
    tsl02 `当月收入`,
    (tsl01+tsl02) as `累计收入`,
    3 as `月份`,
    tsl03 `当月收入`,
    (tsl01+tsl02 + tsl03) as `累计收入`,
    4 as `月份`,
    tsl04 `当月收入`,
    (tsl01 + tsl02 + tsl03+ tsl04) as `累计收入`,
    5 as `月份`,
    tsl05 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05) as `累计收入`,
    6 as `月份`,
    tsl06 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05+ tsl06) as `累计收入` ,
    7 as `月份`,
    tsl07 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06+ tsl07) as `累计收入`,
    8 as `月份`,
    tsl08 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08) as `累计收入`,
    9 as `月份`,
    tsl09 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08+ tsl09) as `累计收入`,
    10 as `月份`,
    tsl10 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08 + tsl09+ tsl10) as `累计收入`,
    11 as `月份`,
    tsl11 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08 + tsl09 + tsl10+ tsl11) as `累计收入`,
    12 as `月份`,
    tsl12 `当月收入`,
    (tsl01 + tsl02 + tsl03 + tsl04 + tsl05 + tsl06 + tsl07 + tsl08 + tsl09 + tsl10 + tsl11+ tsl12) as `累计收入`
from
    ex.burks);
-- 1
select *
from (
        select concat(
                e.first_name, ' ', e.last_name
            ) as name, e.email, j.job_title, d.department_name
        from
            employees e
            inner join departments d on e.department_id = d.department_id
            inner join jobs j on e.job_id = j.job_id
    ) l
union
(
    select concat(
            e.first_name, ' ', e.last_name
        ) as name, e.email, j.job_title, e.department_id
    from employees e
        inner join jobs j on e.job_id = j.job_id
    where
        e.department_id is null
);
-- department_id is null

-- 2
select concat(
        e.first_name, ' ', e.last_name
    ) as name, j.job_title, e.salary
from employees e
    inner join jobs j on e.job_id = j.job_id
where
    salary = (
        select max(salary)
        from employees e
    );

select max(salary) from employees e;
-- 3
select d.department_name, avg(e.salary) as salary
from employees e
    inner join departments d on e.department_id = d.department_id
group by
    d.department_name;
-- 4
select concat(
        e.first_name, ' ', e.last_name
    ) as name, e.salary, d.department_name
from employees e
    inner join departments d on e.department_id = d.department_id
where
    e.salary > 5000;
-- 5
select concat(
        e.first_name, ' ', e.last_name
    ) as name, j.job_title, e.commission_pct
from employees e
    inner join jobs j on e.job_id = j.job_id
where
    e.commission_pct = max(e.commission_pct);
-- 6
select max(e.salary) as max_sa, min(e.salary) as min_sa, j.job_id
from employees e
    inner join jobs j on e.job_id = j.job_id
group by
    j.job_id;
-- 7
select concat(
        e.first_name, ' ', e.last_name
    ) as name, e.hiredate, j.job_title
from employees e
    inner join jobs j on e.job_id = j.job_id
where
    year(e.hiredate) < 2000;

-- 8
select count(*) as person_number, d.department_id
from employees e
    inner join departments d on e.department_id = d.department_id
group by
    d.department_id
    -- 9

select concat(
        e.first_name, ' ', e.last_name
    ) as name, e.salary, d.department_name
from employees e
    inner join departments d on e.department_id = d.department_id
where (e.salary, d.department_name) in (
        select max(e.salary) as salary, d.department_name
        from employees e
            inner join departments d on e.department_id = d.department_id
        group by
            d.department_name
    )
    -- 10

select
    -- *
    concat(
        e.first_name, ' ', e.last_name
    ) as name, e.salary, d.department_name
from
    employees e
    inner join departments d on e.department_id = d.department_id
    inner join (
        select avg(salary) as avg_salary, d.department_name
        from employees e
            inner join departments d on e.department_id = d.department_id
        group by
            d.department_name
    ) ne -- 为子查询表的名字,怕new是关键词，所以取前面两位
    on d.department_name = ne.department_name
where
    e.salary > ne.avg_salary;

-- 11
select count(*) as 人数, j.job_id
from employees e
    inner join jobs j on e.job_id = j.job_id
group by
    j.job_id;

-- 12
select max(salary), min(salary), department_name
from employees e
    inner join departments d on e.department_id = d.department_id
group by
    department_name;

-- 13
select concat(
        e.first_name, ' ', e.last_name
    ) as ename, e.email, e.job_id, concat(
        m.first_name, ' ', m.last_name
    ) as mname
from employees e
    inner join employees m on e.manager_id = m.employee_id;

-- 14
select
    avg(commission_pct) as avg_commission_pct,
    department_name
from employees e
    inner join departments d on e.department_id = d.department_id
group by
    department_name;

-- 15
select count(*) as 员工人数, l.city
from
    employees e
    inner join departments d on e.department_id = d.department_id
    inner join locations l on d.location_id = l.location_id
group by
    l.city;

-- 16
select count(distinct e.job_id) as 职位种类数, department_name
from
    employees e
    inner join departments d on e.department_id = d.department_id
    inner join jobs j on e.job_id = j.job_id
group by
    department_name;

-- 17
select
    -- *
    concat(
        e.first_name, ' ', e.last_name
    ) as name, e.salary, j.job_title
from employees e
    inner join jobs j on e.job_id = j.job_id
    inner join (
        select avg(salary) as avg_salary, j.job_title
        from employees e
            inner join jobs j on e.job_id = j.job_id
        group by
            j.job_title
    ) ne -- 为子查询表的名字,怕new是关键词，所以取前面两位
    on j.job_title = ne.job_title
where
    e.salary > ne.avg_salary;

-- 18
select count(*) as 员工人数, l.country_id
from
    employees e
    inner join departments d on e.department_id = d.department_id
    inner join locations l on d.location_id = l.location_id
group by
    l.country_id;

-- 19
select concat(
        e.first_name, ' ', e.last_name
    ) as ename, j.job_title
from employees e
    inner join jobs j on e.job_id = j.job_id
where
    manager_id is null;

-- 20
select concat(
        e.first_name, ' ', e.last_name
    ) as ename, j.job_title, e.salary
from employees e
    inner join jobs j on e.job_id = j.job_id
where
    e.job_id = 'IT_PROG';
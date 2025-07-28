### 1、行列转换
数据:
表1
姓名,科目,分数
name,item,score
张三,数学,33
张三,英语,77
李四,数学,66
李四,英语,78

表2
姓名,数学,英语
name,math,english
张三,33,77
李四,66,78

> 创建表1
```sql
create table bigdata.table1(
    name string,
    item string,
    score double
)row format delimited fields terminated by ','
stored as textfile;

load data local inpath '/root/table1.csv' overwrite into table bigdata.table1;
```

> 将表1 转换为表2 (case when 流程控制函数)
```sql
create table bigdata.table3 as 
select
    name,
    -- 汇总数据成绩：如果item 等于‘数学’，取score成绩，否则取0，再按学生求和
    sum(
        case
            when item = '数学' then score
            else 0
        end
    )as math,
    -- 汇总英语成绩：如果item等于‘英语’，取score成绩，否则取0，再按学生求和
    sum(
        case
            when item = '英语' then score
            else 0
        end
    )as english
from bigdata.table1
group by name;
```

> 将表2转为表1

```sql
select
    name,
    item,
    score
from bigdata.table3
lateral view explode(
    map(
        '数学',math,  -- map的key为数学，value为math的值
        '英语',english -- map的key为英语,value为english的值
    )
) T as item,score; -- 为map 的key命名为item,value命名为score
```


### 2、连续登录
数据:
user_id,login_date
01,2021-02-28
01,2021-03-01
01,2021-03-02
01,2021-03-04
01,2021-03-05
01,2021-03-06
01,2021-03-08
02,2021-03-01
02,2021-03-02
02,2021-03-03
02,2021-03-04
02,2021-03-06
03,2021-03-06

> 创建数据表


```sql
create table bigdata.user_login_log(
    user_id string,
    login_date string
)row format delimited fields terminated by ','
stored as textfile

load data local inpath '/root/user_login_log.csv' overwrite into table
```



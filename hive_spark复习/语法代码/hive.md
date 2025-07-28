### DDL 数据定义语言
#### 数据库
##### 创建数据库

***create database [if not exists] database_name***
***[comment database_comment]***
***[location hdfs_path]***
***[with dbproperties(property_name=property_value,...)]***

```sql
create database if not exists db_test2
comment "这是个数据库"
location '/db_test2'
with dbproperties('create_date' = '2025-06-12');
```

ps.如果不指定路径,其默认路径为${hive.metastore.warehouse.dir}/database_name.db


##### 查询数据库

***显示所有数据库***

***show databases [like 'identifier_with_wildcards'];***

-- 注: 'like' 通配符表达式说明: *表示任意个字符, | 表示或的关系

```sql
show databases like 'db_test';
```


***查看数据库信息***

***describe database [extended] db_name;***

> 查看基本信息

```sql
desc database db_test3;
```

> 查看更多信息
```sql
desc database extended db_hive3;
```

##### 修改数据库

> 修改dbproperties
***alter database database_name set dbproperties(property_name = property_value,...);***

> 修改location
***alter database database_name set location hdfs_path;***

> 修改owner user
***alter database database_name set owner user user_name;***


eg:
> 修改dbproperties
```sql
alter database db_test3 set dbproperties ('create_date'='2025-06-13');
```

##### 删除数据库

***drop database (if exists) database_name [restrict|cascade]***

ps.
restrict: 严格模式,若数据不为空则会删除失败,默认为该模式

cascade:级联模式,不论数据库是否为空,都会将库删除

eg
> 删除空数据库
```sql
drop database db_test2;
```

> 删除非空数据库
```sql
drop database db_test3 cascade;
```

##### 切换当前数据库

***use database_name;***

#### 表

##### 创建表


> 普通建表

***create [temporary] [external] table [if not exists]***
***[db_name.]table_name***
***[(col_name data_type[comment col_comment],***
***........)]***
***[comment table_comment]***
***[partitioned by (col_name data_type [comment col_comment],...)]***
***[clustered by(col_name,col_name,...)[sorted by (col_name [ASC|DESC],...)] into num_buckets BUCKETS]***
***[row format row_format]***
***[stored as file_format]***
***[location hdfs_path]***
***[tblproperties (property_name=property_value,...)]***

> 三种表(内部、外部、临时)

-- 外部表: external，删除时，删除表但不会删除hdfs中的数据。因为hive只接管元数据但不接管hdfs中的数据

-- 内部表: 默认为内部表,删除表的同时也会将数据一并删除数据。内部表,hive会完全接管该表(包括元数据和hdfs中的数据)

-- temporary: 临时表,创建只有在这个窗口sql才存在的表,当退出sql时，此表会消失

> data_type

tinyint、smallint、int、bigint 整数型    
boolean  布尔型(0、1/T、F)
float  单精度浮点型
double 双精度浮点型
decimal  精确存储数据类型  deciaml(m,d) eg :decimal(5,9) 范围为-999.99刀999.99
string  
timestamp  时间戳类型
binary  二进制类型
复杂类型:array、map、struct  
array<string>  数据类型
map<string,int>  元组类型
struct<id:int,name:string> 结构体类型】

> row format

delimited fields terminated by 列的分隔符

collection items terminated by: array、map、struct 中每个元素之间的分隔符

map keys terminated by: map 中 key 与 value分隔符

lines terminated by: 行分隔符

> stored as 文件格式

stored as textfile

stored as orc

stored as parquet

> location hdfs_path

> tblproperties(property_name=property_value,...)

> create table as select (CTAS) 

***create [temporary] table [if not exists] table_name***
***[comment table_comment]***
***[row format row_format]***
***[stored as file_format]***
***[location hdfs_path]***
***[tblproperties (property_name=property_value,...)]***
***[as select_statement]***


> create table like

***create [temprorary] [external] table [if not exists]***
***[db_name.]table_name***
***[like exist_table_name]***
***[row format row_format]***
***[stored as file_format]***
***[location hdfs_path]***
***[tblproperties (property_name=property_value,...)]***


##### 查看表

> 显示所有表

***show tables [in database_name] like ['identifier_with_wildcards'];***


> 查看表信息

***desc [extended|formatted] [db_name.]table_name***

extened : 战士详细信息
formatted : 对详细信息进行格式化展示

##### 修改表

> 重命名表

***alter table table_name rename to new_table_name***

> 增加列

***alter table table_name add columns (col_name data_type [comment col_comment],...)***

> 更新列

***alter table table_name change [column] col_old_name col_new_name column_type [comment col_comment] [FIRST|AFTER column_name]***

> 替换列

***alter table table_name replace columns (col_name data_type [comment col_comment],...)***

##### 删除表

***drop table [if exists] table_name***

##### 清空表

***truncate [table] table_name;***

ps.只清空表的数据，而不删除表


### DML 数据操作语言

#### load

***load data [local] inpath 'filepath' [overwrite] into table tablename [partition (partcol=val1,partcol2=val2,...)];***


#### insert

> 将查询结果插入表中

***insert (into|overwrite) table tablename [partition (partcol1=val1,parcol2=val2,...)] select_statement;***


> 将给定的values插入表中

***insert (into|overwrite) table tablename [partition (partcol1[=val1],partcol2[=val2]...)] values values_row [,values_row]***


> 将查询结果写入目标路径

***insert overwrite [local] directory directory_name [row format row_format] [stored as file_format] select_statement;***


#### export&import

> 导出
***export table tablename to 'export_target_path'***


> 导入
***import [external] table new_or_original_tablename from source_path [location 'import_target_path']***


### DQL 数据查询语言

> 总语法

***select [all|distinct] select_exp,select_exp,...***
***from table_reference***
***[where where_condition]***
***[group by col_list]***
***[having col_list]***
***[order by col_list]***
***[cluster by col_list |[distribute by col_list][sort by col_list]]***
***[limit number]***

#### 基本查询
>全表及列查询

eg
```sql
select * from dept;
select * from emp;
-- sql语言大小写不敏感
select 
  deptno,
  dname,
  loc
from dept;
```

> 列别名
eg:
```sql
-- 取别名的好处，便于计算。
select 
  deptno,
  dname as name,
  loc
from dept;
```

> limit
eg:
```sql
-- 限制返回行数

select
  empno,
  ename,
  job,
  sal,
  deptno
from emp
limit 3;

select
  empno,
  ename,
  job,
  sal,
  deptno
from emp
limit 2,3;   -- 表示从第二行开始，向下查找三行,,下标从0开始
```

> where

```sql
-- 将不满足条件的行过滤。
-- where子句紧随from子句后面
-- 查询薪水大于8000的所有员工
select
  empno,
  ename,
  job,
  sal as salary,
  deptno
from emp
where sal > 8000;
-- where 子句后面不能使用字段别名
```


> having 分组后过滤

```sql
-- having 与where不同点
-- where后面不能跟聚合函数，而having后面可以使用分组聚合函数
-- having只用于group by分组统计语句



-- 求每个部门的平均薪水高于4000的部门
-- （1）求每个部门的平均工资
select
  deptno,
  avg(sal) as avg_salary
from emp
group by deptno;
-- （2）求每个部门的平均薪水大于4000的部门
select
  deptno,
  avg(sal) as avg_salary
from emp
group by deptno
having avg_salary > 4000;
```


> 关系运算函数
eg
```sql
-- 关系运算符 用于where having
=
<=>
!=  <>
<
>
>=
<=

a [not] between b and c

a is null

a is not null

a [not] like b

in(num1,num2)
-- a rlike b, a regexp b    
```

> 逻辑运算函数
```sql
and  -- 逻辑并
or  -- 逻辑或
not -- 逻辑非


-- 查询薪水大于8000，部门是30的
select
  empno,
  ename,
  job,
  sal as salary,
  deptno
from emp
where sal > 8000 and deptno=30;



-- 查询薪水大于8000，或者部门是30的
select
  empno,
  ename,
  job,
  sal as salary,
  deptno
from emp
where sal > 8000 or deptno=30;


-- 查询除了20部门和30部门以为外的员工信息
select
  empno,
  ename,
  job,
  sal as salary,
  deptno
from emp
where deptno not in(30,20);


select * from emp where job is not null;
```
> 聚合函数
eg
```sql
count(*) -- 表示统计所有行数，包括null值
count(1) -- 表示统计所有行数，包括null值
count(某列)  -- 表示统计所有行数，不包括null值
max() -- 求最大值，不包括null，除非所有值都是null
min() -- 求最小值，不包括null，除非所有值都是null
sum() -- 求和，不包括null
avg() -- 平均值，不包括null


select count(*) as num
from emp;



select max(sal) as max_salary
from emp;

select sum(sal) as max_salary
from emp;


select avg(sal) as avg_salary
from emp
```
#### 分组
> group by

eg:
```sql
-- 计算emp表每个部门的平均工资
select
  t.deptno,
  avg(t.sal) as avg_salary
from emp t
group by t.deptno;


-- 计算emp表中每个部门中每个岗位最高薪水

select
  t.deptno,
  t.job,
  max(t.sal) as max_salary
from emp t
group by t.deptno,t.job;
```

#### join

> 等值join
-- hive 只支持等值连接，不支持非等值连接

> 内连接 默认为内连接
```sql
-- 只有进行连接的两个表中都存在与连接条件相匹配的数据才会被保留下来
select
  e.empno,
  e.ename,
  d.dname
from emp e
join dept d
on e.deptno=d.deptno;
```

> 左外连接
eg
```sql
-- join操作符左边表中符合where子句的所有记录将会被返回。
select
  e.empno,
  e.ename,
  d.dname
from emp e
left join dept d
on e.deptno=d.deptno;
```

> 右外连接
eg:
```sql
-- join操作符右边表中符合where子句的所有记录将会被返回
select
  e.empno,
  e.ename,
  d.dname
from emp e
right join dept d
on e.deptno=d.deptno;
```

> 全外连接
```sql
-- 返回所有表中符合where语句条件的所有记录，如果任一表的指定字段没有符合条件的值，那么就使用null值替代
select
  e.empno,
  e.ename,
  d.dname
from emp e
full join dept d
on e.deptno=d.deptno;
```

> 多表连接
eg
```sql
-- 连接n个表，至少需要n-1个条件
-- location
// 部门位置id  部门的位置
// 1700     合肥
// 1800		 宿州
// 1900     滁州
// 1900     滁州

create table location(
  loc int,
  loc_name string
)
row format delimited fields terminated by '\t';


select
  e.ename,
  d.dname,
  l.loc_name
from emp e
join dept d
on e.deptno=d.deptno
join location l
on d.loc = l.loc;
```
>笛卡尔集

```sql
-- 省略连接条件
-- 连接条件无效
-- 表中所有行互联

select
  empno,
  dname
from
emp,dept;
```

>联合(union/union all) hive里面union去重 union all 不去重.spark里面两个都不去重

```sql
-- union & union all  上下拼接

// union & union all上下拼接sql结果，和join区别，join是左右关联，union & union all
//上下拼接，union去重  union all 不去重

-- 要求：
-- （1）两个sql结果，列的个数必须相同
-- （2）两个sql结果。上下所对应的列的类型必须一致


-- 将员工表30部门的员工信息和40部门的员工信息，利用union拼接显示
select
  *
from emp
where deptno = 30
union
select
  *
from emp
where deptno = 40;
```

#### 排序
> 全局排序(order by)
eg:
```sql
-- desc 降序
-- asc 升序（默认）
-- order by 全局排序，只有一个reduce
-- 注意： order by子句在select语句结尾

select
  *
from emp
order by sal;


select
  *
from emp
order by sal desc;


-- 按照员工的薪水*2进行排序（按别名排序）
select
  ename,
  sal * 2 as d_sal
from emp
order by d_sal

-- 按照部门和工资升序排序 (按多个字段排序)
select
  ename,
  deptno,
  sal
from emp
order by deptno,sal;
```

> 每个reduce内部排序(sort by)

```sql
-- sort by 对大规模的数据集 order by 的效率是非常低，在很多情况下并不需要全局排序，此时sort by
-- sort by 为每个reduce产生一个排序文件，每个reduce内部进行排序，对全局结果来说就不是排序



-- 设置reduce各数
set mapreduce.job.reduces=3;

-- 查看reduce各数
set mapreduce.job.reduces;



-- 根据部门编号降序查看员工信息

select
 *
from emp
sort by deptno desc;
```

> 分区(distribute by)
eg
```sql
select *
from emp
distribute by deptno
sort by sal desc;
```

> 分区排序(cluster by)

eg:
```sql
-- cluseter by 只能升序排，兼容distribute by 和 sort by的功能


select
  *
from emp
cluster by deptno;
```

#### 函数

> ***单行函数***
> 算术运算函数     + - * / % & ｜ ^ ～

eg：
```sql
select sal + 10 from emp;
```
> 数值函数     
>   ■ round：四舍五入
    ■ ceil：向上取整
    ■ floor：向下取整

eg:
```sql
select round(3.1415926);
select ceil(3.14);
select floor(3.5);
select
  round(avg(sal),2) as avg_sal
from emp;
```

> 字符串函数
> substring:截取字符串
```sql
-- 语法1: substring(string A,int start) 返回值为string
-- 说明: 返回字符串A 从start位置到结尾的字符串
select substring('Hadoop',3);
select substring('Hadoop',-3);

-- 语法2: substring(string A,int start,int len) 返回值为string
-- 说明： 返回字符串A从start位置开始，长度为len的字符串
select substring('lanzhishujiaxueyuanllinxu',7,13);
```

> replace:替换

```sql
-- 语法: replace(string A,string B,string C) 范围值为string
-- 说明: 将字符串A 中的字符串B 替换为 字符串C
select replace('lanzhishujiaxueyuan','xueyuan','daxue');
```

> regexp_replace:正则替换

```sql
-- 语法:regexp_replace(string A,string B,string C) 返回值为string
-- 说明:将字符串A 中符合
```

> regexp：正则匹配

```sql
-- 语法:string A regexp '正则表达式' 返回值为boolean
-- 说明: 如果字符串符合正则表达式,则返回true,否则为false

select 'abcdttthhhj' regexp 'ct+';
```

> repeat: 重复字符串

```sql
-- 语法:repeat(string A,int n) 返回值为string
-- 说明: 将字符串A 重复n遍

select repeat('暑假学院',3);
```

> split:字符串分隔
```sql
-- 语法: split(string str,string pat) 返回值为array
-- 说明: 按正则表达式pat匹配到的内容分隔str,分隔后的字符串,以数组的形式进行返回

select split('h-a-d-o-o-p','-');
```

> nvl:替换null值

```sql
-- 语法:nvl(A,B)
-- 说明: 如果A的值不为null，则返回A，否则返回B
select nvl(null,1)
```


> concat：拼接字符串

```sql
-- 语法: concat(string A,string B.string C,...) 返回值为string
-- 说明: 将字符串ABC...进行拼接为一个字符串


select concat('anhui','hefei','shushan');
```

> concat_ws:以指定分隔符拼接字符串或者字符串数组

```sql
-- 语法:concat_ws (String A,String ... | array (string)) 返回值为string
-- 说明: 使用分隔符A拼接多个字符串,或者一个数组的所有元素

select concat_ws('-','2025','06','13');

select concat_ws('-',array('2025','06','14'));
```

> get_json_object:解析json 字符串
```sql
-- 语法: get_json_object (string json_string,string path) 返回值为string
-- 说明: 解析json字符串 json_string,返回path指定的内容,如果输入的json字符串错误,则返回null


select get_json_object('{"name":"zhangsan","friends":["zhangsan1", "zhangsan2"],"students":{"lisi1":20,"lisi2":22},"address":{"street":"shushanqu","city":"hefei","code":230001}}','$.students.lisi1')
```

> 日期函数
> unix_timestamp 返回当前或指定时间的时间戳

```sql
-- 语法:unix_timestamp()
-- 返回值: bigint
-- 说明；前面是日期 后面是值日期传进来的格式
select unix_timestamp('2025/06/14 09-21-15','yyyy/MM/dd HH-mm-ss')
```

> from_unixtime:转化unix时间戳(从1970-01-01 00:00:00 UTC) 到当前时区的时间格式

eg:
```sql
-- 语法:from_unixtime(bigint unixtime[,string format])
-- 返回值:string 类型
select from_unixtime(1749863973,'yyyy/MM/dd');
```

>current_date: 当前日期
eg:
```sql
select current_date;  -- 返回的内容：年月日
```

> month: 获取日期中的月
eg:
```sql
-- 语法：month(string date)
-- 返回值： int

select month('2025-06-14 9:28:50');
```
> day: 获取日期中的日

```sql
-- 语法：day(string date)
-- 返回值： int

select day('2025-06-14 9:28:50');
```
> hour:获取日期中的小时

eg:
```sql
-- 语法: hour(string date)
-- 返回值:int
select hour('2025-06-14 09:28:50');
```

> datediff：两个日期相差的天数(结束日期减去开始日期的天数)

```sql
-- 语法:datediff(string end_date,string start_date);
-- 返回值: int


select datediff('2025-06-14','2025-04-14');
-- 学习的天数
```

> date_add:在日期上加上天数
```sql
-- 语法: date_add(string start_date,int days)
-- 返回值: string 类型
-- 说明:返回开始日期start_date增加days天后的日期

select date_add('2025-06-14',2);
```

> date_sub:日期减天数
```sql
-- 语法:date_sub (string start_date,int days)
-- 返回值:string类型
-- 说明: 返回开始日期start-date 减少days太难后的日期

select date_sub('2025-06-14 09:28:50',2);
```

> date_format: 将标准日期解析成指定格式字符串

```sql

select date_format('2025-06-14 09:28:50','yyyy年MM月dd日 HH时mm分ss秒');
```

> 流程控制函数
> case when:条件判断函数
```sql
-- 语法: case when a then b [when c then d] [else f] end
-- 返回值；T
-- 说明:如果a为true则返回b,如果c为true则返回d，否则返回e



select case when 1=2 then 'zhangsan'
            when 2=2 'lisi'
        else 'shujia' end
from students;

-- 语法2 case a when b then c [when d then e] [else f] end
-- 返回值:T
-- 说明: 如果a=b,那么返回c;如果a=d，那么返回e 否则返回f

select case 100 when 50 then 'zhangsan' when 100 then 'shujia' else 'lanzhi' end,
    id,
    name
from students
limit 5;
```

> if:条件判断
```sql
-- 语法:if [boolean testcondition,T valuetrue,T valueFalse0orNull]
-- 返回值:T
-- 说明:当条件testcondition为true时，则返回valueTrue，否则返回valueFalseorNull


// (a>b)?a:b
-- 条件满足,输出正确
select if(10>5,'正确','错误')
select if(10<5,'正确','错误')
```

> 集合函数
> size: 集合中元素的个数

```sql
create table test_tbl1(
    name string,
    friends array<string>,
    students map<string,int>,
    address struct<street:string,city:string,code:int>
)
row format delimited
fields terminated by '\t'
collection items terminated by ','
map keys terminated by ':'
lines terminated by '\n';



-- 数据 zhangsan    zhangsan1,zhangsan2    lisi1:18,lisi:16    shushanqu,hefei,230001


-- jsob格式数据建表
create table test_tbl3(
    name string,
    friends array<string>,
    students map<string,int>,
    address struct<street:string,city:string,code:int>
)
row format serde
'org.apache.hadoop.hive.serde2.JsonSerDe';
-- 数据 {"name":"zhangsan","friends":["zhangsan1", "zhangsan2"],"students":{"lisi1":20,"lisi2":22},"address":{"street":"shushanqu","city":"hefei","code":230001}}


select size(friends) as friends_num from test_tbl1;

select
  name,
  size(friends),
  students['lisi1'],
  address.city
from test_tbl2;
```

> map:创建map集合
```sql
-- 语法:map(key1,value1,key2,value2,....)
-- 说明:根据输入的key和value构建map类型 kv对


select map('name','zhangsan','age',18);
-- 结果{"name":"zhangsan","age"；"18"}
```

> map_keys:返回map中的key,并以列表的形式返回
```sql
select map_keys(map('name','zhangsan','age',18));
-- 结果["name","age"]
```

> map_values:返回map中的value，并且以列表的形式返回
eg
```sql
select map_values(map('name','zhangsan','age',18));
-- 结果["zhangsan","18"]
```


> array 声明array集合
```sql
-- 语法:array(value1,value2,...)
-- 说明: 根据输入的参数构建数组array类
select array(1,2,3,4,5);
select array('1','2','3','4');
```

> array_contains:判断array中是否包含某个元素

```sql
select array_contains(array('1','2','3','4'),'4');
```

> sort_array:将array中的元素排序

```sql
select sort_array(array('a','d','A','b')); -- 不支持倒序,只支持升序
```

> struct 声明struct中的各属性

```sql
-- 语法:struct(val1,val2,val3,...)
-- 说明:根据输入的参数构建结构体 struct类
select struct('name'.'age','sex');
```

> named_struct 声明struct的属性和值
```sql
select named_struct('name','zhangsan','age',18)
```


> 窗口函数
***定义***
窗口函数:能为每行数据划分一个窗口,然后对窗口范围内的数据进行计算,最后将计算结果返回给该行数据。

***语法***
窗口函数的语法主要包括"窗口"和"函数"两个部分,其中窗口用于定计算,函数用于定计算逻辑

```sql
select
    id,
    `name`,
    sex,
    score,
    函数(score) over (窗口范围) as total_age -- 窗口函数
from students;

-- 函数:绝大数聚合函数都可以配合窗口使用:max min sum count avg

```

>窗口的范围定义分为两种:一种基于行,一种基于值。

> 基于行: 根据行数，划到几行就是几行，要求每行数据的窗口为上一行到当前行
> 基于值: 值相同的时候会将相同的值一起划入范围，要求每行数据的窗口为,值位于当前-1，到当前值

> 窗口函数的省略
over() 中的三部分内容 partition by、order by、(rows|range) between 这三部分内容全可以省略不写

其中 partition by省略不写,表示不分区
order by省略不写 表示不排序
(rows|range) between xxx and xxx 省略不写,则使用其默认值,默认值如
(
***-- 如果over()中包含order by,则默认值为:***
range between unbounded preceding and current row

***-- 如果over()中不包含order by,则默认值为:***
rows between unbounded preceding and unbounded following

***范围从上到下为:***
unbounded preceding
[num] preceding
current now
[num] following
unbounded following
)

> 窗口函数中的函数类型

***聚合函数***
max:最大值
min:最小值
sum:求和
avg：平均值
count:计数

***跨行取值函数***
lag(向前取值)
```sql
select
  id,
  sum(score) as sum_score,
  lag(sum(score),1,0) over (order by sum(score) desc) as last_score
from bigdata.scores
group by id;
```

lead(向后取值)
```sql
select
  id,
  sum(score) as sum_score,
  lead(sum(score),1,0) over (order by sum(score) desc) as lead_score
from bigdata.scores
group by id;
```

first_value(窗口中第一个值)
```sql
select
  id,
  score,
  first_value(score) over ( partition by id order by score  desc) as fv_score
from bigdata.scores;
```

last_value(窗口中最后一个值)
```sql
select
  id,
  score,
  last_value(score) over (partition by id) as lv_score
from bigdata.scores;
```



***排名函数***
rank 多行相同排序共享其值且下一个不相同的为该值的+n
```sql
select
  id,
  sum(score),
  rank() over(order by sum(score) desc) as r
from
  bigdata.scores
group by id;
```

dense_rank 多行相同排序共享其值
```sql
select
  id,
  sum(score),
  dense_rank() over(order by sum(score) desc) as r
from
  bigdata.scores
group by id;
```


row_number 不会共享相同值,直接向下数
```sql
select
  id,
  cid,
  score,
  row_number() over(partition by id order by score desc) as r
from
  bigdata.scores;

-- 全局排序   -- 求topn
select
  id,
  sum(score) as sum_score,
  row_number() over(order by sum(score) desc) as r
from
  bigdata.scores
group by id;
```

***自定义函数***

UDAF:多行变一行(聚合函数)
UDTF:一行变多行(爆炸函数)
通过lateral view和UDTF的配合解决行转列问题
***lateral view 和UDTF联合使用时，表示将UDTF的结果存储在一张虚拟表中***，因为UDTF本身不能使用group by等函数和关联原有的表中的字段，所以将结果存在虚拟表中。



UDF:一行变一行(普通一些函数)
在sql中 array类型类似于python 中的列表类型.
map类型类似于python 中的字典类型(即key-value键值对类型)。












### 分区分桶表
#### 分区表
hive 中的分区表是把一张大表按照业务需求分成几个分区，分散存储到多个目录中，这样可以在查询时使用where子句进行查询。这样在查询时就可以不用扫描全表，而是只扫描分区，从而提高了查询效率。


***语法***

create table dept_partition
(
deptno int,    --部门编号
dname  string, --部门名称
loc    string  --部门位置
)
partitioned by (day string) -- 分区字段
row format delimited fields terminated by '\t';


***读数据***
select *
from dept_partition
where day = '2025-06-12' -- 分区字段

***分区表基本操作***
**查看所有分区信息**
show partitions dept_partition(table_name);

**创建单个分区**
alter table dept_partition add partition(day = '20250612')

**同时创建多个分区(分区之间不能有逗号)**
alter table dept_partition(table_name) add partition(day = '20250612') partition(day='20250613')

**删除单个分区**
alter table dept_partition(table_name) drop partition(day = '20250612')

**删除多个分区**
alter table dept_partition(table_name) drop partition(day = '20250612'),partition(day = '20250613')


**分区表修复**
***修复原因***
hive将分区表的所有分区信息都保存在元数据中,只有元数据与hdfs上的路径一致时,分区表才能正常读写数据。
若用户手动创建/删除分区,hive感知不到,这样就导致了hive的元数据和hdfs的分区路径不一致,从而查不到分区表的数据.
此时就需要对分区表进行修复

***add partition***
若手动创建hdfs的分区路径,hive无法识别,可通过add partition 命令增加分区元数据信息,从而使元数据和分区路径保持一致.

***drop partition***
若手动删除hdfs的分区路径,hive无法识别,可通过drop partition 命令删除分区元数据信息,从而使元数据和分区路径保持一致。

***msck***
若分区元数据和HDFS的分区路径不一致,还可使用msck命令进行修复  

msck repair table table_name [add/drop/sync partitions];

**说明**
msck repair table table_name add partitions：该命令会增加 HDFS存在但元数据缺失的分区信息

msck repair table table_name drop partitions: 该命令会删除 HDFS已经删除但元数据仍然存在的分区信息。

msck repair table table_name sync partitions: 该命令会 同步HDFS路径和元数据分区信息
##### 动态分区
动态分区是指 向分区表插入数据时,数据被写入的分区不由用户指定,而是由每行数据的最后一个字段的值来动态指定

> 动态分区功能总开关(默认为true ，开启)

set hive.exec.dynamic.partition=true

> 严格模式:默认为严格模式,要求必须指定至少一个分区为静态分区
> 非严格模式:允许所有的分区字段都使用动态分区
set hive.exec.dynamic.partition.mode=nonstrict 

> 一条insert语句 可同时创建的最大分区个数,默认1000
set hive.exec.max.dynamic.partitions=1000

> 单个mapper或者reducer 可同时创建的最大的分区个数,默认为100
set hive.exec.max.dynamic.partitions.pernode=100

> 一条insert语句 可以创建的最大文件个数,默认为100000
hive.exec.max.created.files=100000

> 当查询结果为空且进行动态分区时,是否抛出异常,默认为false
hive.error.on.empty.partition=false



##### 二级分区表

**语法**
create table dept_partition2(
deptno int,    -- 部门编号
dname string, -- 部门名称
loc string     -- 部门位置
)
partitioned by (day string,hour string)
row format delimited fields terminated by '\t';


#### 分桶表
> 分区提供了一个隔离数据和优化查询的隔离方法，但不是所有的数据集都可以使用分区
> 那么对于这些不能使用分区的数据集,就可以将数据集划分成桶。
> 当然也可以将表或者分区进一步划分成桶,进行更细粒度的数据范围划分
> 分区针对的是数据的存储路径,分桶针对的是数据文件。
> 分桶表的基本原理是,首先为每行数据计算一个指定字段的数据的hash值。然后模以分桶数,最后将取模运算结果相同的行,写入同一个文件中,
> 这个文件就称为一个分桶(bucket)。
create table stu_buck(
id int, 
name string
)
clustered by (id) 
into 4 buckets
row format ddelimited fields terminated by '\t';

**分桶排序**
create table stu_buck(
id int, 
name string
)
clustered by (id) sorted by (id)
into 4 buckets
row format delimited fields terminated by '\t';


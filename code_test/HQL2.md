1、分区分桶表
1.1 分区表
Hive中的分区就是把一张大表的数据按照业务需要分散的存储到多个目录，每个目录就称为该表的一个分区。
在查询时通过where子句中的表达式选择查询所需要的分区，这样的查询效率会提高很多。
-- 创建分区表
create table bigdata.gateway_records_partition(
  plate_number string comment '车牌号',
  city string comment '城市',
  car_brand string comment '车辆品牌',
  road_id string comment '道路编号',
  speed double comment '车辆速度',
  travel_direction string comment '车辆行驶的方向'
)
partitioned by (gateway_id string  comment '卡口编号')
row format delimited fields terminated by ','
stored as textfile;


// 京T33152,G2054,武汉,比亚迪,R700,42,下行
// 京J48798,G0033,天津,大众,R878,37,下行
// 京U25922,G2322,重庆,奔驰,R576,39,下行
// 京M52241,G5111,南京,本田,R184,27,下行
// 京M65881,G5167,天津,现代,R984,76,上行
// 京N18183,G4952,深圳,丰田,R852,39,上行
// 京X94090,G0056,深圳,特斯拉,R430,65,下行
-- 静态分区
-- 插入数据到分区表中，插入的时候需要指定分区
insert into bigdata.gateway_records_partition partition(gateway_id='G7390')
select 
  plate_number,
  city,
  car_brand,
  road_id,
  speed,
  travel_direction
from bigdata.gateway_records_text_file
where geteway_id='G7390';



-- 查询
select count(1) as num
from bigdata.gateway_records_partition
where gateway_id='G7390';

● 动态分区
-- 动态分区是指向分区表insert数据时，被写往的分区不由用户指定，
-- 而是由每行数据的最后一个字段的值来动态的决定。使用动态分区，
-- 可只用一个insert语句将数据写入多个分区。

-- 动态分区功能总开关（默认true，开启）
set hive.exec.dynamic.partition=true

-- 严格模式和非严格模式
-- 动态分区的模式，默认strict（严格模式），要求必须指定至少一个分区为静态分区，
-- nonstrict（非严格模式）允许所有的分区字段都使用动态分区
set hive.exec.dynamic.partition.mode=nonstrict

-- 一条insert语句可同时创建的最大的分区个数，默认为1000
set hive.exec.max.dynamic.partitions=1000

-- 单个Mapper或者Reducer可同时创建的最大的分区个数，默认为100
set hive.exec.max.dynamic.partitions.pernode=100

-- 一条insert语句可以创建的最大的文件个数，默认100000
hive.exec.max.created.files=100000

-- 当查询结果为空时且进行动态分区时，是否抛出异常，默认false
hive.error.on.empty.partition=false


// 1500100001,施笑槐,22,0,文科六班
// 1500100002,吕金鹏,24,1,文科六班
// 1500100003,单乐蕊,22,0,理科六班
// 1500100004,葛德曜,24,1,理科三班

-- 创建非分区表
create table bigdata.students(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
row format delimited fields terminated by ','
stored as textfile;



-- 创建分区表
create table bigdata.students_partition(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  clazz string comment '班级'
)
partitioned by (sex string comment '性别')
row format delimited fields terminated by ','
stored as textfile
location '/data/bigdata/students_partition';


-- 插入数据自动分区
insert into bigdata.students_partition partition(sex)
select 
  id,
  name,
  age,
  clazz,
  sex
from bigdata.students;


-- 查询
select * from students_partition where sex='0';
select * from students_partition where sex='1';




-- 创建分区表
create table bigdata.students_partition2(
  id string comment '学号',
  name string comment '姓名',
  sex string comment '性别',
  clazz string comment '班级'
)
partitioned by (  age int comment '年龄')
row format delimited fields terminated by ','
stored as textfile
location '/data/bigdata/students_partition2';


-- 插入数据自动分区
insert into bigdata.students_partition2 partition(age)
select 
  id,
  name,
  sex,
  clazz,
  age
from bigdata.students;

-- 创建二级分区
-- 创建分区表
create table bigdata.students_partition3(
  id string comment '学号',
  name string comment '姓名',
  clazz string comment '班级'
)
partitioned by ( sex string comment '性别',age int comment '年龄')
row format delimited fields terminated by ','
stored as textfile
location '/data/bigdata/students_partition3';


-- 插入数据自动分区
insert into bigdata.students_partition3 partition(sex,age)
select 
  id,
  name,
  clazz,
  sex,
  age
from bigdata.students;
1.2 分桶表
// 分区提供一个隔离数据和优化查询的便利方式。不过，并非所有的数据集都可形成合理的分区。
// 对于一张表或者分区，Hive 可以进一步组织成桶，也就是更为细粒度的数据范围划分，
// 分区针对的是数据的存储路径，分桶针对的是数据文件。
// 分桶表的基本原理是，首先为每行数据计算一个指定字段的数据的hash值，
// 然后模以一个指定的分桶数，最后将取模运算结果相同的行，写入同一个文件中，
// 这个文件就称为一个分桶（bucket）。


-- 创建分桶表
create table bigdata.students_bucket(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
clustered by (id) into 10 buckets
row format delimited fields terminated by ','
stored as textfile
location '/data/bigdata/students_bucket';



-- 插入数据
insert into bigdata.students_bucket
select
  *
from students;

2、查询
语法：
SELECT [ALL | DISTINCT] select_expr, select_expr, ...
FROM table_reference       -- 从什么表查
[WHERE where_condition]   -- 过滤
[GROUP BY col_list]        -- 分组查询
[HAVING col_list]          -- 分组后过滤
[ORDER BY col_list]        -- 排序
[CLUSTER BY col_list
| [DISTRIBUTE BY col_list] [SORT BY col_list]
]
[LIMIT number]                -- 限制输出的行数
-- 部门编号 部门名称 部门位置id
-- dept
10	行政部	1700
20	技术部	1800
30	教学部	1900
40	实训部	1900
-- 员工编号 姓名 岗位    薪资  部门
-- emp
10001	A	技术部	8000.00	30
10002	B	技术部	16000.00	20
10003	C	行政部	3500.00	10
10004	D	实训部	7000.00	40
10005	E	技术部	12000.00	30
10006	F	技术部	28000.00	30
10007	G	\N	24000.0	30
10008	H	行政部	3000.00	10
10009	I	实训部	5000.00	40
10010	J	实训部	7500.00	40
10011	K	行政部	4000.00	10
10012	L	教学部	30000.00	30
10013	M	行政部	3000.00	10
10014	N	教学部	13000.00	30


create database dm_db;

create table dept(
    deptno int,    -- 部门编号
    dname string,  -- 部门名称
    loc int        -- 部门位置
)
row format delimited fields terminated by '\t';

create table emp(
    empno int,      -- 员工编号
    ename string,   -- 员工姓名
    job string,     -- 员工岗位
    sal double,     -- 员工薪资
    deptno int      -- 部门编号
)
row format delimited fields terminated by '\t';
2.1 基本查询
● 全表及列查询
select * from dept;
select * from emp;
-- sql语言大小写不敏感
select 
  deptno,
  dname,
  loc
from dept;
● 列别名
-- 取别名的好处，便于计算。
select 
  deptno,
  dname as name,
  loc
from dept;


● limit语句
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
● where语句
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
● 关系运算函数
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
● 逻辑运算函数
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
● 聚合函数
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
from emp;

2.2 分组
● Group By语句
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

● Having语句
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


2.3 Join语句
● 等值Join
-- hive 只支持等值连接，不支持非等值连接


-- 根据员工表和部门表中的部门编号相等，查询员工编号、员工名、部门名
select
  e.empno,
  e.ename,
  d.dname
from emp e
join dept d
on e.deptno=d.deptno;

● 表的别名
-- 简化sql
-- 区分字段来源
● 内连接
-- 只有进行连接的两个表中都存在与连接条件相匹配的数据才会被保留下来
select
  e.empno,
  e.ename,
  d.dname
from emp e
join dept d
on e.deptno=d.deptno;

● 左外连接
-- join操作符左边表中符合where子句的所有记录将会被返回。
select
  e.empno,
  e.ename,
  d.dname
from emp e
left join dept d
on e.deptno=d.deptno;
● 右外连接
-- join操作符右边表中符合where子句的所有记录将会被返回
select
  e.empno,
  e.ename,
  d.dname
from emp e
right join dept d
on e.deptno=d.deptno;
● 全外连接
-- 返回所有表中符合where语句条件的所有记录，如果任一表的指定字段没有符合条件的值，那么就使用null值替代
select
  e.empno,
  e.ename,
  d.dname
from emp e
full join dept d
on e.deptno=d.deptno;



● 多表连接
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

● 笛卡尔集
-- 省略连接条件
-- 连接条件无效
-- 表中所有行互联

select
  empno,
  dname
from
emp,dept;




● 联合（union & union all）
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
2.4 排序
● 全局排序（Order By）
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




● 每个Reduce内部排序（Sort By）
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
● 分区（Distribute By）
select *
from emp
distribute by deptno
sort by sal desc;
● 分区排序（Cluster By）
-- cluseter by 只能升序排，兼容distribute by 和 sort by的功能


select
  *
from emp
cluster by deptno;
3、函数
● 单行函数
  ○ 算术运算函数
    ■ + - * / % & ｜ ^ ～
select sal + 10 from emp;
  ○ 数值函数
    ■ round：四舍五入
    ■ ceil：向上取整
    ■ floor：向下取整
select round(3.1415926);
select ceil(3.14);
select floor(3.5);

select
  round(avg(sal),2) as avg_sal
from emp;
  ○ 字符串函数
    ■ substring：截取字符串
-- 语法1：substring（string A,int start） 返回值string
-- 说明：返回字符串A 从start位置到结尾的字符串
select substring('Hadoop',3);
select substring('Hadoop',-3);
-- 语法2：substring（string A,int start，int len） 返回值string
-- 说明：返回字符串A从start位置开始，长度为len的字符串
select substring('lanzhishujiaxueyuanllinxu',7,13);
    ■ replace ：替换
-- 语法：replace(string A,string B,string C)   返回值string
-- 说明：将字符串A子字符串B替换为C
select replace('lanzhishujiaxueyuan','xueyuan','daxue');
    ■ regexp_replace：正则替换
-- 语法：regexp_replace(string A,string B,string C)   返回值string
-- 说明：将字符串中A符合正则表达式B的部分替换为C（在某些情况下需要转义）
select regexp_replace('100-200','(\\d+)','num');
    ■ regexp：正则匹配
-- 语法：string A  regexp '正则表达式'  返回值：boolean
-- 说明：如果字符串符合正则表达式，则返回true，否则false
select 'abcdttthhhj' regexp 'ct+';
    ■ repeat：重复字符串
-- 语法：repeat(string A, int n)返回值string
-- 说明：将字符串A 重复n遍

select repeat('数加学院',3);

    ■ split ：字符串切割
-- 语法：split(string str,string pat)返回值array
-- 说明：按正则表达式pat匹配到的内容分割str，分割后的字符串，以数组的形式进行返回。


select split('h-a-d-o-o-p','-');
    ■ nvl ：替换null值
-- 语法：nvl(A,B)
-- 说明：如果A的值不为null，则返回A，否则返回B
select nvl(null,1);
    ■ concat ：拼接字符串
-- 语法：concat(String A,String B,String C,......)   返回值string
-- 说明：将字符串ABC...进行拼接为一个字符串


select concat('anhui','-hefei','-shujiaxueyuan');
    ■ concat_ws：以指定分隔符拼接字符串或者字符串数组
-- 语法：concat_ws（String A,String... | array（string））  返回值string
-- 说明：使用分隔符A拼接多个字符串，或者一个数组的所有元素

select concat_ws('-','2025','06','13');
select concat_ws('-',array('2025','06','14'));
    ■ get_json_object：解析json字符串
-- 语法：get_json_object（string json_string,string path）返回值string
-- 说明：解析json字符串 json_string,返回path指定的内容，如果输入的json字符串错误，则返回NULL


select get_json_object('{"name":"zhangsan","friends":["zhangsan1", "zhangsan2"],"students":{"lisi1":20,"lisi2":22},"address":{"street":"shushanqu","city":"hefei","code":230001}}','$.students.lisi1')

  ○ 日期函数
    ■ unix_timestamp：返回当前或指定时间的时间戳
-- 语法：unix_timestamp()
-- 返回值：bigint
-- 说明：前面是日期后面是值日期传进来的格式
select unix_timestamp('2025/06/14 09-21-15','yyyy/MM/dd HH-mm-ss')
    ■ from_unixtime：转化UNIX时间戳（从 1970-01-01 00:00:00 UTC 到指定时间的秒数）到当前时区的时间格式
-- 语法：from_unixtime(bigint unixtime[,string format])
-- 返回值：string类型
select from_unixtime(1749863973,'yyyy/MM/dd');
    ■ current_date：当前日期
select current_date;  -- 返回的内容：年月日
    ■ current_timestamp：当前的日期加时间，并且精确的毫秒
select current_timestamp;
    ■ month：获取日期中的月
-- 语法：month(string date)
-- 返回值： int

select month('2025-06-14 9:28:50');
    ■ day：获取日期中的日
-- 语法：day(string date)
-- 返回值： int

select day('2025-06-14 9:28:50');
    ■ hour：获取日期中的小时
-- 语法：hour(string date)
-- 返回值： int

select hour('2025-06-14 09:28:50');
    ■ datediff：两个日期相差的天数（结束日期减去开始日期的天数）
-- 语法：datediff(string enddate,string startdate);
-- 返回值 int


select datediff('2025-06-14','2025-04-14');  -- 学习的天数
    ■ date_add：日期加天数
-- 语法：date_add(string startdate,int days)
-- 返回值 string类型
-- 说明：返回开始日期startdate增加days天后的日期

select date_add('2025-06-14',2);


    ■ date_sub：日期减天数
-- 语法：date_sub(string startdate,int days)
-- 返回值 string类型
-- 说明：返回开始日期startdate减少days天后的日期

select date_sub('2025-06-14 09:28:50',2)
    ■ date_format:将标准日期解析成指定格式字符串
select date_format('2025-06-14 09:28:50','yyyy年MM月dd日 HH时间mm分ss秒');
  ○ 流程控制函数
    ■ case when：条件判断函数
-- 语法：case when a then b [when c then d]* [else e] end
-- 返回值 : T
-- 说明：如果a为true则返回b，如果c为true则返回d，否则返回e



select case when 1=2 then 'zhangsan'
            when 2=2 then 'lisi' 
       else 'shujia' end  
from students;


-- 语法2 case a when b then c [when d then e]* [else f] end
-- 返回值 : T
-- 说明：如果a=b，那么返回c ；如果a=d，那么返回e    否则 返回f


select case 100 when 50 then 'zhangsan' when 100 then 'shujia' else 'lanzhi' end ,
  id,
  name
from students
limit 5;

    ■ if: 条件判断
-- 语法：if [boolean testCondition,T valueTrue,T valueFalseOrNull]
-- 返回值：T
-- 说明：当条件testCondition为true时，则返回valueTrue；否则返回valueFalseOrNull

// (a>b)?a:b
-- 条件满足，输出正确
select if(10 > 5,'正确','错误');

select if(10 < 5,'正确','错误');
  ○ 集合函数
    ■ size：集合中元素的个数
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

    ■ map：创建map集合
-- 语法：map(key1,value1,key2,value2,....)
-- 说明：根据输入的key和value构建map类型   kv对

select map('name','zhangsan','age',18);

--  结果{"name":"zhangsan","age":"18"}
    ■ map_keys： 返回map中的key
select map_keys(map('name','zhangsan','age',18));
-- 结果 ["name","age"]
    ■ map_values: 返回map中的value
select map_values(map('name','zhangsan','age',18));

-- 结果["zhangsan","18"]
    ■ array 声明array集合
-- 语法：array(value1,value2,...)
-- 说明：根据输入的参数构建数组array类

select array(1,2,3,4,5);
select array('1','2','3','4');
    ■ array_contains: 判断array中是否包含某个元素
select array_contains(array('1','2','3','4'),'4');
    ■ sort_array：将array中的元素排序
select sort_array(array('a','d','A','b'));  -- 不支持倒叙 只支持升序
    ■ struct声明struct中的各属性
-- 语法：struct(val1,val2,val3,....)
-- 说明：根据输入的参数构建结构体 struct类



select struct('name','age','sex');


    ■ named_struct声明struct的属性和值

-- 声明结构体的属性和值
select named_struct('name','zhangsan','age',18)
● 窗口函数
-- 窗口函数，能为每行数据划分一个窗口，然后对窗口范围内的数据进行计算，最后将计算结果返回给该行数据。


-- 语法：串口函数的语法主要包括“窗口”和“函数”两个部分，其中窗口用于定于计算范围的，函数用于定义计算逻辑的。


select
  id,
  name,
  sex,
  score,
  函数(score) over (窗口范围) as total_age   -- 窗口函数
from students;


-- 函数：绝大多数聚合函数都可以配合窗口使用：max min sum count avg
-- 窗口：窗口的范围的定义分为两种类型，一种基于行的，一种基于值的。






-- 窗口范围基于行

sum(score) over()


--  order by[column]   rows between                       and                  



-- 窗口范围基于值

sum(score) over()


-- order by [column] range between                       and     

-- 窗口的分区
-- 定义窗口范围时，可以指定分区字段，每个分区单独划分窗口


-- 窗口函数的省略


-- over()中的三部分内容 partition by 、order by、 （rows | range） between xxx and xxx,
-- 这三部分内容全可以省略不写

-- partition by 省略不写，表示不分区
-- order by 省略不写，表示不排序
-- （rows | range） between xxx and xxx省略不写，则使用其默认值，默认值如：


-- 如果over（）中包含order by，则默认值为
range between unbounded preceding and current row
-- 如果over（）中不包含order by,则默认值为：
rows between unbounded preceding and unbounded following

  ○ 聚合函数
    ■ max：最大值
    ■ min：最小值
    ■ sum：求和
    ■ avg：平均值
    ■ count：计数
  ○ 跨行取值函数
    ■ lead和lag
    ■ first_value和last_value
  ○ 排名函数
    ■ rank 
    ■ dense_rank
    ■ row_number
● 自定义函数
  ○ UDF函数
  ○ UDAF函数
  ○ UDTF函数




# Spark SQL方言

## 1、CREATE语句

> spark sql完全兼容hive语法，同时有自己的语法

- csv

```sql
CREATE TABLE students_csv
(
    id STRING, 
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) 
USING CSV;

-- hive中不支持csv
hdfs dfs -put students.txt /data/bigdata/students_csv
```

- parquet

```sql
CREATE TABLE students_parquet
(
    id STRING, 
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) 
USING parquet
LOCATION '/data/students_parquet';

insert into students_parquet
select * from students_csv;
```

## 2、INSERT OVERWRITE DIRECTORY

> 将查询结果保存到目录中，可以是HDFS 可以说本地目录
> hive也支持

```sql
-- 结果保存到本地
INSERT OVERWRITE LOCAL DIRECTORY '/root/clazz_num'
select 
clazz,
count(1) as num
from 
bigdata.students_parquet
group by clazz;

-- 结果保存到HDFS
INSERT OVERWRITE DIRECTORY '/root/clazz_num'
select 
clazz,
count(1) as num
from 
bigdata.students_parquet
group by clazz;
```

## 3、HINTS

### 1、重分区

```sql
-- 产生小文件
-- 小文件带来的问题
-- 1、会增加namenode元数据管理的压力
-- 2、会影响计算的效率，会产生很多task
create table students_repartition as 
select /*+ REPARTITION(100) */ * from students_parquet;


-- COALESCE：只能用于减少分区，不会产生shuffle
-- COALESCE：主要用于合并小文件
select /*+ COALESCE(3) */  * from students_repartition;

-- REPARTITION: 可以用于增加分区或者减少fen'q
select /*+ REPARTITION(3) */  * from students_repartition;
```

### 2、map join

> 将小表加到Driver的内存中，广播到Executor中进行关联，在map端进行关联，不会产生shuffle
> map join适合大表关联小表，小表的数据量控制在100M内

```sql
# 急用自动触发map join,
# 默认是10M
set spark.sql.autoBroadcastJoinThreshold=1kb;

# 手动触发map join
# MAPJOIN，BROADCAST，BROADCASTJOIN
select /*+ MAPJOIN(b) */ * from 
scores as a
join
students as b
on a.id=b.id;
```

## 4、缓存

> 当同一个表被多次使用时，可以将表的数据缓存起来

```sql
select 
clazz,
count(1) as num
from 
bigdata.students
group by clazz;

-- 缓存表
cache table bigdata.students;

-- 指定缓存级别进行缓存
-- MEMORY_AND_DISK_SER：先放内存，内存放不下再放磁盘，并且压缩
cache table bigdata.students OPTIONS ('storageLevel' 'MEMORY_AND_DISK_SER');

-- 清除缓存
uncache table  bigdata.students;

-- 缓存中间结果
CACHE TABLE students_filter OPTIONS ('storageLevel' 'DISK_ONLY')
select * from 
bigdata.students
where sex ='1';

-- 删除视图
drop view students_filter;

select 
clazz,
count(1) as num
from 
students_filter
group by clazz;

-- 清空缓存
CLEAR CACHE;

-- 刷新缓存
REFRESH TABLE bigdata.students;
```

## 5、Spark SQL DAG

```sql
-- 在spark sql中两次shuffle中间结果不需要落地
-- 在mapreduce中，前一个mapredceu执行结束之后需要将结果保存到HDFS再进行下一次mapreduce
select num,count(1) as num from(
    select 
    clazz,
    count(1) as num
    from 
    bigdata.students
    group by clazz
) as a
group by num;

-- spark sql 比hive 快的原因
-- 1、缓存
-- 2、DAG
-- 3、spark是粗粒度资源调度
```


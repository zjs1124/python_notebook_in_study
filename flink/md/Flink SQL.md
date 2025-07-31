Flink SQL

## 1、sql命令行

```sql
# 启动flink 会话集群
yarn-session.sh -d

# 进入sql命令行
sql-client.sh

# 创建动态表
CREATE TABLE students (
    id STRING,
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'students',
    'properties.bootstrap.servers' = 'master:9092',
    'properties.group.id' = 'testGroup',
    'scan.startup.mode' = 'latest-offset',
    'format' = 'csv'
);

# 统计
select clazz,count(1) as num
from students
group by clazz
```

## 2、命令行输出模式

### 1、**表格模式**

> 只保留最终的计算结果

```shell
SET 'sql-client.execution.result-mode' = 'table';
```

### 2、**变更日志模式**

> 显示计算过程

```shell
SET 'sql-client.execution.result-mode' = 'changelog';
```

### 3、**Tableau模式**

> 显示计算过程,不会打开新的窗口

```shell
SET 'sql-client.execution.result-mode' = 'tableau';
```

## 3、流批一体
同一个代码既可以做流处理，也可以做批处理称为流批一体。

### 1、流处理

> 1、流处理底层是持续流模型，所有的task同时启动，等待数据到达，来一条数据处理一条数据
> 2、持续输出结果，包括中间的计算结果
> 3、可以用于处理有界流和无界流

```sql
SET 'execution.runtime-mode' = 'streaming';

# 无界流
CREATE TABLE students_hdfs_stream (
    id STRING,
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) WITH (
    'connector' = 'filesystem',           -- 必选：指定连接器类型
    'path' = 'hdfs://master:9000/data/students',  -- 必选：指定路径
    'format' = 'csv',                     -- 必选：文件系统连接器指定 format
    'csv.field-delimiter' = ',',
    'source.monitor-interval' = '5000' -- 每隔一段时间扫描目录下新的文件，、
);

select clazz,count(1) as num
from students_hdfs_stream
group by clazz;
```

### 2、批处理

> 1、底层是mapreduce模型，先执行map task再执行reduce task
> 2、输出最终结果
> 3、只能用于处理有界流,不能用于处理无界流

```sql
SET 'execution.runtime-mode' = 'batch';

# 有界流
CREATE TABLE students_hdfs (
    id STRING,
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) WITH (
    'connector' = 'filesystem',           -- 必选：指定连接器类型
    'path' = 'hdfs://master:9000/data/students',  -- 必选：指定路径
    'format' = 'csv', -- 建表语句字段和顺序需要和数据顺序一致
    'csv.field-delimiter' = ','
);


select clazz,count(1) as num
from students_hdfs
group by clazz;
```

## 4、HINT与动态表
提示，/*+ 参数*/ sql语句或者代码会读取提示中的参数,并且执行。

### 1、动态表参数

>扩展(动态表):动态表是一个逻辑概念，是一个执行给定的sql语句，数据不断变化的虚拟表。

>动态表中不存储数据，只存储sql逻辑。

>处理方式:通过sql的create语句将流包装成动态表，在通过select等语句进行查询等，将得到的结果再更新或者追加到动态结果表中，并且回流。

> 在对动态表的连续查询下,结果表的状态或者计算代价可能会越来越高，当到一定的程度时，会停止连续查询。这时就可以通过添加限制来限制计算代价和状态大小来长期运行连续查询。比如添加where等限制条件来限定查询的条数来限制代价的大小。
```sql
# 批处理
SET 'execution.runtime-mode' = 'batch';
select clazz,count(1) as num
from students_hdfs
group by clazz;

# 流处理
SET 'execution.runtime-mode' = 'streaming';
select clazz,count(1) as num
from students_hdfs /*+options('source.monitor-interval' = '5000')*/
group by clazz;
```

## 5、连接器

### 1、kafka

#### 1、kafka source

```sql
-- kafka source表(无界流)
CREATE TABLE students_json (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    ts TIMESTAMP_LTZ(3) METADATA FROM 'timestamp' -- 数据写入kafka的时间，
) WITH (
  'connector' = 'kafka',
  'topic' = 'students_partition_age',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json' -- flink自动解析，按名称映射
);

select * from students_json;
```

#### 2、kafka sink

```sql
# 1、将仅追加的结果流写入kafka
-- kafka sink表
CREATE TABLE students_kafka_sink(
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'students_kafka_sink',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'csv' -- flink自动解析，按名称映射
);

-- 将查询结果写入kafka sink表 
insert into students_kafka_sink
select id,name,age,gender,clazz
from students_json
where clazz='文科一班';

-- 查看结果
select * from students_kafka_sink;
kafka-console-consumer.sh --bootstrap-server master:9092 --from-beginning --topic students_kafka_sink

# 2、将更新更改的结果流写入kafka
CREATE TABLE clazz_num_sink(
    clazz STRING,
    num BIGINT
) WITH (
  'connector' = 'kafka',
  'topic' = 'clazz_num_sink',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'canal-json' -- debezium-json,canal-json（将数据编程更新更改的流写入kafka,在每条数据上增加操作类型标记）
);

insert into clazz_num_sink
select clazz,count(1) as num
from students_json
group by clazz;

-- 查看结果
kafka-console-consumer.sh --bootstrap-server master:9092 --from-beginning --topic clazz_num_sink
-- clazz_num_sink是一个更新更改的表
select * from clazz_num_sink;
```

### 2、MySQL

#### 1、mysql source

```sql
-- 创建mysql source表（有界流）
CREATE TABLE students_jdbc (
    id STRING,
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://master:3306/shujia',
    'table-name' = 'student',
    'username' = 'root',
    'password' = '123456'
);

SET 'execution.runtime-mode' = 'batch';

select clazz,count(1) as num
from students_jdbc
group by clazz;
```

#### 2、mysql sink

```sql
-- 1、将仅追加的结果流写入mysql
SET 'execution.runtime-mode' = 'streaming';

insert into students_jdbc
select 
id,name,age,gender as sex,clazz
from students_json;


-- 2、将更新更改的结果流写入mysql

-- 在mysql中创建表
CREATE TABLE clazz_num (
    clazz varchar(20),
    num BIGINT,
    PRIMARY KEY (clazz) -- flink在写入数据时会按照主键进行更新
);

-- 创建mysql sink表
CREATE TABLE clazz_num (
    clazz STRING,
    num BIGINT,
    PRIMARY KEY (clazz) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://master:3306/shujia',
    'table-name' = 'clazz_num',
    'username' = 'root',
    'password' = '123456'
);

insert into clazz_num
select clazz,count(1) as num
from students_json
group by clazz;
```

### 3、HDFS

#### 1、hdfs source

```sql
-- 1、有界流的方式读取hdfs
CREATE TABLE students_hdfs (
    id STRING,
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) WITH (
    'connector' = 'filesystem',           -- 必选：指定连接器类型
    'path' = 'hdfs://master:9000/data/students',  -- 必选：指定路径
    'format' = 'csv', -- 建表语句字段和顺序需要和数据顺序一致
    'csv.field-delimiter' = ','
);

SET 'execution.runtime-mode' = 'batch';
select clazz,count(1) as num
from students_hdfs
group by clazz;


-- 2、无界流的方式读取hdfs
SET 'execution.runtime-mode' = 'streaming';
select clazz,count(1) as num
from students_hdfs /*+options('source.monitor-interval' = '5000')*/ -- 监听目录
group by clazz;
```

#### 2、hdfs sink

```sql
-- 1、批处理方式写入hdfs（hive ,spark sql）
CREATE TABLE clazz_num_hdfs (
    clazz STRING,
    num BIGINT
) WITH (
    'connector' = 'filesystem',           -- 必选：指定连接器类型
    'path' = 'hdfs://master:9000/data/clazz_num_hdfs',  -- 必选：指定路径
    'format' = 'json'
);

SET 'execution.runtime-mode' = 'batch';

insert overwrite clazz_num_hdfs
select clazz,count(1) as num
from students_hdfs
group by clazz;

-- 查看结果
# hdfs dfs -cat /data/clazz_num_hdfs/*
select * from clazz_num_hdfs;


-- 2、流式写入hdfs
-- 一、将仅追加的结果流写入hdfs
CREATE TABLE students_filter (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING
) WITH (
    'connector' = 'filesystem',           -- 必选：指定连接器类型
    'path' = 'hdfs://master:9000/data/students_filter',  -- 必选：指定路径
    'format' = 'csv', -- 建表语句字段和顺序需要和数据顺序一致
    'csv.field-delimiter' = ','
);
SET 'execution.runtime-mode' = 'streaming';
insert into students_filter
select id,name,age,gender,clazz from students_json
where age > 23;

-- 可以实时查询结果表
select * from students_filter /*+options('source.monitor-interval' = '5000')*/;

-- 二、将更新的结果流写入hdfs

CREATE TABLE clazz_num_stream_hdfs (
    clazz STRING,
    num BIGINT
) WITH (
    'connector' = 'filesystem',           -- 必选：指定连接器类型
    'path' = 'hdfs://master:9000/data/clazz_num_stream_hdfs',  -- 必选：指定路径
    'format' = 'canal-json',
    'sink.rolling-policy.file-size' = '128M', -- 滚动前文件最大大小
    'sink.rolling-policy.rollover-interval' = '30 min' -- 滚动的间隔时间
);

insert into clazz_num_stream_hdfs
select clazz,count(1) as num
from students_json
group by clazz;

-- 查看结果
hdfs dfs -cat /data/clazz_num_stream_hdfs/*
```

### 4、DataGen

> 用于高性能测试，测试flink任务的吞吐量

```sql
CREATE TABLE students_datagen (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING
) WITH (
    'connector' = 'datagen',
    'rows-per-second'='5', -- 每秒生成的数据行数
    'fields.id.length'='10',
    'fields.name.length'='2',
    'fields.age.min'='1',
    'fields.age.max'='100',
    'fields.gender.length'='1',
    'fields.clazz.length'='4'
);
```

### 5、Print

```sql
CREATE TABLE print_table (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING
) WITH (
 'connector' = 'print'
);

-- LIKE ： 继承原表的字段创建新的表
CREATE TABLE print_table WITH ('connector' = 'print')
LIKE students_datagen (EXCLUDING ALL);

insert into print_table
select * from students_datagen;
```

### 6、BlackHole 

> 用于高性能测试

```sql
CREATE TABLE blackhole_table WITH ('connector' = 'blackhole')
LIKE students_datagen (EXCLUDING ALL);

insert into blackhole_table
select * from students_datagen;


-- 测试flink集群性能

CREATE TABLE blackhole_table_clazz_num (
    clazz STRING,
    num BIGINT
) WITH (
  'connector' = 'blackhole'
);

insert into blackhole_table_clazz_num
select clazz,count(1) as num
from students_datagen /*+options('rows-per-second'='5000')*/
group by clazz;
```

### 7、Hive

#### 1、hive catalog

> flink通过catalog可以读取hive中的表，也可以将元数据保存到hive的元数据中
>
> catalog ---> database --> table ---> 字段---> 数据

```sql
CREATE CATALOG hive_catalog WITH (
    'type' = 'hive',
    'default-database' = 'default',
    'hive-conf-dir' = '/usr/local/soft/hive-3.1.3/conf'
);

# default_catalog: flink默认的元数据，元数据保存在当前会话的内存中
show catalogs;

-- 切换元数据
USE CATALOG hive_catalog;

show databases;

-- 查询hive中的表
select * from hive_catalog.dws.dws_grid_stay_d_i limit 100;

-- 创建数据库
create database flink;
use flink;
-- 创建flink动态表
CREATE TABLE students_json (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    ts TIMESTAMP_LTZ(3) METADATA FROM 'timestamp' -- 数据写入kafka的时间，
) WITH (
    'connector' = 'kafka',
    'topic' = 'students_partition_age',
    'properties.bootstrap.servers' = 'master:9092',
    'properties.group.id' = 'testGroup',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json' -- flink自动解析，按名称映射
);

-- 在flink中查询数据
-- 在hive不能查询，因为hive不兼容flink的sql语句
select * from students_json ;
```

#### 2、hive fucntions

```sql
-- 加载hive的函数
LOAD MODULE hive WITH ('hive-version' = '3.1.3');


select split('java,flink,spark',',');

-- wordcount
kafka-console-producer.sh --broker-list master:9092 --topic words
flink,python.spark
hadoop,flink,hive,java

CREATE TABLE words (
    line STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'words',
    'properties.bootstrap.servers' = 'master:9092',
    'properties.group.id' = 'testGroup',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'csv',
    'csv.field-delimiter'='|'
);

select word ,count(1) as num
from words,
LATERAL TABLE(explode(split(line,','))) t(word)
group by word;
```

### 8、clickhouse

#### 1、clickhouse sink

```sql
-- 在ck中创建表
CREATE TABLE dws.students (
    id String,
    name String,
    age UInt32,
    gender String,
    clazz String
)ENGINE = MergeTree()
order by(id);

-- 在flink中创建表
CREATE TABLE students_ck (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    PRIMARY KEY (`id`) NOT ENFORCED
) WITH (
    'connector' = 'clickhouse',
    'url' = 'jdbc:ch://master:8123',
    'database-name' = 'dws',
    'table-name' = 'students',
    'sink.batch-size' = '500',
    'sink.flush-interval' = '1000',
    'sink.max-retries' = '3'
);


insert into students_ck
select id,name,age,gender,clazz
from students_json;
```

## 6、时间属性

### 1、事件时间

```sql
CREATE TABLE cars (
    car STRING,
    city_code STRING,
    county_code STRING,
    card BIGINT,
    camera_id STRING,
    orientation STRING,
    road_id BIGINT,
    `time` BIGINT,
    speed DOUBLE,
    user_action_time as TO_TIMESTAMP(FROM_UNIXTIME(`time`)), -- 动态增加新的字段
    WATERMARK FOR user_action_time AS user_action_time - INTERVAL '5' SECOND -- 设置时间字段和水位线
) WITH (
  'connector' = 'kafka',
  'topic' = 'cars',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'json' -- flink自动解析，按名称映射
);
```

### 2、处理时间

```sql
-- 使用PROCTIME函数声明时间字段
CREATE TABLE words_proctime (
    line STRING,
    user_action_time AS PROCTIME() -- 声明一个额外的列作为处理时间属性
) WITH (
    'connector' = 'kafka',
    'topic' = 'words',
    'properties.bootstrap.servers' = 'master:9092',
    'properties.group.id' = 'testGroup',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'csv',
    'csv.field-delimiter'='|'
);

-- 加载hive的函数
LOAD MODULE hive WITH ('hive-version' = '3.1.3');

select 
    word ,
    TUMBLE_START(user_action_time, INTERVAL '5' SECOND) as win_start,
    TUMBLE_END(user_action_time, INTERVAL '5' SECOND) as win_end,
    count(1) as num
from words_proctime,
LATERAL TABLE(explode(split(line,','))) t(word)
group by 
    word,
    TUMBLE(user_action_time, INTERVAL '5' SECOND);
```

## 7、DQL

### 1、with

> 当一段代码逻辑被重复使用时，可以定义到with子句中，减少代码量

```sql
with tmp as(
    select * from students_json
    where clazz='文科一班'
)
select * from tmp
union all 
select * from tmp;
```

### 2、distinct

```sql
-- flink的distinct会将数据保存在状态中，状态可能会越来越大，状态太大会导致内存放不下，也可能会导致checkpoint超时
select distinct id,name,age,gender,clazz from students_json;
```

### 3、row_number去重

```sql
-- 使用row_number去重，状态中只需要保存partition by后面字段的值，不需要保存其他字段
CREATE TABLE students_proctime (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    proctime as PROCTIME()
) WITH (
  'connector' = 'kafka',
  'topic' = 'students_partition_age',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json' -- flink自动解析，按名称映射
);

select * from (
    select *,
    row_number() over(partition by id order by proctime asc) as r
    from students_proctime
) as a
where r =1;
```

### 4、窗口表值函数

#### 1、滚动窗口

```sql
CREATE TABLE Bid (
    bidtime  TIMESTAMP(3),
    price  DECIMAL(10, 2),
    item  STRING,
    WATERMARK FOR bidtime AS bidtime
) WITH (
  'connector' = 'kafka',
  'topic' = 'bid',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv' -- flink自动解析，按名称映射
);
kafka-console-producer.sh --broker-list master:9092 --topic bid
2020-04-15 08:05:00,4.00,C
2020-04-15 08:07:00,2.00,A
2020-04-15 08:09:00,5.00,D
2020-04-15 08:11:00,3.00,B
2020-04-15 08:13:00,1.00,E
2020-04-15 08:17:00,6.00,F

-- TUMBLE函数会在原表的基础上增加window_start，window_end，window_time
-- TUMBLE 函数有三个必传参数，一个可选参数：
-- TUMBLE(TABLE data,DESCRIPTOR(timecol),size[,offset])
-- data:拥有时间属性的列的表
-- timecol:列描述符,决定数据的那个时间属性应该映射到窗口
-- size:窗口的大小
SELECT * FROM TABLE(
   TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES)
);
-- 
-- 再分组聚合
SELECT 
    item,
    window_start,
    window_end,
    avg(price) as avg_price
FROM TABLE(
   TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES)
)
group by item,window_start,window_end;

-- 全局窗口
-- 全局窗口会将窗口内所有的数据都发送到下游相同的task中进行计算，会影响计算的吞吐量
SELECT 
    window_start,
    window_end,
    avg(price) as avg_price
FROM TABLE(
   TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES)
)
group by window_start,window_end;
```

#### 2、滑动窗口

```sql
-- 在原表的基础上增加window_start，window_end，window_time
-- HOP滑动窗口函数的参数如下
-- HOP(TABLE data, DESCRIPTOR(timecol), slide, size [, offset ])
SELECT * FROM TABLE(
   HOP(TABLE Bid, DESCRIPTOR(bidtime),INTERVAL '5' MINUTES, INTERVAL '10' MINUTES)
);

-- 分组聚合
SELECT 
    item,
    window_start,
    window_end,
    avg(price) as avg_price
FROM TABLE(
   HOP(TABLE Bid, DESCRIPTOR(bidtime),INTERVAL '5' MINUTES, INTERVAL '10' MINUTES)
)
group by item,window_start,window_end;
```

#### 3、累积窗口

```sql
-- 在原表的基础上增加window_start，window_end，window_time
-- 累计窗口的参数如下
-- CUMULATE(TABLE data, DESCRIPTOR(timecol), step, size)
SELECT * FROM TABLE(
   CUMULATE(TABLE Bid, DESCRIPTOR(bidtime),INTERVAL '1' MINUTES, INTERVAL '10' MINUTES)
);

SELECT 
    item,
    window_start,
    window_end,
    count(1) as num
FROM TABLE(
     CUMULATE(TABLE Bid, DESCRIPTOR(bidtime),INTERVAL '1' MINUTES, INTERVAL '1' DAY)
)
group by item,window_start,window_end;
```

#### 4、会话窗口
两个数据之间间隔超过一定时间就不计算并关闭
```sql
2020-04-15 08:05:00,4.00,C
2020-04-15 08:05:10,4.00,C
2020-04-15 08:05:20,4.00,C
2020-04-15 08:05:30,4.00,C
2020-04-15 08:06:31,4.00,C
-- SESSION(TABLE data [PARTITION BY(keycols, ...)], DESCRIPTOR(timecol), gap)
select 
    item,
    SESSION_START(bidtime, INTERVAL '1' MINUTES) as window_start,
    SESSION_END(bidtime, INTERVAL '1' MINUTES) as window_end,
    count(1) as num
from 
Bid
group by 
    item,
    SESSION(bidtime, INTERVAL '1' MINUTES);
```

### 5、over函数
over函数中的order by 必须按照时间字段进行升序，否则计算代价会越来越大

```sql
CREATE TABLE orders (
    order_id STRING,
    order_time  TIMESTAMP(3),
    amount  DECIMAL(10, 2),
    product STRING,
    WATERMARK FOR order_time AS order_time
) WITH (
  'connector' = 'kafka',
  'topic' = 'orders',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv' -- flink自动解析，按名称映射
);
kafka-console-producer.sh --broker-list master:9092 --topic orders
001,2025-07-26 15:05:00,4.00,C
002,2025-07-26 15:07:00,2.00,C
002,2025-07-26 15:07:05,2.00,C
003,2025-07-26 15:09:00,5.00,C
003,2025-07-26 15:08:58,5.00,C
003,2025-07-26 15:10:00,5.00,C
004,2025-07-26 15:11:00,3.00,A
005,2025-07-26 15:13:00,1.00,A
006,2025-07-26 15:17:00,6.00,B
```

#### 1、聚合类

```sql
-- sum max min count avg

-- 流处理中的错误写法
-- 每来一条新的数据都需要重新计算数据的顺序，计算代价太大
select 
    order_id,
    order_time,
    amount,
    product,
    su
    m(amount) over(partition by product order by product) as sum_amount
from 
    orders;

-- 1、计算每个商品累积销售金额
-- 必须按照时间字段升序排序
select 
    order_id,
    order_time,
    amount,
    product,
    sum(amount) over(partition by product order by order_time asc) as sum_amount
from 
    orders;

-- 1、计算每个商品累积销售金额，计算最近两分钟
select 
    order_id,
    order_time,
    amount,
    product,
    sum(amount) over(
        partition by product 
        order by order_time asc
        RANGE BETWEEN INTERVAL '2' MINUTE PRECEDING AND CURRENT ROW -- 增加计算的时间边界
    ) as sum_amount
from 
    orders;

-- 1、计算每个商品累积销售金额，计算最近3条数据
select 
    order_id,
    order_time,
    amount,
    product,
    sum(amount) over(
        partition by product 
        order by order_time asc
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) as sum_amount
from 
    orders;
```

#### 2、排序类

```sql
-- 只能按照时间字段升序排序
select 
    order_id,
    order_time,
    amount,
    product,
    row_number() over(
        partition by product 
        order by order_time asc
    ) as r
from 
    orders;
    
-- 特殊情况 
-- 获取每个商品销售金额最高的前两个订单
-- 取top之后每一次计算的代价不会一直增加
-- 由于顺序会改变，所以计算的结果是一个更新更改的流
select * from(
    select 
        order_id,
        order_time,
        amount,
        product,
        row_number() over(
            partition by product 
            order by amount desc
        ) as r
    from 
        orders
) as a
where r <=2;
```

#### 3、取值类

```sql
-- 在流处理中只能使用lag，不能使用lead
select 
    order_id,
    order_time,
    amount,
    product,
    lag(amount,1) over(
        partition by product 
        order by order_time asc
    ) as lag_amount
from 
    orders;
```

### 6、模式检测（CEP）

#### 1、案例1

```sql
CREATE TABLE fraud (
    user_id STRING,
    price  DECIMAL(10, 2),
    event_time  TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time
) WITH (
  'connector' = 'kafka',
  'topic' = 'fraud',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv' -- flink自动解析，按名称映射
);

kafka-console-producer.sh --broker-list master:9092 --topic fraud
user001,100,2025-07-26 15:01:00
user001,20,2025-07-26 15:02:00
user001,0.1,2025-07-26 15:05:00
user001,0.5,2025-07-26 15:06:00
user001,0.3,2025-07-26 15:07:00
user001,700,2025-07-26 15:08:00
user001,100,2025-07-26 15:09:00
user001,100,2025-07-26 15:10:00

-- 对于一个账户，如果出现小于 $1 美元的交易后紧跟着一个大于 $500 的交易，就输出一个报警信息
select * from fraud
    MATCH_RECOGNIZE (
      PARTITION BY user_id
      ORDER BY event_time
      MEASURES -- 定义返回格式
        A.event_time as min_time,
        A.price as min_price,
        B.event_time as max_time,
        B.price as max_price
      PATTERN (A B) -- 定义规则,A,B代表的是一条数据的别名
      DEFINE -- 定义规则需要满足的条件
        A as price < 1,
        B as price > 500
    ) AS T;
 
 -- 对于一个账户，如果出现3次小于 $1 美元的交易后紧跟着一个大于 $500 的交易，就输出一个报警信息
 select * from fraud
    MATCH_RECOGNIZE (
      PARTITION BY user_id
      ORDER BY event_time
      MEASURES -- 定义返回格式
        A.event_time as last_time, -- 直接取是最后一个
        FIRST(A.price) as FIRST_price, -- 取第一行
        last(A.price) as last_price, -- 取最后一行
        avg(A.price) as avg_price, -- 取平均值
        B.event_time as max_time,
        B.price as max_price
      PATTERN (A{3} B) -- 定义规则,A,B代表的是一条数据的别名
      DEFINE -- 定义规则需要满足的条件
        A as price < 1,
        B as price > 500
    ) AS T;
    
-- 对于一个账户，如果出现多次小于 $1 美元的交易后紧跟着一个大于 $500 的交易，就输出一个报警信息
select * from fraud
    MATCH_RECOGNIZE (
      PARTITION BY user_id
      ORDER BY event_time
      MEASURES -- 定义返回格式
        A.event_time as last_time, -- 直接取是最后一个
        FIRST(A.price) as FIRST_price, -- 取第一行
        last(A.price) as last_price, -- 取最后一行
        avg(A.price) as avg_price, -- 取平均值
        B.event_time as max_time,
        B.price as max_price
      AFTER MATCH SKIP PAST LAST ROW  -- 在当前匹配成功后开始下一个匹配，同一条数据不会落到多个匹配中
      PATTERN (A{2,} B) -- 定义规则,A,B代表的是一条数据的别名
      DEFINE -- 定义规则需要满足的条件
        A as price < 1,
        B as price > 500
    ) AS T;
    
-- 对于一个账户，如果出现小于 $1 美元的交易后紧跟着一个大于 $500 的交易，就输出一个报警信息，需要在10秒内出现
user001,0.1,2025-07-26 15:07:02
user001,700,2025-07-26 15:07:06
user001,0.3,2025-07-26 15:07:10
user001,700,2025-07-26 15:07:22
select * from fraud
    MATCH_RECOGNIZE (
      PARTITION BY user_id
      ORDER BY event_time
      MEASURES -- 定义返回格式
        A.event_time as min_time,
        A.price as min_price,
        B.event_time as max_time,
        B.price as max_price
      PATTERN (A B) WITHIN INTERVAL '10' SECOND -- 增加时间限制
      DEFINE -- 定义规则需要满足的条件
        A as price < 1,
        B as price > 500
    ) AS T;
```

#### 2、案例2

```sql
CREATE TABLE Ticker (
    symbol STRING,
    rowtime  TIMESTAMP(3), 
    price  DECIMAL(10, 2),
    tax DECIMAL(10, 2),
    WATERMARK FOR rowtime AS rowtime
) WITH (
  'connector' = 'kafka',
  'topic' = 'ticker',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv' -- flink自动解析，按名称映射
);

kafka-console-producer.sh --broker-list master:9092 --topic ticker
ACME,2025-07-26 10:00:01,15,1
ACME,2025-07-26 10:00:02,17,2
ACME,2025-07-26 10:00:03,18,1
ACME,2025-07-26 11:00:04,15,3
ACME,2025-07-26 11:00:05,14,2
ACME,2025-07-26 11:00:06,12,1
ACME,2025-07-26 12:00:07,11,1
ACME,2025-07-26 12:00:08,14,2
ACME,2025-07-26 12:00:09,24,2
ACME,2025-07-26 13:00:12,25,2
ACME,2025-07-26 13:00:13,29,1

select * from Ticker
    MATCH_RECOGNIZE (
      PARTITION BY symbol
      ORDER BY rowtime
      MEASURES -- 定义返回格式
        A.price as a_price,
        A.rowtime as a_rowtime,
        last(B.price) as b_price,
        B.rowtime as b_rowtime,
        C.price as c_price,
        C.rowtime as c_rowtime
      AFTER MATCH SKIP PAST LAST ROW  -- 在当前匹配成功后开始下一个匹配，同一条数据不会落到多个匹配中
      PATTERN (A B+ C)
      DEFINE
        B as (last(B.price,1) is null and B.price < A.price) or (B.price < last(B.price,1)),
        C as C.price > B.price
    ) AS T;
```

### 7、Join

#### 1、Regular Joins

> 常规关联方式，和spark sql  hive 类似

```sql
CREATE TABLE students (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'students',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic students
1500100001,施笑槐,22,女,文科六班
1500100002,吕金鹏,24,男,文科六班
1500100003,单乐蕊,22,女,理科六班
1500100004,葛德曜,24,男,理科三班
1500100005,宣谷芹,22,女,理科五班
1500100006,边昂雄,21,男,理科二班

CREATE TABLE scores (
    sid STRING,
    cid STRING,
    score DOUBLE
) WITH (
  'connector' = 'kafka',
  'topic' = 'scores',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic scores
1500100001,1000001,98
1500100002,1000002,5
1500100001,1000003,137
1500100001,1000004,29
1500100001,1000005,85
1500100001,1000006,52
1500100002,1000001,139

-- 1、inner join
-- 使用常规的关联方式实现双流join，flink会将两个流表的数据一直保存在状态中，状态会越来越大
select a.id,a.name,b.cid,b.score from 
students as a
inner join
scores as b
on a.id=b.sid;

-- 2、left join
select a.id,a.name,b.cid,b.score from 
students as a
left join
scores as b
on a.id=b.sid;

-- 3、full join
select a.id,a.name,b.cid,b.score from 
students as a
full join
scores as b
on a.id=b.sid;


-- 解决状态不断增长的方式，可以让状态定时过期
-- 只关联5秒内的数据
SET 'table.exec.state.ttl' = '5000';

select a.id,a.name,b.cid,b.score from 
students as a
full join
scores as b
on a.id=b.sid;

select clazz,
count(1) as num from 
students
group by clazz;
```

#### 2、Interval Joins 

> 主要用于双流join

```sql
CREATE TABLE students_event_time (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time 
) WITH (
  'connector' = 'kafka',
  'topic' = 'students',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic students
1500100001,施笑槐,22,女,文科六班,2025-07-28 10:32:10
1500100002,吕金鹏,24,男,文科六班,2025-07-28 10:32:11
1500100003,单乐蕊,22,女,理科六班,2025-07-28 10:32:13
1500100004,葛德曜,24,男,理科三班,2025-07-28 10:32:16
1500100005,宣谷芹,22,女,理科五班,2025-07-28 10:32:20
1500100006,边昂雄,21,男,理科二班,2025-07-28 10:32:22

CREATE TABLE scores_event_time (
    sid STRING,
    cid STRING,
    score DOUBLE,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time 
) WITH (
  'connector' = 'kafka',
  'topic' = 'scores',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic scores
1500100001,1000001,98,2025-07-28 10:32:09
1500100002,1000002,5,2025-07-28 10:32:12
1500100001,1000003,137,2025-07-28 10:32:13
1500100001,1000004,29,2025-07-28 10:32:14
1500100001,1000005,85,2025-07-28 10:32:15
1500100001,1000006,52,2025-07-28 10:32:16
1500100002,1000001,139,2025-07-28 10:32:17


select a.id,a.name,b.cid,b.score 
from students_event_time a ,scores_event_time b
where a.id=b.sid
-- 学生表数据的时间需要在分数表数据时间之前参数，而在在5秒内，所以状态中只保留5秒内的数据
and  a.event_time BETWEEN b.event_time - INTERVAL '5' SECOND AND b.event_time;
```

#### 3、Temporal Joins

> 用于流表关联时态表

```sql
-- 订单表（事实表）（流表）
CREATE TABLE orders (
    order_id    STRING,
    price       DECIMAL(32,2),
    currency    STRING,
    order_time  TIMESTAMP(3),
    WATERMARK FOR order_time AS order_time 
) WITH (
  'connector' = 'kafka',
  'topic' = 'orders',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic orders
o_001,20,USD,2025-07-28 10:32:09
o_002,10,USD,2025-07-28 10:32:15
o_003,100,USD,2025-07-28 10:32:21

-- 汇率表（维度表）（时态表）
CREATE TABLE currency_rates (
    currency STRING,
    conversion_rate DECIMAL(32, 2),
    update_time TIMESTAMP(3) ,
    WATERMARK FOR update_time AS update_time,
    PRIMARY KEY(currency) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'currency_rates',
    'properties.bootstrap.servers' = 'master:9092',
    'properties.group.id' = 'testGroup',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'canal-json'
);
-- 写入汇率数据
insert into currency_rates
values
('USD',7.17,TIMESTAMP'2025-07-28 10:32:05'),
('USD',7.16,TIMESTAMP'2025-07-28 10:32:10'),
('USD',7.2,TIMESTAMP'2025-07-28 10:32:15'),
('USD',7.22,TIMESTAMP'2025-07-28 10:32:20');

-- 1、使用常规关联方式进行关联,会取最新的汇率
select order_id,price,order_time,conversion_rate,update_time from 
orders as a
left join
currency_rates as b
on a.currency=b.currency;

-- 2、使用时态表join
-- FOR SYSTEM_TIME AS OF a.order_time: 使用订单表的时间去汇率表中查询对应时段的数据
select order_id,price,order_time,conversion_rate,update_time from 
orders as a
left join
currency_rates  FOR SYSTEM_TIME AS OF a.order_time as b
on a.currency=b.currency;
```

#### 4、lookup join

> 用于流表关联维度表

```sql
 -- 流标（事实表）
CREATE TABLE scores (
    sid STRING,
    cid STRING,
    score DOUBLE,
    proctime as PROCTIME()
) WITH (
  'connector' = 'kafka',
  'topic' = 'scores',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic scores
1500100001,1000001,98
1500100002,1000002,5
1500100003,1000003,137
1500100001,1000004,29
1500100001,1000005,85
1500100001,1000006,52
1500100002,1000001,139

-- 维度表
CREATE TABLE students_jdbc (
    id STRING,
    name STRING,
    age INT,
    sex STRING,
    clazz STRING
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://master:3306/shujia',
    'table-name' = 'student',
    'username' = 'root',
    'password' = '123456'
);


-- 1、使用常规关联方式进行关联
-- mysql中的数据学生表flink只会启动的时候读取一次
-- 如果数据库数据更新了，flink不知道
-- flink会将两个表的数据一直保存在状态
select b.id,b.name,a.sid,a.score from 
scores as a
left join
students_jdbc as b
on a.sid=b.id;


-- 2、使用lookup join
-- 当流表每来一条数据，使用关联的字段到维表对应的数据库中查询最新的数据，
-- 问题：每一条数据都需要查询数据库，会影响flink任务的吞吐量
select b.id,b.name,a.sid,a.score from 
scores as a
left join
students_jdbc FOR SYSTEM_TIME AS OF a.proctime as b
on a.sid=b.id;

-- 优化方式：增加缓存
-- lookup.cache.max-rows: 最大缓存行数
-- lookup.cache.ttl：缓存过期时间
select b.id,b.name,a.sid,a.score from 
scores as a
left join
students_jdbc/*+options('lookup.cache.max-rows'='2','lookup.cache.ttl'='20000')*/ FOR SYSTEM_TIME AS OF a.proctime as b
on a.sid=b.id;
```

### 8、窗口关联

```sql
CREATE TABLE students_event_time (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time 
) WITH (
  'connector' = 'kafka',
  'topic' = 'students',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic students
1500100001,施笑槐,22,女,文科六班,2025-07-28 10:32:10
1500100002,吕金鹏,24,男,文科六班,2025-07-28 10:32:11
1500100003,单乐蕊,22,女,理科六班,2025-07-28 10:32:13
1500100004,葛德曜,24,男,理科三班,2025-07-28 10:32:16
1500100005,宣谷芹,22,女,理科五班,2025-07-28 10:32:20
1500100006,边昂雄,21,男,理科二班,2025-07-28 10:32:22

CREATE TABLE scores_event_time (
    sid STRING,
    cid STRING,
    score DOUBLE,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time 
) WITH (
  'connector' = 'kafka',
  'topic' = 'scores',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic scores
1500100001,1000001,98,2025-07-28 10:32:09
1500100002,1000002,5,2025-07-28 10:32:12
1500100001,1000003,137,2025-07-28 10:32:13
1500100001,1000004,29,2025-07-28 10:32:14
1500100001,1000005,85,2025-07-28 10:32:15
1500100001,1000006,52,2025-07-28 10:32:16
1500100002,1000001,139,2025-07-28 10:32:17
1500100001,1000001,139,2025-07-28 10:32:21

-- 在相同的窗口内进行关联
select a.id,a.name,b.cid,b.score from 
(
    SELECT * FROM TABLE(
       TUMBLE(TABLE students_event_time, DESCRIPTOR(event_time), INTERVAL '10' SECOND)
    )
) as a
full join
(
    SELECT * FROM TABLE(
       TUMBLE(TABLE scores_event_time, DESCRIPTOR(event_time), INTERVAL '10' SECOND)
    )
) as b
on a.id=b.sid 
and a.window_start=b.window_start and a.window_end=b.window_end;
```

### 9、order by 

```sql
CREATE TABLE students_event_time (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time 
) WITH (
  'connector' = 'kafka',
  'topic' = 'students',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'csv'
);
kafka-console-producer.sh --broker-list master:9092 --topic students
1500100001,施笑槐,22,女,文科六班,2025-07-28 10:32:10
1500100002,吕金鹏,24,男,文科六班,2025-07-28 10:32:10
1500100003,单乐蕊,22,女,理科六班,2025-07-28 10:32:10
1500100004,葛德曜,24,男,理科三班,2025-07-28 10:32:16
1500100005,宣谷芹,22,女,理科五班,2025-07-28 10:32:20
1500100006,边昂雄,21,男,理科二班,2025-07-28 10:32:22
1500100006,边昂雄,27,男,理科二班,2025-07-28 10:32:22

-- 2、流处理中必须按照时间属性升序排序
select * from 
students_event_time
order by event_time,age;

-- 特殊情况，取limit
select * from 
students_event_time
order by age
limit 5;
```

## 8、Checkpoint

vim clazz_num.sql

```sql
-- 创建source 表
CREATE TABLE students (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'students',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset', -- 如果从快照恢复任务，会从上一次消费的位置读取数据
  'format' = 'csv'
);

-- 创建sink表
CREATE TABLE print_table (
    clazz STRING,
    num BIGINT
) WITH (
 'connector' = 'print'
);

-- 指定sql 任务恢复的checkpoint位置
-- SET 'execution.savepoint.path' = 'hdfs://master:9000/flink/checkpoints/317786eb97f590664f9150e727d68006/chk-7';

insert into print_table
select clazz,count(1) as num
from 
students
group by clazz;
```

- 提交任务

```shell
# 1、第一次直接提交任务
sql-client.sh -f  clazz_num.sql

# 2、重启任务增加execution.savepoint.path重启
sql-client.sh -f  clazz_num.sql 
sql-client.sh -f  clazz_num.sql  -D execution.savepoint.path=hdfs://master:9000/flink/checkpoints/317786eb97f590664f9150e727d68006/chk-7

kafka-console-producer.sh --broker-list master:9092 --topic students
1500100001,施笑槐,22,女,文科六班
1500100002,吕金鹏,24,男,文科六班
1500100003,单乐蕊,22,女,理科六班
1500100004,葛德曜,24,男,理科三班
1500100005,宣谷芹,22,女,理科五班
1500100006,边昂雄,21,男,理科二班
```

## 9、sql-client.sh -i

> 进行sql命令前执行初始化sql

vim init.sql

```sql
CREATE CATALOG hive_catalog WITH (
    'type' = 'hive',
    'default-database' = 'default',
    'hive-conf-dir' = '/usr/local/soft/hive-3.1.3/conf'
);

-- 切换元数据
USE CATALOG hive_catalog;

SET 'sql-client.execution.result-mode' = 'tableau';
```

```sql
sql-client.sh -i init.sql
```

## 10、设置sql的并行度

```sql
SET 'parallelism.default' = '2';

select clazz,count(1) as num
from 
students_json
group by clazz;
```

## 11、执行一组sql

```sql
CREATE TABLE clazz_num (
    clazz STRING,
    num BIGINT
) WITH (
 'connector' = 'print'
);

CREATE TABLE gender_num (
    gender STRING,
    num BIGINT
) WITH (
 'connector' = 'print'
);

-- 执行一组sql,多个insert into共用同一个job, 如果使用了同一张表只会读取一次
EXECUTE STATEMENT SET 
BEGIN
    insert into clazz_num
    select clazz,count(1) as num
    from 
    students_json
    group by clazz;

    insert into gender_num
    select gender,count(1) as num
    from 
    students_json
    group by gender;
END;
```

## 案例

### 1、车辆拥堵情况

```sql
-- {"car":"皖F6C7R7","city_code":"340100","county_code":"340111","card":117296031814010,"camera_id":"00230","orientation":"东","road_id":34590541,"time":1614731609,"speed":34.81}
CREATE TABLE cars (
    car STRING,
    city_code STRING,
    county_code STRING,
    card BIGINT,
    camera_id STRING,
    orientation STRING,
    road_id BIGINT,
    `time` BIGINT,
    speed DOUBLE,
    user_action_time as TO_TIMESTAMP(FROM_UNIXTIME(`time`)), -- 动态增加新的字段
    WATERMARK FOR user_action_time AS user_action_time - INTERVAL '5' SECOND -- 设置时间字段和水位线
) WITH (
  'connector' = 'kafka',
  'topic' = 'cars',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'json' -- flink自动解析，按名称映射
);


-- 在mysql中创建表
CREATE TABLE road_flow_avg_speed (
    road_id BIGINT,
    win_start DATETIME ,
    win_end DATETIME ,
    flow BIGINT,
    avg_speed DOUBLE,
    PRIMARY KEY (road_id)
) ;


-- 在flink中创建sink表
CREATE TABLE road_flow_avg_speed (
    road_id BIGINT,
    win_start TIMESTAMP(3),
    win_end TIMESTAMP(3),
    flow BIGINT,
    avg_speed DOUBLE,
    PRIMARY KEY (road_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://master:3306/shujia',
    'table-name' = 'road_flow_avg_speed',
    'username' = 'root',
    'password' = '123456'
);


-- 统计每个道路的车流量和平均车速
-- 计算最近15分钟，每隔1分钟计算一次
insert into road_flow_avg_speed
select 
    road_id,
    HOP_START(user_action_time, interval '1' MINUTE, interval '15' MINUTE) as win_start,
    HOP_END(user_action_time, interval '1' MINUTE, interval '15' MINUTE) as win_end,
    count(1) flow,
    avg(speed) as avg_speed 
from cars
group by 
    road_id,
    HOP(user_action_time, interval '1' MINUTE, interval '15' MINUTE);
```

### 2、异常车辆检测

```sql
-- 当车辆连续3次车速超过60，标记为异常车辆

-- 在mysql中创建表
CREATE TABLE car_speed (
    car VARCHAR(20),
    avg_speed DOUBLE,
    first_speed DOUBLE,
    first_road_id BIGINT,
    first_user_action_time DATETIME,
    speed DOUBLE,
    road_id BIGINT,
    user_action_time DATETIME
);

-- 创建mysql sink表
CREATE TABLE car_speed (
    car STRING,
    avg_speed DOUBLE,
    first_speed DOUBLE,
     first_road_id BIGINT,
    first_user_action_time  TIMESTAMP(3),
    speed DOUBLE,
     road_id BIGINT,
    user_action_time  TIMESTAMP(3)
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:mysql://master:3306/shujia',
    'table-name' = 'car_speed',
    'username' = 'root',
    'password' = '123456'
);

insert into car_speed
select * from cars
	 MATCH_RECOGNIZE (
      PARTITION BY car
      ORDER BY user_action_time
      MEASURES -- 定义返回格式
         round(avg(A.speed),3) as avg_speed,
         FIRST(A.speed) as first_speed,
         FIRST(A.road_id) as first_road_id,
         FIRST(A.user_action_time) as first_user_action_time,
         A.speed as speed,
         FIRST(A.road_id) as road_id,
         A.user_action_time as user_action_time
      PATTERN (A{3}) WITHIN INTERVAL '1' HOUR -- 定义规则
      DEFINE -- 定义规则需要满足的条件
         A as A.speed > 80
    ) AS T;
```






# Doris

## 1、数据模型

### 1、明细模型

|                  | 明细模型               | 主键模型 | 聚合模型 |
| ---------------- | ---------------------- | -------- | -------- |
| Key 列唯一约束   | 不支持，Key 列可以重复 | 支持     | 支持     |
| 同步物化视图     | 支持                   | 支持     | 支持     |
| 异步物化视图     | 支持                   | 支持     | 支持     |
| UPDATE 语句      | 不支持                 | 支持     | 不支持   |
| DELETE 语句      | 部分支持               | 支持     | 不支持   |
| 导入时整行更新   | 不支持                 | 支持     | 不支持   |
| 导入时部分列更新 | 不支持                 | 支持     | 部分支持 |

> 数据不会去重，不能更新数据
> 一般用于存储日志类型的数据

```sql
-- 创建明细模型表
CREATE TABLE IF NOT EXISTS example_tbl_duplicate
(
    log_time        DATETIME       NOT NULL,
    log_type        INT            NOT NULL,
    error_code      INT,
    error_msg       VARCHAR(1024),
    op_id           BIGINT,
    op_time         DATETIME
)
DUPLICATE KEY(log_time, log_type, error_code) -- 指定表的模型和排序键
DISTRIBUTED BY HASH(log_type) BUCKETS 10 -- 分桶
PROPERTIES (
    "replication_num" = "1"
);

-- 4 rows raw data
INSERT INTO example_tbl_duplicate VALUES
('2024-11-01 00:00:00', 2, 2, 'timeout', 12, '2024-11-01 01:00:00'),
('2024-11-02 00:00:00', 1, 2, 'success', 13, '2024-11-02 01:00:00'),
('2024-11-03 00:00:00', 2, 2, 'unknown', 13, '2024-11-03 01:00:00'),
('2024-11-04 00:00:00', 2, 2, 'unknown', 12, '2024-11-04 01:00:00');

-- insert into 2 rows
INSERT INTO example_tbl_duplicate VALUES
('2024-11-01 00:00:00', 2, 2, 'timeout', 12, '2024-11-01 01:00:00'),
('2024-11-01 00:00:00', 2, 2, 'unknown', 13, '2024-11-01 01:00:00');
```

### 2、主键模型

```sql
CREATE TABLE IF NOT EXISTS example_tbl_unique
(
    user_id         LARGEINT        NOT NULL,
    user_name       VARCHAR(50)     NOT NULL,
    city            VARCHAR(20),
    age             SMALLINT,
    sex             TINYINT
)
UNIQUE KEY(user_id, user_name) -- 主键模型
DISTRIBUTED BY HASH(user_id) BUCKETS 10
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true", -- 开启写时合并
    "replication_num" = "1"
);

-- insert into raw data
INSERT INTO example_tbl_unique VALUES
(101, 'Tom', 'BJ', 26, 1),
(102, 'Jason', 'BJ', 27, 1),
(103, 'Juice', 'SH', 20, 2),
(104, 'Olivia', 'SZ', 22, 2);

--  插入新的数据时，如果key已存在会整行覆盖，如果不存在再插入
INSERT INTO example_tbl_unique VALUES
(101, 'Tom', 'BJ', 27, 1),
(102, 'Jason', 'SH', 28, 1);

select * from example_tbl_unique;

-- 如果没开启部分列更新，插入数据时整行覆盖
INSERT INTO example_tbl_unique(user_id,user_name,age) VALUES
(101, 'Tom', 30);

-- 开启部分列更新，只支持写时合并策略
-- 部分列更新写入数据的性能会降低
SET enable_unique_key_partial_update=true;
INSERT INTO example_tbl_unique(user_id,user_name,age) VALUES
(102, 'Jason', 30);
```

### 3、聚合模型

```sql
CREATE TABLE IF NOT EXISTS example_tbl_agg
(
    user_id             LARGEINT    NOT NULL,
    load_dt             DATE        NOT NULL,
    city                VARCHAR(20),
    last_visit_dt       DATETIME    REPLACE DEFAULT "1970-01-01 00:00:00", -- 替换
    cost                BIGINT      SUM DEFAULT "0", -- 求和
    max_dwell           INT         MAX DEFAULT "0",-- 取最大值
)
AGGREGATE KEY(user_id, load_dt, city)
DISTRIBUTED BY HASH(user_id) BUCKETS 10
PROPERTIES (
    "replication_num" = "1"
);

-- 4 rows raw data
INSERT INTO example_tbl_agg VALUES
(101, '2024-11-01', 'BJ', '2024-10-29', 10, 20),
(102, '2024-10-30', 'BJ', '2024-10-29', 20, 20),
(101, '2024-10-30', 'BJ', '2024-10-28', 5, 40),
(101, '2024-10-30', 'SH', '2024-10-29', 10, 20);

-- 插入数据时如果key已存在，会进行聚合
INSERT INTO example_tbl_agg VALUES
(101, '2024-11-01', 'BJ', '2024-10-30', 20, 10);

INSERT INTO example_tbl_agg VALUES
(101, '2024-11-01', 'BJ', '2024-10-30', 20, 100);
```

## 2、数据分区

### 1、手动分区

```sql
-- 1、range分区
CREATE TABLE  bigdata.gateway_records_partition
(
    plate_number VARCHAR(10),
    speed  INT,
    gateway_id VARCHAR(10),
    city VARCHAR(10),
    car_brand VARCHAR(10),
    road_id VARCHAR(10),
    travel_direction VARCHAR(10)
)
DUPLICATE KEY(plate_number,speed)
PARTITION BY RANGE(speed)
(
    PARTITION `p10` VALUES [("0"),  ("10")),
    PARTITION `p20` VALUES [("10"), ("20")),
    PARTITION `p30` VALUES [("20"), ("30")),
    PARTITION `p40` VALUES [("30"), (MAXVALUE))
)
DISTRIBUTED BY HASH(gateway_id) BUCKETS 10
PROPERTIES (
    "replication_num" = "1"
);

insert into bigdata.gateway_records_partition
select plate_number,
cast(speed as int) as speed,gateway_id,city,car_brand,road_id,travel_direction
from bigdata.gateway_records limit 1000;

-- 查看错误信息
curl http://master:8041/api/_load_error_log?file=__shard_0/error_log_insert_stmt_17e6fea7f38c472a-962e46fc75002a61_17e6fea7f38c472a_962e46fc75002a61
                            
-- 1、list分区
CREATE TABLE  bigdata.gateway_records_list_partition
(
    plate_number VARCHAR(10),
    speed  INT,
    gateway_id VARCHAR(10),
    city VARCHAR(10),
    car_brand VARCHAR(10),
    road_id VARCHAR(10),
    travel_direction VARCHAR(10)
)
DUPLICATE KEY(plate_number,speed)
PARTITION BY LIST(city)
(
    PARTITION `bj` VALUES in ('北京'),
    PARTITION `sh` VALUES in ('上海'),
    PARTITION `gz` VALUES in ('广州'),
    PARTITION `sz` VALUES in ('深圳')
)
DISTRIBUTED BY HASH(gateway_id) BUCKETS 10
PROPERTIES (
    "replication_num" = "1"
);
                            
insert into bigdata.gateway_records_list_partition
select plate_number,
cast(speed as int) as speed,gateway_id,city,car_brand,road_id,travel_direction
from bigdata.gateway_records
where city in('北京','上海','广州','深圳')
limit 1000;
                            
SHOW PARTITIONS FROM gateway_records_list_partition;
```

### 2、动态分区

> 自动创建和删除分区

```sql
CREATE TABLE test_dynamic_partition(
    order_id    BIGINT,
    create_dt   DATE,
    username    VARCHAR(20)
)
DUPLICATE KEY(order_id)
PARTITION BY RANGE(create_dt) ()
DISTRIBUTED BY HASH(order_id) BUCKETS 10
PROPERTIES(
    "dynamic_partition.enable" = "true",
    "dynamic_partition.time_unit" = "DAY",
    "dynamic_partition.start" = "-1",
    "dynamic_partition.end" = "2",
    "dynamic_partition.prefix" = "p",
    "dynamic_partition.create_history_partition" = "true",
    "replication_num" = "1"
);

insert into test_dynamic_partition
values(101,'2025-08-01','zhangsan');

insert into test_dynamic_partition
values(103,'2025-08-02','zhangsan1');

insert into test_dynamic_partition
values(104,'2025-07-31','lisi');

-- 如果分区不存在数据插入会报错
insert into test_dynamic_partition
values(102,'2025-07-26','zhangsan');

SHOW PARTITIONS FROM test_dynamic_partition;
```

### 3、自动分区

> 插入数据时自动增加分区

```sql
CREATE TABLE test_auto_partition(
    order_id    BIGINT,
    create_dt   DATE NOT NULL,
    username    VARCHAR(20)
)
DUPLICATE KEY(order_id)
AUTO PARTITION BY RANGE (date_trunc(create_dt, 'day'))()
DISTRIBUTED BY HASH(order_id) BUCKETS 10
PROPERTIES(
    "replication_num" = "1"
);

SHOW PARTITIONS FROM test_auto_partition;

insert into test_auto_partition
values(104,'2025-07-31','lisi');

insert into test_auto_partition
values(105,'2025-07-31','lisi');

insert into test_auto_partition
values(106,'2025-08-01','lisi');
```

## 3、数据分桶

### 1、分桶数量设置原则

- **大小原则**：建议一个 tablet 的大小在 1-10G 范围内。过小的 tablet 可能导致聚合效果不佳，增加元数据管理压力；过大的 tablet 则不利于副本迁移、补齐，且会增加 Schema Change 操作的失败重试代价；
- **数量原则**：在不考虑扩容的情况下，一个表的 tablet 数量建议略多于整个集群的磁盘数量。

### 2、分桶字段选择原则

- **利用查询过滤条件：**使用查询中的过滤条件进行 Hash 分桶，有助于数据的剪裁，减少数据扫描量；
- **利用高基数列：**选择高基数（唯一值较多）的列进行 Hash 分桶，有助于数据均匀的分散在每一个分桶中；
- **高并发点查场景：**建议选择单列或较少列进行分桶。点查可能仅触发一个分桶扫描，不同查询之间触发不同分桶扫描的概率较大，从而减小查询间的 IO 影响。
- **大吞吐查询场景：**建议选择多列进行分桶，使数据更均匀分布。若查询条件不能包含所有分桶键的等值条件，将增加查询吞吐，降低单个查询延迟。

| 单表大小 | 建议分桶数量                                   |
| -------- | ---------------------------------------------- |
| 500MB    | 4-8 个分桶                                     |
| 5GB      | 6-16 个分桶                                    |
| 50GB     | 32 个分桶                                      |
| 500GB    | 建议分区，每个分区 50GB，每个分区 16-32 个分桶 |
| 5TB      | 建议分区，每个分区 50GB，每个分桶 16-32 个分桶 |

```sql
CREATE TABLE hash_bucket_tbl(
    oid         BIGINT,
    dt          DATE,
    region      VARCHAR(10),
    amount      INT
)
DUPLICATE KEY(oid)
PARTITION BY RANGE(dt) (
    PARTITION p250101 VALUES LESS THAN("2025-01-01"),
    PARTITION p250102 VALUES LESS THAN("2025-01-02")
)
DISTRIBUTED BY HASH(region) BUCKETS 8
PROPERTIES(
    "replication_num" = "1"
);
SHOW PARTITIONS FROM hash_bucket_tbl;
```


CREATE TABLE students_json (
    id STRING,
    name STRING,
    age INT,
    gender STRING,
    clazz STRING,
    ts TIMESTAMP_LTZ(3) METADATA FROM 'timestamp' -- 数据写入kafka的时间，
) WITH (
  'connector' = 'kafka',
  'topic' = 'students_partition_age9',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json' -- flink自动解析，按名称映射
);


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
    user_action_time as TO_TIMESTAMP(FROM_UNIXTIME(`time`)), 
    WATERMARK FOR user_action_time AS user_action_time - INTERVAL '5' SECOND 
) WITH (
  'connector' = 'kafka',
  'topic' = 'cars',
  'properties.bootstrap.servers' = 'master:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json' 
);
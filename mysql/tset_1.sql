-- Active: 1750324115522@@master@8123@dws
-- Active: 1750085304813@@master@10000

create external table ods.ods_szt_data (
    car_no string comment '车牌号',
    card_no string comment '卡号',
    close_date string comment '结算日期',
    company_name string comment '公司名称',
    conn_mark string comment '联程标记',
    deal_date string comment '交易日期时间',
    deal_money string comment '交易金额',
    deal_type string comment '交易类型',
    deal_value string comment '交易值',
    equ_no string comment '设备编码',
    station string comment '线路站点'
) partitioned by (dt string comment '分区,按天分区')
row format delimited fields terminated by '\u0001'
stored as orc location '/daas/ods/ods_szt_data';

select * from ods.ods_szt_data where dt = '20180901' limit 100;

create external table dwd.dwd_fact_szt_in_out_detail (
    car_no String comment '车牌号',
    card_no String comment '卡号',
    close_date String comment '结算日期',
    company_name String comment '公司名称',
    conn_mark int comment '联程标记',
    deal_date String comment '交易日期时间',
    deal_money DECIMAL(10, 2) comment '交易金额',
    deal_value DECIMAL(10, 2) comment '交易值',
    equ_no String comment '设备编码',
    station String comment '线路站点'
) partitioned by (
    dt STRING comment '天分区',
    deal_type STRING comment '交易类型'
)
row format delimited fields terminated by '\u0001'
stored as orc location '/daas/dwd/dwd_fact_szt_in_out_detail';

insert
    overwrite table dwd.dwd_fact_szt_in_out_detail partition (dt = '20180901', deal_type)
select
    car_no,
    card_no,
    close_date,
    company_name,
    conn_mark,
    deal_date,
    deal_money,
    deal_value,
    equ_no,
    station,
    case
        when deal_type = '地铁入站' then 'I'
        else 'O'
    end as deal_type
from ods.ods_szt_data
where
    dt = '20180901'
    and deal_type != '巴士'
    and date_format(deal_date, 'HH:mm') > '06:14'
    and date_format(deal_date, 'HH:mm') < '23:59';

select *
from dwd.dwd_fact_szt_in_out_detail
where
    dt = 20180901
limit 100;

-- 进站人次排行

select  ikj,, kl,88888888station, count(*) as persons
from dwd.dwd_fact_szt_in_out_detail
where
    dt = '20180901'
    and deal_type = 'I'
    and station != '""'
group by
    station
order by persons desc;

-- 每日运输乘客最多的车站区间排行榜

select
    case
        when station > in_station then concat(station, '-', in_station)
        else concat(in_station, '-', station)
    end as station_part,
    count(*) as number
from (
        select
            car_no, card_no, station, -- 出站站名
            deal_date, -- 出站时间
            deal_type, -- 出站类型
            lag(station, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_station, -- 进站站名
            lag(deal_date, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_date, -- 进站时间
            lag(deal_type, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_type -- 进站类型
        from dwd.dwd_fact_szt_in_out_detail
        where
            dt = '20180901'
    ) as a
where
    deal_type = 'O'
    and in_deal_type = 'I'
    and station != '""'
    and in_station != '""'
group by (
        case
            when station > in_station then concat(station, '-', in_station)
            else concat(in_station, '-', station)
        end
    )
order by number desc;

-- 线路单程直达乘客耗时平均值排行榜
select in_company_name, round(
        avg(
            (
                unix_timestamp(deal_date) - unix_timestamp(in_deal_date)
            ) / 60
        ), 2
    ) as avg_time
from (
        select
            car_no, card_no, station, -- 出站站名
            deal_date, -- 出站时间
            deal_type, -- 出站类型
            company_name, -- 出站地铁线名
            lag(station, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_station, -- 进站站名
            lag(deal_date, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_date, -- 进站时间
            lag(deal_type, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_type, -- 进站类型
            lag(company_name, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_company_name -- 进站线路
        from dwd.dwd_fact_szt_in_out_detail
        where
            dt = '20180901'
            and station != '""'
    ) as a
where
    deal_type = 'O'
    and in_deal_type = 'I'
    and in_station != '""'
    and company_name = in_company_name
group by
    in_company_name -- (case when station > in_station then concat(station,'-',in_station) else concat(in_station,'-',station) end)
order by avg_time desc;

select round(
        avg(
            (
                unix_timestamp(deal_date) - unix_timestamp(in_deal_date)
            ) / 60
        ), 2
    ) as avg_time
from (
        select
            car_no, card_no, station, -- 出站站名
            deal_date, -- 出站时间
            deal_type, -- 出站类型
            company_name, -- 出站地铁线名
            lag(station, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_station, -- 进站站名
            lag(deal_date, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_date, -- 进站时间
            lag(deal_type, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_type, -- 进站类型
            lag(company_name, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_company_name -- 进站线路
        from dwd.dwd_fact_szt_in_out_detail
        where
            dt = '20180901'
            and station != '""'
    ) as a
where
    deal_type = 'O'
    and in_deal_type = 'I'
    and in_station != '""'
    and company_name = in_company_name;
-- group by in_company_name-- (case when station > in_station then concat(station,'-',in_station) else concat(in_station,'-',station) end)
-- order by avg_time desc;

-- 地铁事实表
create EXTERNAL table dwd.dwd_take_subway_detail (
    card_no String comment '用户编号',
    car_no String comment '车牌号',
    take_day String comment '乘坐日期',
    in_company_name String comment '进站线路',
    out_company_name String comment '出战线路',
    in_station String comment '进站站点',
    out_station String comment '出战站点',
    in_time String comment '进站时间',
    out_time String comment '出站时间',
    in_equ_no String comment '进站设备编码',
    out_equ_no String comment '出战设备编码',
    conn_mark INT comment '联程标记',
    deal_money DOUBLE comment '交易金额',
    take_time DOUBLE comment '用时'
) partitioned by (dt STRING comment '天分区')
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\u0001'
STORED AS ORC LOCATION '/daas/dwd/dwd_take_subway_detail';

-- insert
insert
    overwrite table dwd.dwd_take_subway_detail partition (dt = '20180901')
select
    card_no,
    car_no,
    date_format(in_deal_date, 'yyyy-MM-dd') as take_day, -- 乘坐日期
    in_company_name,
    out_company_name,
    in_station,
    out_station,
    date_format(in_deal_date, 'HH:mm') as in_time, -- in_deal_date as in_time  
    date_format(out_deal_date, 'HH:mm') as out_time, -- out_deal_date as out_time
    in_equ_no,
    out_equ_no,
    conn_mark,
    deal_money,
    round(
        (
            (
                unix_timestamp(out_deal_date) - unix_timestamp(in_deal_date)
            ) / 60
        ),
        2
    ) as take_time
from (
        select
            car_no, card_no, deal_date as out_deal_date, -- 当前交易日期当作出站日期
            station as out_station, -- 当前站点作为出站站点
            company_name as out_company_name, -- 当前公司作为出站公司
            equ_no as out_equ_no, -- 当前设备编码作为出站设备编码
            conn_mark, deal_type, -- 交易类型（I进 O出）
            deal_money, --交易金额
            -- 获取同一卡片（卡号）乘客的上一条交易记录的类型   "（判断是否是进站）" 
            lag(deal_type, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as lag_deal_type,
            -- 获取同一卡片乘客的上一条交易记录公司（作为进站公司）
            lag(company_name, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_company_name,
            -- 获取同一卡片（卡号）乘客的上一条交易记录的站点（作为进站站点）
            lag(station, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_station,
            -- 获取同一卡片（卡号）乘客的上一条交易记录的时间（作为进站时间）
            lag(deal_date, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_deal_date,
            -- 获取同一卡片（卡号）乘客的上一条交易记录的设备（作为进站设备）
            lag(equ_no, 1) over (
                partition by
                    card_no
                order by deal_date
            ) as in_equ_no
        from dwd.dwd_fact_szt_in_out_detail
        where
            dt = '20180901'
    ) as a
where
    -- 筛选条件 确保一次完整的进站--- > 出站形程
    lag_deal_type = 'I'
    and deal_type = 'O'
    and
    -- 排除无效站点
    in_station != '""'
    and out_station != '""';

select * from dwd.dwd_take_subway_detail limit 10;


## 每张卡日消费排行
select * from dwd.dwd_fact_szt_in_out_detail  where deal_value != 0 limit 10;

select
    distinct
    card_no,
    round(((sum(deal_money) over (partition by card_no))/100)) as sum_money
from
    dwd.dwd_fact_szt_in_out_detail
where dt = '20180901' and station !=  '""'
order by sum_money desc
limit 10;

## 线路单日运输乘客总次数排行榜
select
    distinct
    company_name,
    count(*) over (partition by company_name) as passengers
from
    dwd.dwd_fact_szt_in_out_detail
where dt = '20180901' and station !=  '""'
order by passengers desc
limit 10;

select
    company_name,
    count(*) as passengers
from
    dwd.dwd_fact_szt_in_out_detail
where dt = '20180901' and station !=  '""'
group by company_name
order by passengers desc
limit 10;

## 单日从上车到下车间隔时间排行榜
select
    card_no,
    round(((sum(unix_timestamp(deal_date) - unix_timestamp(in_deal_date)))/60),2) as sum_time
from(
select
    card_no,
    deal_date,  -- 下车时间
    deal_type, -- 下车状态
    lag(deal_date,1) over (partition by card_no order by deal_date)  as in_deal_date, -- 上车时间
    lag(deal_type, 1) over ( partition by card_no order by deal_date ) as in_deal_type -- 上车状态
from
    dwd.dwd_fact_szt_in_out_detail
where dt = '20180901' and station != '""') as a
where deal_type = 'O' and in_deal_type = 'I'
group by card_no
order by sum_time desc;

## 站点出站闸机数量排行榜

select
    station,
    count(distinct equ_no) as count_equ_no
    
from
    dwd.dwd_fact_szt_in_out_detail
where
    dt='20180901' and station != '""' and deal_type = 'O'
group by station
order by count_equ_no desc;

## 站点入站闸机数量排行榜
select
    station,
    count(distinct equ_no) as count_equ_no
    
from
    dwd.dwd_fact_szt_in_out_detail
where
    dt='20180901' and station != '""' and deal_type = 'I'
group by station
order by count_equ_no desc;


### 线路进站闸机数排行榜
select
    company_name,
    count(distinct equ_no) as count_equ_no
    
from
    dwd.dwd_fact_szt_in_out_detail
where
    dt='20180901' and station != '""' and deal_type = 'I'
group by company_name
order by count_equ_no desc;

### 线路出站闸机数排行榜
select
    company_name,
    count(distinct equ_no) as count_equ_no
    
from
    dwd.dwd_fact_szt_in_out_detail
where
    dt='20180901' and station != '""' and deal_type = 'O'
group by company_name
order by count_equ_no desc;

### 出站交易收入排行榜
select
    station,
    (sum(deal_money)/100) as sum_deal_money
    
from
    dwd.dwd_fact_szt_in_out_detail
where
    dt='20180901' and station != '""' and deal_type = 'O'
group by station
order by sum_deal_money desc;


### 出站交易所在线路收入排行榜
select
    company_name,
    (sum(deal_money)/100) as sum_deal_money
    
from
    dwd.dwd_fact_szt_in_out_detail
where
    dt='20180901' and station != '""' and deal_type = 'O'
group by company_name
order by sum_deal_money desc;

select * from dwd.dwd_fact_szt_in_out_detail limit 10;

## 每天每线路换乘出站乘客百分比排行榜



select
    a.company_name,
    round(((change_number/full_number)*100),2) as percent_number
from(select
    company_name,
    count(distinct card_no) as full_number
from
    dwd.dwd_fact_szt_in_out_detail
where dt='20180901' and station != '""' and deal_type = 'O'
group by company_name
order by company_name ) as a 
join
(select 
    company_name,
    count(distinct card_no) as change_number
from
    dwd.dwd_fact_szt_in_out_detail
where dt='20180901' and station != '""' and conn_mark = 1 and deal_type = 'O'
group by company_name
order by company_name) as b -- 换乘
on a.company_name = b.company_name
order by percent_number desc;


## 换乘耗时最久的乘客排行榜

select 
    *
from(
select
    card_no,
    company_name,
    deal_date,
    deal_type,
    conn_mark,
    lead(deal_date,1) over (partition by card_no order by deal_date) as out_deal_date,
    lead(deal_type,1)over ( partition by card_no order by deal_date ) as out_deal_type
from
    dwd.dwd_fact_szt_in_out_detail
where dt = '20180901' and station != '""'
order by card_no) as a
where conn_mark = 1;



select
    card_no,
    (sum(unix_timestamp(deal_date) - unix_timestamp(out_deal_date)) over (partition by card_no))as t
from(
select
    card_no,
    company_name,
    deal_date,
    deal_type,
    conn_mark,
    lag(deal_date,1) over (partition by card_no order by deal_date) as out_deal_date,
    lag(deal_type,1)over ( partition by card_no order by deal_date ) as out_deal_type
from
    dwd.dwd_fact_szt_in_out_detail
where dt = '20180901' and station != '""'
order by card_no) as a
where conn_mark = 1 and out_deal_type = 'I' and deal_type = 'O'
order by t desc;



## json 脚本

{
    "job": {
        "setting": {
            "speed": {
                "channel": 3
            }
        },
        "content": [
            {
                "reader": {
                    "name": "hdfsreader",
                    "parameter": {
                        "path": "/daas/dws/dws_take_subway_detail/dt=20180901/*",
                        "defaultFS": "hdfs://master:9000",
                        "column":[
                            {
                                "index": 0,
                                "type": "String"
                            },
                            {
                                "index": 1,
                                "type": "String"
                            },
                            {
                                "index": 2,
                                "type": "String"
                            },
                            {
                                "index": 3,
                                "type": "String"
                            },
                            {
                                "index": 4,
                                "type": "String"
                            },
                            {
                                "index": 5,
                                "type": "String"
                            },
                            {
                                "index": 6,
                                "type": "String"
                            },
                            {
                                "index": 7,
                                "type": "String"
                            },
                            {
                                "index": 8,
                                "type": "String"
                            },
                            {
                                "index": 9,
                                "type": "String"
                            },
                            {
                                "index": 10,
                                "type": "String"
                            },
                            {
                                "index": 11,
                                "type": "String"
                            },
                            {
                                "index": 12,
                                "type": "String"
                            },
                            {
                                "index": 13,
                                "type": "LONG"
                            },
                            {
                                "index": 14,
                                "type": "STRING"
                            },
                            {
                                "index": 15,
                                "type": "LONG"
                            },
                            {
                                "index": 16,
                                "type": "DOUBLE"
                            },
                            {
                                "index": 17,
                                "type": "DOUBLE"
                            }
                        ],
                        "fileType": "orc",
                        "encoding": "UTF-8",
                        "fieldDelimiter": "\u0001"
                    }

                },
                "writer": {
                "name": "clickhousewriter",
                "parameter": {
                    "username": "default",
                    "password": "123456",
                    "column": [
                            "card_no",
                            "car_no",
                            "take_year",
                            "take_month",
                            "take_day",
                            "in_company_name",
                            "out_company_name",
                            "in_station",
                            "out_station",
                            "in_time",
                            "out_time",
                            "in_equ_no",
                            "out_equ_no",
                            "age",
                            "sex",
                            "conn_mark",
                            "deal_money",
                            "take_time"
                        ],
                    "connection": [
                        {
                            "jdbcUrl": "jdbc:clickhouse://master:8123/dws",
                            "table": ["dws_take_subway_detail"]
                        }
                    ],
                    "preSql": [],
                    "postSql": [],

                    "batchSize": 65536,
                    "batchByteSize": 134217728,
                    "dryRun": false,
                    "writeMode": "insert"
                    }
                }
            }
        ]
    }
}


show tables;

select * from dws.dws_take_subway_detail limit 10;


select
    out_company_name,
    count(*) as out_p
from
    dws.dws_take_subway_detail
where conn_mark = 1
group by out_company_name
order by out_company_name;

select
    in_company_name,
    count(*) as in_p
from
    dws.dws_take_subway_detail
group by in_company_name
order by in_p desc;
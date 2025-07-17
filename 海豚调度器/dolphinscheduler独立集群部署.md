# dolphinscheduler独立集群部署

## 1、上传解压

```shell
# 1、上传解压
tar -xvf apache-dolphinscheduler-3.2.1-bin.tar.gz 
mv apache-dolphinscheduler-3.2.1-bin dolphinscheduler-3.2.1

# 2、配置环境变量
export PATH=$PATH:/usr/local/soft/dolphinscheduler-3.2.1/bin
```

## 2、配置mysql作为默认的数据库

```shell
# 1、将mysql（mysql-connector-java-8.0.16.jar）驱动上传到 
# api-server/libs
# alert-server/libs
# master-server/libs  
# standalone-server/libs/standalone-server/
cp mysql-connector-java-8.0.16.jar api-server/libs
cp mysql-connector-java-8.0.16.jar alert-server/libs
cp mysql-connector-java-8.0.16.jar master-server/libs
cp mysql-connector-java-8.0.16.jar worker-server/libs
cp mysql-connector-java-8.0.16.jar standalone-server/libs/standalone-server/
cp mysql-connector-java-8.0.16.jar tools/libs

# 2、初始化数据库
mysql -uroot -p123456 -hmaster
CREATE DATABASE dolphinscheduler DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

# 3、在环境变量中配置mysql信息
# for mysql
vim /etc/profile

export DATABASE=${DATABASE:-mysql}
export SPRING_PROFILES_ACTIVE=${DATABASE}
export SPRING_DATASOURCE_URL="jdbc:mysql://master:3306/dolphinscheduler?useUnicode=true&characterEncoding=UTF-8&useSSL=false"
export SPRING_DATASOURCE_USERNAME=root
export SPRING_DATASOURCE_PASSWORD=123456


source /etc/profile

# 4、执行脚本初始化数据库
bash tools/bin/upgrade-schema.sh
```

## 3、启动dolphinscheduler

```shell
# Start Standalone Server
dolphinscheduler-daemon.sh start standalone-server
# Stop Standalone Server
dolphinscheduler-daemon.sh stop standalone-server
# Check Standalone Server status
dolphinscheduler-daemon.sh status standalone-server

http://master:12345/dolphinscheduler/ui
admin/dolphinscheduler123
```

## 4、配置环境

````shell
export JAVA_HOME=/usr/local/soft/jdk1.8.0_212
export HADOOP_HOME=/usr/local/soft/hadoop-3.1.3
export HADOOP_CONF_DIR=/usr/local/soft/hadoop-3.1.3/etc/hadoop
export SPARK_HOME=/usr/local/soft/spark-3.1.3
export PYTHON_LAUNCHER=/usr/bin/python3
export HIVE_HOME=/usr/local/soft/hive-3.1.3
export DATAX_LAUNCHER=/usr/local/soft/datax/bin/datax.py

export PATH=$PATH:$HADOOP_HOME/bin:$SPARK_HOME/bin:$PYTHON_LAUNCHER:$JAVA_HOME/bin:$HIVE_HOME/bin:$FLINK_HOME/bin:$DATAX_LAUNCHER
````

## 5、案例

### 1、创建表

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS students(
    id string ,
    name string ,
    age string  ,
    gender string  ,
    clazz string 
) 
PARTITIONED BY(pt STRING)
ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
    OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'  
location '/data/students'; 
```

### 2、创建目录

```shell
hdfs dfs -rm -r /data/students/pt=${pt}
hdfs dfs -mkdir -p /data/students/pt=${pt}
```

### 1、datax脚本

```sql
{
    "job": {
        "setting": {
            "speed": {
                 "channel": 1
            },
            "errorLimit": {
                "record": 0,
                "percentage": 0.02
            }
        },
        "content": [
            {
                "reader": {
                    "name": "mysqlreader",
                    "parameter": {
                        "username": "shujia777",
                        "password": "Shujia123456",
                        "column": [
                            "id",
                            "name",
                            "age",
                            "sex",
                            "clazz"
                        ],
                        "connection": [
                            {
                                "table": [
                                    "students"
                                ],
                                "jdbcUrl": ["jdbc:mysql://localhost:3306/bigdata27"
                                ]
                            }
                        ]
                    }
                },
                "writer": {
                    "name": "hdfswriter",
                    "parameter": {
                        "defaultFS": "hdfs://master:9000",
                        "fileType": "text",
                        "path": "/data/students/pt=${pt}",
                        "fileName": "part",
                        "column": [
                            {
                                "name": "id",
                                "type": "VARCHAR"
                            },
                            {
                                "name": "name",
                                "type": "VARCHAR"
                            },
                            {
                                "name": "age",
                                "type": "INT"
                            },
                            {
                                "name": "sex",
                                "type": "VARCHAR"
                            },
                            {
                                "name": "clazz",
                                "type": "VARCHAR"
                            }
                        ],
                        "writeMode": "append",
                        "fieldDelimiter": "\t"
                    }
                }
            }
        ]
    }
}
```

### 4、增加分区

```sql
-- hive的分区表，需要增加分区才能查询到数据
alter table students add if not exists partition(pt='${pt}');
```

### 5、创建结果表

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS clazz_num(
    clazz string ,
    num BIGINT
) 
PARTITIONED BY(pt STRING)
ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
    OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'  
location '/data/clazz_num'; 
```

### 6、统计班级的人数

```sql
insert overwrite table clazz_num partition(pt='${pt}')
select clazz,count(1) as num 
from students
where pt='${pt}'
group by clazz;

```

### 7、创建表

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS sex_num(
    sex string ,
    num BIGINT
) 
PARTITIONED BY(pt STRING)
ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
    OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'  
location '/data/sex_num'; 
```

### 8、统计性别的人数

```sql
insert overwrite table sex_num partition(pt='${pt}')
select gender as sex,count(1) as num 
from students
where pt='${pt}'
group by gender;
```

### 8、导入mysql

```json
{
    "job": {
        "setting": {
            "speed": {
                "channel": 1
            }
        },
        "content": [
            {
                "reader": {
                    "name": "hdfsreader",
                    "parameter": {
                        "path": "/data/sex_num/pt=${pt}/*",
                        "defaultFS": "hdfs://master:9000",
                        "column": [
                               {
                                "index": 0,
                                "type": "string"
                               },
                               {
                                "index": 1,
                                "type": "long"
                               }
                        ],
                        "fileType": "text",
                        "encoding": "UTF-8",
                        "fieldDelimiter": "\t"
                    }
                },
                 "writer": {
                    "name": "mysqlwriter",
                    "parameter": {
                        "writeMode": "insert",
                        "username": "shujia777",
                        "password": "Shujia123456",
                        "column": [
                            "sex",
                            "num"
                        ],
                        "preSql": [
                            "truncate table sex_num"
                        ],
                        "connection": [
                            {
                                "jdbcUrl": "jdbc:mysql://rm-cn-jia3m9rky000bluo.rwlb.rds.aliyuncs.com:3306/bigdata27?useUnicode=true&characterEncoding=UTF-8",
                                "table": [
                                    "sex_num"
                                ]
                            }
                        ]
                    }
                }
            }
        ]
    }
}
```


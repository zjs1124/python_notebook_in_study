# Spark SQL写代码方式

## 1、命令行写SQL

> 和hive类似

```shell
# spark-sql只能使用client模式，local模式
spark-sql --master yarn --deploy-mode client --conf spark.sql.shuffle.partitions=1

# -e :执行sql命令
spark-sql --master yarn --deploy-mode client --conf spark.sql.shuffle.partitions=1 -e "show databases"

# -f: 执行sql文件
spark-sql --master yarn --deploy-mode client --conf spark.sql.shuffle.partitions=1 -f  clazz_num.sql
```

## 2、在pycharm中写代码

> 可以使用SQL处理数据也可以使用DSL，还可以使用RDD
> 也可以读取hive的表进行数据处理（enableHiveSupport）

```python
from pyspark.sql.functions import *
from pyspark.sql.session import SparkSession

# 1、创建SparkSql执行环境
spark = SparkSession.builder.master("local").appName("sql").getOrCreate()

students_df = spark.read.format("csv").schema("id STRING,name STRING,age INT,sex STRING,clazz STRING").load("/data/students")

students_df.show()
```

- 通过spark命令提交任务

```sql
spark-submit  --master yarn --deploy-mode client --conf spark.sql.shuffle.partitions=1 test.py
```

## 3、pyspark

> 交互式代码编写

```sql
# 进入pyspark
pyspark --master yarn --deploy-mode client --conf spark.sql.shuffle.partitions=1 

students_df = spark.read.format("csv").schema("id STRING,name STRING,age INT,sex STRING,clazz STRING").load("/data/students")

students_df.show()

from pyspark.sql.functions import *
students_df.groupby("clazz").agg(count("clazz")).show()
```


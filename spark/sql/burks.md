```python
from pyspark.sql import Window
from pyspark.sql.functions import *
from pyspark.sql.session import SparkSession

# 1、创建SparkSql执行环境
spark = SparkSession.builder.master("local").appName("sql").getOrCreate()

burks_df = (spark.read.format("csv").schema("""
  id STRING,
  year STRING,
  tsl01 DOUBLE,
  tsl02 DOUBLE,
  tsl03 DOUBLE,
  tsl04 DOUBLE,
  tsl05 DOUBLE,
  tsl06 DOUBLE,
  tsl07 DOUBLE,
  tsl08 DOUBLE,
  tsl09 DOUBLE,
  tsl10 DOUBLE,
  tsl11 DOUBLE,
  tsl12 DOUBLE
 """).option("sep", ",").load("../../data/burks.txt"))

burks_df.show()

tsl_arr = array("tsl01", "tsl02", "tsl03", "tsl04", "tsl05", "tsl06", "tsl07", "tsl08", "tsl09", "tsl10", "tsl11",
                "tsl12")

# 每个公司每年每月收入
burk_month_df = burks_df \
    .select("id", "year", posexplode(tsl_arr).alias("index", "tsl")) \
    .withColumn("month", col("index") + 1) \
    .drop("index")

# 如果DF被多次使用可以缓存
burk_month_df.cache()

# 1、统计每个公司每年按月累积收入
burk_month_df \
    .withColumn("acc_tsl", sum("tsl").over(Window.partitionBy("id", "year").orderBy("month"))) \
    .show()

# 2、每个公司当年比上年同期增长率
burk_month_df \
    .withColumn("last_tsl", lag("tsl", 1, 0).over(Window.partitionBy("id", "month").orderBy("year"))) \
    .withColumn("p", coalesce(round(col("tsl") / col("last_tsl") - 1, 5), expr("1.0"))) \
    .show()
```
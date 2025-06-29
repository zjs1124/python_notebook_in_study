```python
from pyspark.sql.session import SparkSession

from pyspark.sql.functions import count

#1、创建sparksql执行环境
spark = SparkSession.builder.master("local").appName("sql").getOrCreate()

# 读取数据,返回DataFrame
#  DF是对RDD的封装,在RDD的基础上增加了表结构
students_df = (spark
               .read
               .format("csv") # 读取数据的格式
               .option("sep",",") # 字段分隔符
               .schema("id string,name string,age int,sex string,clazz string") # 表结构
               .load("../../data/students.txt") # 读取数据的路径
                )

# 体现出了很灵活
# 可以将DF转换成RDD,转换之后可以使用RDD的算子处理数据
students_rdd = students_df.rdd

#1、使用SQL处理数据
# 注册视图(这里创建临时表和视图是一个效果，但一般选择创建视图)
students_df.createOrReplaceTempView("students")

# 使用sql处理数据,返回一个新的DF
clazz_num_df = spark.sql("""
select clazz,count(1) as num
from students
group by clazz
"""
)
# spark.sql 然后里面写sql语句
clazz_num_df.show()
# 2、使用DSL处理数据
(
    students_df
    .groupby("clazz")
    .agg(count("clazz").alias("num"))
    .show()
)
# 这里可以连着点是因为函数返回的是自己本身，所以可以点
```
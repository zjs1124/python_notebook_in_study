```python
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *

# 创建spark环境
spark = (SparkSession
         .builder
         .master("local")
         .appName("demo6")
         .getOrCreate())


# csv、json、parquet、orc
# 其中csv格式hive不支持,hive支持TextFile,所以hive中不能查看csv类的表
# 当spark自己读取json格式的数据时,会自动推断表的结构
# parquet是一种自带表的结果的压缩类型

# 1、csv
students_df = (spark
               .read
               .format("csv")
               .option("sep",",")
               .schema("id string,name string,age int,sex string,clazz string")
               .load("../../data/students.txt")) # 读取数据的路径

# 在sparksql中shuffle之后的分区默认为200
clazz_num = students_df.groupby("clazz").agg(count("clazz").alias("num"))

clazz_num.write.format("csv").mode("overwrite").option("sep","\u0001").save("../../data/clazz_num")

# 2、json
# spark会自动推断json数据中的表结构
data_json = spark.read.json("../../data/data.json")


data_json.printSchema()

# 复杂json解析
# roles的json为array(list)类型
data_json \
    .select(explode("roles").alias("roles")) \
    .select("roles.id","roles.role","roles.works_count") \
    .show(truncate=False)

# 3、parquet

# 读取parquet
students_df.write.format("parquet").mode("overwrite").save("../../data/students_parquet")

# 读取parquet
students_parquet = spark.read.format("parquet").load("../../data/students_parquet")

students_parquet.printSchema()
students_parquet.show()

# 4、orc
students_df.write.format("orc").mode("overwrite").save("../../data/students_orc")
orc_parquet = spark.read.format("orc").load("../../data/students_orc")
orc_parquet.printSchema()
orc_parquet.show()



*******************************
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *


# enableHiveSupport；开启hive元数据支持,可以使用hive中的表
spark = (SparkSession.builder
         .master("local")
         .appName("demo7")
         .config("spark.sql.shuffle.partitions",1)
         .enableHiveSupport()
         .getOrCreate())

spark.sql("show databases").show()

# 1、直接写sql处理数据
spark.sql("""drop table if exists bigdata.clazz_num""")
spark.sql("""
create table bigdata.clazz_num as
select clazz,count(1) as num
from bigdata.students
group by clazz
"""
)

# 2、获取表得到DF使用DSL处理数据
students_df = spark.table("bigdata.students")

# 通过DSL处理数据
sex_num = students_df.groupby("sex").agg(count("sex").alias("num"))

# 创建表
spark.sql("""
create table if not exists bigdata.sex_num(
    sex string,
    num bigint
)
"""
)


# insertInto:将处理结果写入表中
# overwrite:覆盖写入
sex_num.write.insertInto("bigdata.sex_num",overwrite=True)

# 将结果保存到表中,自动创建表，默认格式parquet
# partitionBy: 动态分区
# 静态分区需要指定partitionBy = 具体字段值
sex_num.write.format("orc").mode("overwrite").saveAsTable("bigdata.sex_num2",partitionBy="sex")

****************************************************

from pyspark.sql.session import SparkSession

spark = (SparkSession
         .builder
         .master("local")
         .appName("demo8")
         .config("spark.sql.shuffle.partitions",1)
         .getOrCreate())

# 创建表，只在当前代码中有效
spark.sql("""
create table students
(
    id string,
    name string,
    age int,
    sex string,
    clazz string
)
using csv
location 'file:D/:/trian/data/students.txt';
""")

spark.sql("desc formatted students").show(truncate=False)


spark.sql("select * from students").show()
```
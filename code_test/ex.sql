from pyspark.sql.session import SparkSession
from pyspark.sql.functions import * spark = (
        SparkSession.builder.appName ("app").config (
            "spark.jars", "jars/mysql-connector-java-8.0.29.jar"
        ).config (
            "spark.sql.shuffle.partitions", 1
        ).getOrCreate ()
    )

# 1、读取数据
staypoint = (spark
             .read
             .format("csv")
             .schema(
    "mdn STRING,date STRING,county STRING,lon DOUBLE,lat DOUBLE,bsid STRING,grid_id STRING,biz_type string,event_type string,data_source string")
             .option("sep", "\t")
             .load("../../data/data/staypoint.txt"))

staypoint.createOrReplaceTempView("staypoint")

# staypoint.show()
# 日均停留点数量分布

admincode = (spark
             .read
             .format("csv")
             .schema(
    "prov_id STRING,prov_name STRING,city_id STRING,city_name string,county_id string,county_name STRING,city_level STRING,economic_belt string,city_feature1 string")
             .option("sep", ",")
             .load("../../data/data/admincode.txt"))
# admincode.show()

admincode.createOrReplaceTempView("admincode")

usertag = (spark
           .read
           .format("csv")
           .schema(
    "mdn STRING,name STRING,gender STRING,age string,id_number string,number_attr STRING,trmnl_brand STRING,trmnl_price string,packg string,conpot string,resi_grid_id string,resi_county_id string")
           .option("sep", ",")
           .load("../../data/data/usertag.txt"))
usertag.createOrReplaceTempView("usertag")

# usertag.show()

result = spark.sql("""
select
collect_set(`time`) as `time`,
county_name,
collect_set(gender) as gender
from
(
select
distinct 
s.mdn,
substring(`date`,9,2) as `time`,
concat(prov_name,city_name,county_name) as county_name,
gender
from
staypoint as s join admincode as a on s.county = a.county_id 
join usertag as u on u.mdn=s.mdn) as b
group by county_name
""")

# Convert array columns to string columns for JDBC write
result = result.withColumn("time", concat_ws(",", col("time"))) \
               .withColumn("gender", concat_ws(",", col("gender")))

result.show()

result.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://master:3306") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "bigdata.time") \
    .option("user", "root") \
    .option("password", "123456") \
    .mode("overwrite") \
    .save()
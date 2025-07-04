```python
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
spark = SparkSession.builder.master("local").appName("demo2_dsl").getOrCreate()


students_df = spark.read.format("json").load("../../data/students.json")


students_df.printSchema()
```

## 1.show
```python
students_df.show() # 默认查看前20行
students_df.show(n=10) # 查看前10行
students_df.show(truncate=False) # 是否将表中字段过多的部分省略显示
```


## 2、 where:过滤数据

### 使用sql表达式  
```python
students_df.where("gender = '男' and age = 21").show()
```

### 使用列表达式
```python
students_df.where(students_df.age == 21).show()
```

### col("age"):获取列
```python
students_df.where(col("age") == 22).show()
students_df.where(col("age").isNotNull()).show()
```

## 3、select
```python
students_df.select("id","name").show()
students_df.select("id",(col("age")+1).alias("age")).show()
students_df.select("id",substring("clazz",1,2).alias("clazz_type")).show()
```

### selectExpr:使用sql表达式的方式
```python
students_df.selectExpr("id","substring(clazz,1,2) as clazz_type").show()
```

## 4、group by:分组聚合
```python
(
    students_df
    .groupby("clazz")
    .agg(
        count("clazz").alias("num"),
        round(avg("age"),2).alias("avg_age"),
        max("age").alias("max_age")
    ).show()
)
```


### 聚合之后使用where进行过滤,相当于having
```python
(
    students_df
    .groupby("clazz")
    .agg(count("clazz").alias("num"))
    .where(col("num") > 80)
    .show()
)
```

## 5、order by
```python
students_df \
    .groupby("clazz") \
    .agg(count("clazz").alias("num")) \
    .orderBy(col("num").desc()) \
    .show()
```


## 6、limit:返回n行并且以DF的形式返回
```python
students_df.limit(10).show()
```
### head:返回前n行并将其以列表形式返回,将DF的数据拉取到Driver端
```python
head_list = students_df.head(10)
for stu in head_list:
    print(stu.id,stu.name)
```

## 7、join
```python
# 读取分数表
score_df = (spark
            .read
            .format("csv")
            .schema("sid string,cid string,score double")
            .option("sep",",").load("../../data/score.txt")
)
```
### 1、关联字段名一致时
```python
students_df.join(score_df,"id",how="left").show()
# on的字段名为共同的字段名
```
### 2、关联字段名不一致时
```python
students_df.join(score_df,col("id") == col("sid"),how="inner").show()
# 使用col("a表的字段名") == col("b表的字段名")
```

### 统计每个班级总共的平均分
```python
students_df \
    .join(score_df, col("id") == col("sid"), how="inner") \
    .groupby("id", "clazz") \
    .agg(sum("score").alias("sum_score")) \
    .groupby("clazz") \
    .agg(round(avg("sum_score"), 2).alias("avg_score")) \
    .show()
```
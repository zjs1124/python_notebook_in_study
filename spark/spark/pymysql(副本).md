import pymysql
from pyspark.context import SparkContext
import time

# 1、创建spark执行环境
sc = SparkContext(master='local', appName='word_count')

# 统计班级的人数，将统计结果保存到mysql中

student_rdd = sc.textFile("../../data/students.txt")

# 统计班级的人数
clazz_num_rdd = student_rdd.map(lambda stu: (stu.split(",")[-1], 1)).reduceByKey(lambda a, b: a + b)

def to_mysql_fun(kv):
    clazz = kv[0]
    num = kv[1]

    # 1、在foreach算子中创建数据库链接，会为每一条数据都创建一个链接，创建数据库链接大概10毫秒，如果数据量大，会很慢
    # 2、在Driver端创建数据库链接，不能在Executor端使用，因为数据库链接不能序列化

    # 1、创建数据库链接
    start_time = time.time()
    con = pymysql.connect(host='master', port=3306, user='root', passwd='123456', database="shujia")
    end_time = time.time()
    print(f"执行时间：{end_time - start_time}")

    # 2、获取游标执行sql
    cursor = con.cursor()
    # 3、执行sql
    cursor.execute("insert into clazz_num(clazz,num) values (%s,%s)", (clazz, num))
    # 4、提交事务
    con.commit()
    con.close()

clazz_num_rdd.foreach(to_mysql_fun)


import pymysql
from pyspark.context import SparkContext
import time

# 1、创建spark执行环境
sc = SparkContext(master='local', appName='word_count')

# 统计班级的人数，将统计结果保存到mysql中

student_rdd = sc.textFile("../../data/students.txt", 3)

# 统计班级的人数
clazz_num_rdd = student_rdd.map(lambda stu: (stu.split(",")[-1], 1)).reduceByKey(lambda a, b: a + b)

start_time = time.time()


def to_mysql_fun(iter):
    # 1、创建数据库链接
    # 每一个分区创建一个数据库链接
    con = pymysql.connect(host='master', port=3306, user='root', passwd='123456', database="shujia")
    end_time = time.time()
    print(f"执行时间：{end_time - start_time}")

    # 2、获取游标执行sql
    cursor = con.cursor()
    for clazz, num in iter:
        # 3、执行sql
        cursor.execute("insert into clazz_num(clazz,num) values (%s,%s)", (clazz, num))
        # 4、提交事务
        con.commit()

    con.close()


# foreachPartition: 一次处理一个分区的数据
# 一般用于将rdd的数据保存到外部系统
clazz_num_rdd.foreachPartition(to_mysql_fun)
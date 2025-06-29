```python
from pyspark.context import SparkContext

sc = SparkContext(master="local", appName="word_count")

names_rdd = sc.parallelize([('001', '张三'),
                            ('002', '李四'),
                            ('003', '王五'),
                            ('005', '赵六')])

ages_rdd = sc.parallelize([('001', 23),
                           ('002', 24),
                           ('003', 25),
                           ('004', 26)])

# 1、reduce join
# 会产生shuffle
# 一般用于大表关联大表
reduce_join_rdd = names_rdd.join(ages_rdd)

# reduce_join_rdd.foreach(print)


# 2、map join
# 1、将小表拉取到Driver端，放在Driver的内存中
# 2、将小表从Driver端广播到Executor
# 3、大表使用map算子从小表中获取数据

# 1、将小表拉取到Driver端，放在Driver的内存中（小表的数据量在100M左右）
# collectAsMap将RDD转换成python的字典
ages_map = ages_rdd.collectAsMap()

# 2、将小表从Driver端广播到Executor
age_map_bro = sc.broadcast(ages_map)


# 3、大表使用map算子从小表中获取数据
def map_join_fun(kv):
    id = kv[0]
    name = kv[1]

    # 获取广播变量
    ages = age_map_bro.value

    # 通过id获取年龄
    age = ages.get(id)

    return id, name, age


map_join_rdd = names_rdd.map(map_join_fun)
map_join_rdd.foreach(print)

while True:
    pass
```
大表map_join小表只能使用左连接,不能使用全连接哥右连接。
如果大表直接关联小表会产生数据倾斜。
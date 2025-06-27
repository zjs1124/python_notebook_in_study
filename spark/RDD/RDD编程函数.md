## 转换算子和操作算子
转换算子是懒执行，只有当操作算子触发时才会执行
转换算子的数据类型由RDD->RDD,而操作算子的数据类型会由RDD->其他类型

## 转换算子
***1、map(func)***
传一行出一行
map函数将数据一行一行的传入到后面的函数体中进行处理，并将返回的数据构建为RDD
函数可以很简单也可以很复杂
```python
import json

from pyspark.context import SparkContext
# 创建环境
sc = SparkContext(master="local",appName="word_count")

ints = [1,2,3,4,5,6,7,8,9]

#parallelize: 将python集合转换为RDD
rdd1 = sc.parallelize(ints)

rdd2 = rdd1.map(lambda x : x ** 2)
rdd2.foreach(print)

"""
使用map算子解析json格式的数据
"""

students_json_rdd = sc.textFile("../../data/students.json")

# 解析json格式的数据
def student_pas(stu_json):
    stu_dict = json.loads(stu_json)# 加载json 数据
    id = stu_dict.get("id")
    name = stu_dict.get("name")# 使用get不会报错，字典中没有时会返回None
    age = stu_dict.get("age") # 直接使用key查询时如果字典中没有会报错
    gender = stu_dict.get("gender")
    clazz = stu_dict.get("clazz")

    clazz_type = clazz[:2]

    return id,name,age,gender,clazz,clazz_type # 返回一个元组

students_rdd = students_json_rdd.map(student_pas)

students_rdd.foreach(print)


```
***2、fliter(func)***
传多行出少行，过滤函数
将数据一行一行传入到后面的函数体中，若为False则舍弃,True则保留，并将保留的数据构建为RDD  
```python

from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

# 读取数据
students_rdd = sc.textFile("../../data/students.txt")

filter_rdd = students_rdd.filter(lambda stu:stu.split(",")[3] == "男" and int(stu.split(",")[2]) == 21)

filter_rdd.foreach(print)

```
***3、flatMap(func)***
传少行出多行，爆炸函数
将一行传入到后面的函数体中，函数返回一个列表，并将返回的列表展开并构建为RDD函数
```python
from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

stu_score_rdd = sc.textFile("../../data/stu_score.txt")

stu_score_rdd.flatMap(lambda line:line.split(",")[-1].split("|")).foreach(print)

def flat_map_fun(line):
    stu_split = line.split(",")
    # 取出学生信息
    stu_info = stu_split[:-1]
    # 拼接成字符串
    stu = ",".join(stu_info)

    sco_list = stu_split[-1].split("|")

    # 将学生信息拼接到分数前面
    stu_score = [f"{stu},{sco}" for sco in sco_list]

    return stu_score

stu_score_rdd = stu_score_rdd.flatMap(flat_map_fun)
stu_score_rdd.foreach(print)

```

***4、mapPartitions(func)***
传一个迭代器，出一个迭代器
一次处理一个分区
```python
from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

students_rdd = sc.textFile("../../data/students.txt",minPartitions=3)

print(f"students_rdd:{students_rdd.getNumPartitions()}")

def map_fun(iter):
    print("map_fun")
    clazzs = [i.split(",")[-1] for i in iter]
    return clazzs

students_rdd.mapPartitions(map_fun).foreach(print)

```

***5、mapPartitionswithIndex(func)***
类似于 mapPartitions，但也为 func 提供了一个整数值，该值表示 分区，即(v,迭代器)->迭代器

***6、reudeceByKey(func,[numPartitions])***
根据key进行聚合，执行聚合的具体函数为后面的函数体,并将返回的数据构建为RDD
所需要**传入的数据必须为(k,v)格式**
因为具有shuffle阶段，所以**可选择**分区数[numPartitions]
```python
from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

# 读取数据
students_rdd = sc.textFile("../../data/students.txt")

# 解析数据
kv_rdd = students_rdd.map(lambda stu:(stu.split(",")[-1],1))

# reduceByKey: 对相同KEY的value 进行聚合计算
kv_rdd.reduceByKey(lambda x,y:x+y).foreach(print)

# 先分组再聚合计算
group_by_key = kv_rdd.groupByKey()
group_by_key.map(lambda kv:(kv[0] ,sum(kv[1]))).foreach(print)


```

***7、groupByKey([numPartitions])***
根据key进行分组，并将相同key的value整合为一个迭代器,即(k,v迭代器)
所需要**传入的数据必须为(k,v)格式**
因为具有shuffle阶段，所以**可选择**分区数[numPartitions]
```python
from pyspark.context import SparkContext

sc = SparkContext(master='local',appName='word_count')

# 1、统计每个班级的平均年龄

#读取数据
students_rdd = sc.textFile("../../data/students.txt")

# 解析数据
kv_rdd = students_rdd.map(lambda stu:(stu.split(",")[-1],int(stu.split(",")[2])))

# 按照班级分组
group_by_key_rdd = kv_rdd.groupByKey()

def avg_fun(kv):
    clazz = kv[0]
    ages = kv[1]
    # 计算平均年龄
    avg_age = round(sum(ages)/len(ages),2)
    return clazz,avg_age


avg_age_rdd = group_by_key_rdd.map(avg_fun)

avg_age_rdd.foreach(print)


avg_age_rdd = group_by_key_rdd.map(avg_fun)
```

***8、aggregateByKey(zeroValue,seqOp, combOp, [numPartitions])***
对相同的key的value值进行计算
可以自己设置初始值,map端的聚合函数和reduce端的聚合函数
所需要**传入的数据必须为(k,v)格式**
因为具有shuffle阶段，所以**可选择**分区数[numPartitions]
```python
from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

# 读取数据
students_rdd = sc.textFile("../../data/students.txt",3)

# 解析数据
kv_rdd = students_rdd.map(lambda stu:(stu.split(",")[-1],1))

# aggregateByKey:对相同key的value进行聚合计算
# 可以单独定义map端和reduce端的聚合逻辑
num_rdd = kv_rdd.aggregateByKey(0, # 初始值
                                lambda x,y:x+y, # map端预聚合函数
                                lambda a,b:a+b # reduce端合并结果的函数
                                )

num_rdd.foreach(print)
```

***9、sortBy(字段,[ascending]，[numPartitions])***
相比于sortByKey更灵活,可以自由选择字段来进行排序,默认升序
所需要**传入的数据必须为(k,v)格式**
因为具有shuffle阶段，所以**可选择**分区数[numPartitions]
```python
from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

# 读取数据
students_rdd = sc.textFile("../../data/students.txt")

# 解析数据
kv_rdd = students_rdd.map(lambda stu:(stu.split(",")[-1],1))

num_rdd = kv_rdd.reduceByKey(lambda x,y:x+y)

# sortBy；指定一个字段进行排序
sort_rdd = num_rdd.sortBy(lambda kv:kv[1])

sort_rdd.foreach(print)
```
***10、join(RDD)***
一个RDD join 另一个RDD，默认 inner join
**RDD1.join(RDD2)**
此外还有FullJoin,LeftOuterJoin和RightOuterJoin
```python
from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

names_rdd = sc.parallelize([('001', '张三'),
                             ('002', '李四'),
                             ('003', '王五'),
                             ('005', '赵六')])


ages_rdd = sc.parallelize([('001', 23),
                           ('002', 24),
                           ('003', 25),
                           ('004', 26)])

names_rdd.join(ages_rdd).foreach(print)

print("=" * 100)

names_rdd.leftOuterJoin(ages_rdd).foreach(print)

print("=" * 100)

names_rdd.fullOuterJoin(ages_rdd).foreach(print)

print("=" * 100)
# 整理结果
names_rdd.join(ages_rdd).map(lambda kv:(kv[0],kv[1][0],kv[1][1])).foreach(print)

```
***11、union***
一个RDD union 另一个RDD，不去重
**两个RDD的数据类型必须保持一致**
**RDD1.union(RDD2)**
此外,还有 union all
```python
from pyspark.context import SparkContext

sc = SparkContext(master = 'local',appName='word_count')

rdd1 = sc.parallelize([1,2,3,4,5,6,7,8])
rdd2 = sc.parallelize([123,23,3,4,5,6,1,2,3,4])

union_rdd = rdd1.union(rdd2)
print(f"union_rdd:{union_rdd.getNumPartitions()}")
union_rdd.foreach(print)

print("=" * 100 )

distinct_rdd = union_rdd.distinct()

distinct_rdd.foreach(print)
```

***12、sample(replacement,样本比例)***
随机抽出约为样本比例的数据,repalcemen为False时为不放回抽取
```python
from pyspark.context import SparkContext

sc = SparkContext(master='local',appName='word_count')

students_rdd = sc.textFile("../../data/students.txt",minPartitions=3)

sample_rdd = students_rdd.sample(False,0.1) # 不放回抽样且抽样的样本占比约为0.1(实际会有浮动)

sample_rdd.foreach(print)
```

# 操作算子

***1、foreach(func)***
将传入的数据一行一行传入到后面的函数体中，但是不会将返回后的数据构建为RDD


***2、sum()***
累加计算总和

***3、count()***
计算总行数

***4、reduce(func)***
将数据传入到函数中进行全局聚合

***5、take(num)***
取前num位数

***6、collect()***
将RDD转换为python列表

***7、saveAsTextFile(路径)***
将结果保存到路径中

***8、foreachPartitions(fun)***
对每个分区进行fun函数
```python
from itertools import count

from pyspark.context import SparkContext

sc = SparkContext(master="local",appName="word_count")

#读取数据
students_rdd = sc.textFile("../../data/students.txt")

#1、foreach:将rdd中的数据一行一行传递给后面的函数
students_rdd.foreach(lambda line:print(line))
students_rdd.foreach(print)

#2、count:统计行数
count = students_rdd.count()
print(f"count:{count}")

#3、sum求和
sum_age = students_rdd.map(lambda stu:int(stu.split(",")[2])).sum()
print(f"sum_age{sum_age}")
print(f"avg_age:{sum_age / count}")

#4、reduce：全局聚合
reduce = students_rdd.map(lambda stu: int(stu.split(",")[2])).reduce(lambda a,b:a+b)
print(f"reduce；{reduce}")

# 5、collect:将RDD转换为列表
students_list = students_rdd.collect()
print(students_list)

# 6、take；取top
take = students_rdd.take(2)
print(take)

# 7、saveAsTextFile:保存结果
# students_rdd.saveAsTextFile("../../data/student_save")

def fun(iter):
    for i in iter:
        print(i)


# 8、foreachPartition:一次循环一个分区
students_rdd.foreachPartition(fun)
```
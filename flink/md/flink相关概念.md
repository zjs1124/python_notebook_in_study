> 并行度和task之间的关系
一般情况,一个并行度对应一个task，对应一个task slot。但是一个task slot可以有多个task。

> 并行度设置
1、在代码中设置,优先级最高.(在本地运行,即不在服务器上运行时,需要再代码中将并行度设置为1，因为python 和 java之间进行通信，并行度需为 1 才不会报错)
2、提交任务时设置 -p 并行度数
3、配置文件中有默认值,默认为1，即parallelism.default:1

> 设置原则,基于数据量设置(每秒的数据量)
1、非聚合计算:flink单个并行度的吞吐量大概10万/s
2、聚合计算：flink单个并行度的吞吐量大概1万/s
3、也可以参考kafka的分区数来设置并行度

> flink资源
flink 默认一个并行度对应一个slot
设置多少并行度就需要多少资源

> flink中有三种在算子内使用的写法
1、使用lambda函数
```python
words_ds = lines_ds.flat_map(lambda line:line.split(","))
```

2、自定义函数
```python
def flat_map_fun(line):
    for word in line.split(","):
        yield word


lines_ds.flat_map(flat_map_fun)
```

3、使用类方式
这种方式多了open和close方式,可以用于初始化操作,比如创建数据库的连接
```python
class FlatMapClass(FlatMapFunction):
    def flat_map(self, line):
        for word in line.split(","):
            yield word

lines_ds.flat_map(FlatMapClass()).print()
```



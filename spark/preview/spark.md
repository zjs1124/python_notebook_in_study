# 一、spark与mapreduce 和 flink 的区别
### 1、spark与mapreduce 的区别及优缺点

1. 区别

- spark 将中间结果存储在内存中，可以反复利用，从而提高处理数据的性能 

​		而mapreduce将中间结果存储在磁盘中，减少内存的占用，但牺牲性能

- spark 使用了DAG有向无环图,相比mapreduce减少了shuffle次数  

- spark是粗粒度申请,mapreduce是细粒度申请 

​		粗粒度申请是指在提交资源时,spark会提前向资源管理器将资源申请完毕再执行task任务。

​		而mapreduce则会task自己申请资源自己运行，虽然资源充分利用，但很慢

- spark的task执行单位是线程,而mapreduce的task执行单元是进程

  进程的创建销毁开销大而线程的创建销毁开销小

2. spark优缺点

   优点： 

   1、spark把中间数据放在内存中,迭代运算效率高

   2、spark容错性高

   3、spark更加通用

   缺点:

   1、消耗内存大

   2、性能不稳定

   




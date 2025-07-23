> 状态的概念
状态:前面的计算结果。

> 有状态计算
基于上一次/前面的计算结果(状态)进行计算

> 有状态算子
基于前面的计算结果进行计算的算子

> 容错机制(checkpoint)
***概念:*** checkpoint里面存储着状态(即计算结果)和消费偏移量(offset),一定时间持久化到HDFS中进行存储。当任务突然失败或者中断的时候，重新启动任务时会读取checkpoint的数据，再根据状态和消费偏移量(offset)再重新计算。


***触发:*** jobmanager里面的checkpoint coordinator 向taskmanager发送chechkpoint trigger。taskmanager中的task生成的状态(state)会根据 state backends策略生成本地快照副本存储在内存中,再持久化到hdfs的checkpoint目录下，并向jobmanager返回状态快照的元数据.


### Spark和mr底层模型
1、spark和mr(MapReduce) 都是MapReduce模型
2、先执行map task再执行reduce task
3、可以在map端对相同的key进行预聚合,减少shuffle过程中传输的数据量提高执行效率,所以mr模型更适合批处理

### Flink 流处理模式底层模型
1、flink流处理是持续流模型
2、所有task同时启动,等待数据到达,来一条数据处理一条数据
3、持续流模型,需要更多的资源启动task

***Flink的批处理模型和spark一样,是MR模型***

数据从上游发生到下游默认不是一条一条发送,效率低。默认是每隔200ms或者32kb发送一次

flink 流处理模式可以开启预聚合,在上游对一段时间内的数据进行预聚合,减少shuffle过程中传输的数据量,提高效率,开启之后会增加延迟。
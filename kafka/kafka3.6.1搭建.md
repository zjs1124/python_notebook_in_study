# kafka3.6.1搭建

## 1、上传解压配置环境变量

```shell
# 配置环境变量
vim  /etc/profile

export KAFKA_HOME=/usr/local/soft/kafka-3.6.1
export PATH=$PATH:$KAFKA_HOME/bin

source /etc/profile
```

## 2、修改配置文件((已改好，可省略)

```shell
cd /usr/local/soft/kafka-3.6.1/config
server.properties
zookeeper.properties
```

## 3、启动

```shell
# 启动zookeeper
zookeeper-server-start.sh -daemon /usr/local/soft/kafka-3.6.1/config/zookeeper.properties
# 进程名：QuorumPeerMain

# 启动kafka
kafka-server-start.sh -daemon /usr/local/soft/kafka-3.6.1/config/server.properties
# Kafka
```

## 4、测试

```shell
# 创建topic,一个topic对应一种数据，类似hive中建表的意思
kafka-topics.sh --bootstrap-server master:9092 --create --topic shujia --partitions 1

# 查看列表
kafka-topics.sh --bootstrap-server master:9092 --list 

# 查看topic信息
kafka-topics.sh --bootstrap-server master:9092 --describe --topic shujia

# 1、生产者
kafka-console-producer.sh --broker-list master:9092 --topic text

# 2、消费者
# --from-beginning：从头消费
kafka-console-consumer.sh --bootstrap-server master:9092 --from-beginning --topic text

# 创建多分区topic
kafka-topics.sh --bootstrap-server master:9092 --create --topic bigdata --partitions 4
kafka-console-producer.sh --broker-list master:9092 --topic bigdata

# --replication-factor:分区的副本数，保证数据不丢失
kafka-topics.sh --bootstrap-server master:9092 --create --topic bigdata1 --partitions 4 --replication-factor 2
```


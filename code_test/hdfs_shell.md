第5章 HDFS的Shell操作
5.1 基本语法
hadoop fs 具体命令  OR  hdfs dfs 具体命令
两个是完全相同的。
5.2 命令大全

5.3 常用命令实操
5.3.1 准备工作
1、启动Hadoop集群（方便后续的测试）
[xiaobaiwen@node1 hadoop-3.1.3]$ sbin/start-dfs.sh 
[xiaobaiwen@node2 hadoop-3.1.3]$ sbin/start-yarn.sh
2、-help：输出这个命令参数
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -help rm
3、创建/bigdata文件夹
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -mkdir /bigdata
***5.3.2 上传***
1、-moveFromLocal：从本地剪切粘贴到HDFS
#创建一个文件
[xiaobaiwen@node1 hadoop-3.1.3]$ vim xiaobaic.txt
#输入：
xiaobaic

hadoop fs -moveFromLocal xiaobaic.txt /bigdata
2、-copyFromLocal：从本地文件系统中拷贝文件到HDFS路径去
[xiaobaiwen@node1 hadoop-3.1.3]$ vim  xiaobaij.txt
#输入：
xiaobaij

[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -copyFromLocal xiaobaij.txt /bigdata
3、-put：等同于copyFromLocal，生产环境更习惯用put
[xiaobaiwen@node1 hadoop-3.1.3]$ vim xiaobaiw.txt
#输入：
xiaobaiw

[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -put xiaobaiw.txt /bigdata
4、-appendToFile：追加一个文件到已经存在的文件末尾
[xiaobaiwen@node1 hadoop-3.1.3]$ vim xiaobaicjw.txt
#输入：
xiaobaicjw

[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -appendToFile xiaobaicjw.txt /bigdata/xiaobaic.txt
***5.3.3 下载***
1、-copyToLocal：从HDFS拷贝到本地
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -copyToLocal /bigdata/xiaobaic.txt /opt/module/hadoop-3.1.3/
2、-get：等同于copyToLocal，生产环境更习惯用get
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -get /bigdata/xiaobaic.txt /opt/module/hadoop-3.1.3/xiaobaic2.txt
2.3.4 HDFS直接操作
1、-ls: 显示目录信息
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -ls /bigdata/
2、-cat：显示文件内容
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -cat /bigdata/xiaobaic.txt
3、-chgrp、-chmod、-chown：Linux文件系统中的用法一样，修改文件所属权限
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -chmod 666 /bigdata/xiaobaic.txt
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -chmod 666 /bigdata/xiaobaic.txt
4、-mkdir：创建路径
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -mkdir /student
5、-cp：从HDFS的一个路径拷贝到HDFS的另一个路径
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -cp /bigdata/xiaobaic.txt /student
6、-mv：在HDFS目录中移动文件
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -mv /bigdata/xiaobaij.txt /student
7、-tail：显示一个文件的末尾1kb的数据
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -tail /bigdata/xiaobaic.txt
8、-rm：删除文件或文件夹
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -rm /bigdata/xiaobaic.txt
9、-rm -r：递归删除目录及目录里面内容
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -rm -r /bigdata
10、-du统计文件夹的大小信息
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -du -s -h /student
29  87  /student
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -du  -h /student
20  60  /student/xiaobaic.txt
9   27  /student/xiaobaij.txt
说明：29表示文件大小；87表示29*3个副本；/student表示查看的目录
11、-setrep：设置HDFS中文件的副本数量
[xiaobaiwen@node1 hadoop-3.1.3]$ hadoop fs -setrep 10 /student/xiaobaic.txt

这里设置的副本数只是记录在NameNode的元数据中，是否真的会有这么多副本，还得看DataNode的数量。因为目前只有3台设备，最多也就3个副本，只有节点数的增加到10台时，副本数才能达到10。
第7章 HDFS的读写流程
7.1 HDFS写数据流程
7.1.1 剖析文件写入

（1）客户端通过Distributed FileSystem模块向NameNode请求上传文件，NameNode检查目标文件是否已存在，父目录是否存在。
（2）NameNode返回是否可以上传。
（3）客户端请求第一个 Block上传到哪几个DataNode服务器上。
（4）NameNode返回3个DataNode节点，分别为dn1、dn2、dn3。
（5）客户端通过FSDataOutputStream模块请求dn1上传数据，dn1收到请求会继续调用dn2，然后dn2调用dn3，将这个通信管道建立完成。
（6）dn1、dn2、dn3逐级应答客户端。
（7）客户端开始往dn1上传第一个Block（先从磁盘读取数据放到一个本地内存缓存），以Packet为单位，dn1收到一个Packet就会传给dn2，dn2传给dn3；dn1每传一个packet会放入一个应答队列等待应答。
（8）当一个Block传输完成之后，客户端再次请求NameNode上传第二个Block的服务器。（重复执行3-7步）。
7.1.2 网络拓扑-节点距离计算
在HDFS写数据的过程中，NameNode会选择距离待上传数据最近距离的DataNode接收数据。那么这个最近距离怎么计算呢？
节点距离：两个节点到达最近的共同祖先的距离总和。

例如，假设有数据中心d1机架r1中的节点n1。该节点可以表示为/d1/r1/n1。利用这种标记，这里给出四种距离描述。
大家算一算每两个节点之间的距离。

7.1.3 机架感知（副本存储节点选择）
1、机架感知说明
（1）官方说明
http://hadoop.apache.org/docs/r3.1.3/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Data_Replication
For the common case, when the replication factor is three, HDFS’s placement policy is to put one replica on the local machine if the writer is on a datanode, otherwise on a random datanode, another replica on a node in a different (remote) rack, and the last on a different node in the same remote rack. This policy cuts the inter-rack write traffic which generally improves write performance. The chance of rack failure is far less than that of node failure; this policy does not impact data reliability and availability guarantees. However, it does reduce the aggregate network bandwidth used when reading data since a block is placed in only two unique racks rather than three. With this policy, the replicas of a file do not evenly distribute across the racks. One third of replicas are on one node, two thirds of replicas are on one rack, and the other third are evenly distributed across the remaining racks. This policy improves write performance without compromising data reliability or read performance.
（2）源码说明
Crtl + n 查找BlockPlacementPolicyDefault，在该类中查找chooseTargetInOrder方法。
2、Hadoop3.1.3副本节点选择

第一个副本在Client所处的节点上。如果客户端在集群外，随机选一个。
第二个副本在另一个机架的随机一个节点。
第三个副本在第二个副本所在机架的随机节点。
7.2 HDFS读数据流程

（1）客户端通过DistributedFileSystem向NameNode请求下载文件，NameNode通过查询元数据，找到文件块所在的DataNode地址。
（2）挑选一台DataNode（就近原则，然后随机）服务器，请求读取数据。
（3）DataNode开始传输数据给客户端（从磁盘里面读取数据输入流，以Packet为单位来做校验）。
（4）客户端以Packet为单位接收，先在本地缓存，然后写入目标文件。



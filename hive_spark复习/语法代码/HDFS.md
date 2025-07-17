### 语法大体格式:
***hadoop fs 具体命令***
***hdfs dfs 具体命令***

### 如何在虚拟机上查看命令大全
***bin/hadoop fs***

### 常用命令
#### 启动hadoop集群:
start-all.sh

#### 上传

***-movefromlocal:从本地剪切粘贴到HDFS***

hadoop fs -movefromlocal xiaobaic.txt(本地文件) /bigdata(HDFS目标路径)

***-copyfromlocal:从本地文件系统中拷贝文件到HDFS路径去***

hadoop fs -copyfromlocal xiaobaij.txt(本地文件) /bigdata(HDFS目标路径)

***-put:等同于copyFromlocal,生产环境更习惯用put*** *  

hadoop fs -put xiaobaiw.txt(本地文件) /bigdata(目标路径)

***-appendtofile:追加一个文件到已经存在的文件内容的末尾***

hadoop fs -appendtofile xiaobaiw.txt(本地文件) /bigdata/xiaobaic.txt(HDFS目标文件)

### 下载

***-copytolocal:从HDFS拷贝到本地***

hadoop fs -copytolocal /bigdata/xiaobaic.txt(HDFS目标文件路径) /opt/module/hadoop-3.1.3/(本地保存路径)

***-get:等同于copytolocal,生产环境更习惯用get*** *  

hadoop fs -get /bigdata/xiaobaic.txt(HDFS目标文件路径) /opt/module/hadoop-3.1.3/xiaobaic2.txt(本地保存路径)

### 在HDFS上的直接操作

***-ls:显示目录信息***

hadoop fs -ls /bigdata/(目录)

***-cat:显示文件内容***

hadoop fs -cat /bigdata/xiaobaic.txt(文件)

***-chgrp、-chmod、-chown:修改文件所属权限***

hadoop fs -chmod 666 /bigdata/xiaobaic.txt(赋予文件666的权限即: rw-rw-rw-)

***-mkdir:创建路径***

hadoop fs -mkdir /student(创建的目录)

***-cp:从HDFS的一个路径拷贝到HDFS的另一个路径***

hadoop fs -cp /bigdata/xiaobaic.txt(拷贝) /student(拷贝到)

***-mv:在HDFS目录中移动文件***

hadoop fs -mv /bigdata/xiaobaij.txt(移动的文件) /student(移动到的路径)

***-tail:显示一个文件的末尾1kb的数据***

hadoop fs -tail /bigdata/xiaobaic.txt(查看的文件)

***-rm：删除文件或文件夹***  

hadoop fs -rm /bigdata/xiaobaic.txt(删除的文件)

***-rm -r：递归删除目录及目录里面内容***  

hadoop fs -rm -r /bigdata(递归删除)


***-du：统计文件夹的大小信息***  

hadoop fs -du -s -h /student(目标文件夹)

***-setrep：设置HDFS中文件的副本数量***  

hadoop fs -setrep 10 /student/xiaobaic.txt


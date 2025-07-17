1、DDL数据定义
数据库
创建数据库
语法：
CREATE DATABASE [IF NOT EXISTS] database_name
[COMMENT database_comment]
[LOCATION hdfs_path]
[WITH DBPROPERTIES (property_name=property_value, ...)];
eg：
-- 创建一个数据库，不指定路径
create database db_test1;
-- 注：若不指定路径，其默认路径为${hive.metastore.warehouse.dir}/database_name.db
-- 创建一个数据库，指定路径
-- create database db_test2 location '/db_test2';
-- 创建一个数据库，带有dbproperties
create database db_test3 with dbproperties('create_date'='2025-06-12');
查询数据库
● 显示所有数据库
语法：
SHOW DATABASES [LIKE 'identifier_with_wildcards'];
-- 注：like通配表达式说明：*表示任意个任意字符，|表示或的关系。
eg：
show databases like 'db_test*';
● 查看数据库信息
语法：
DESCRIBE DATABASE [EXTENDED] db_name;
eg：
-- 查看基本信息
desc database db_test3;
-- 查看更多信息
desc database extended db_hive3;
修改数据库
语法:
-- 修改dbproperties
ALTER DATABASE database_name SET DBPROPERTIES (property_name=property_value, ...);
-- 修改location
ALTER DATABASE database_name SET LOCATION hdfs_path;
-- 修改owner user
ALTER DATABASE database_name SET OWNER USER user_name;
eg：
-- 修改dbproperties
ALTER DATABASE db_test3 SET DBPROPERTIES ('create_date'='2025-06-13');
删除数据库
语法:
DROP DATABASE [IF EXISTS] database_name [RESTRICT|CASCADE];
注：
restrict：严格模式，若数据库不为空，则会删除失败，默认为该模式。
cascade：级联模式，若数据库不为空，则会将库中的表一并删除。
eg:
-- 删除空数据库
drop database db_test2;
-- 删除非空数据库
drop database db_test3 cascade;
切换当前数据库
语法：
USE database_name;
表
创建表
语法：
● 普通建表
● EXTERNAL与之对应的就是管理表（内部表）。管理表也就意味着hive会完全接管该表，包括元数据和hdfs中的数据，外部表hive只接管元数据，而不完全接管hdfs中的数据
● data_type 
  ○ tinyint、smallint、int、bigint
  ○ boolean
  ○ float
  ○ double
  ○ decimal
  ○ string
  ○ timestamp
  ○ binary
  ○ 复杂的数据类型：array、map、struct
    ■ array<string> 
    ■ map<string,int> 
    ■ struct<id:int,name:string>
● ROW FORMAT *
  ○ FIELDS DELIMITED TERMINATED BY  列的分隔符
  ○ collection items TERMINATED BY :array、map、struct中每个元素之间的分隔符
  ○ map keys TERMINATED BY :map中key与value分隔符
  ○ lines TERMINATED BY :行分隔符
● STORED AS 文件格式
● LOCATION 指定表对应的hdfs路径
● TBLPROPERTIES ：配置表的一些创建kv参数
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name   
[(col_name data_type [COMMENT col_comment], ...)]
[COMMENT table_comment]
[PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
[CLUSTERED BY (col_name, col_name, ...) 
[SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS]
[ROW FORMAT row_format] 
[STORED AS file_format]
[LOCATION hdfs_path]
[TBLPROPERTIES (property_name=property_value, ...)]
● Create Table As Select（CTAS）建表
CREATE [TEMPORARY] TABLE [IF NOT EXISTS] table_name 
[COMMENT table_comment] 
[ROW FORMAT row_format] 
[STORED AS file_format] 
[LOCATION hdfs_path]
[TBLPROPERTIES (property_name=property_value, ...)]
[AS select_statement]
● Create Table Like语法
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name
[LIKE exist_table_name]
[ROW FORMAT row_format] 
[STORED AS file_format] 
[LOCATION hdfs_path]
[TBLPROPERTIES (property_name=property_value, ...)]
-- 临时表  仅存在当前会话
create TEMPORARY table IF NOT EXISTS bigdata.student1(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
);

-- 内部表（管理表）
create table if not exists bigdata.student2(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
);
-- 外部表
create EXTERNAL table if not exists bigdata.student3(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
);


-- 省略
-- 临时表  仅存在当前会话
create TEMPORARY table student1(
  id string,
  name string,
  age int,
  sex string,
  clazz string
);
-- 内部表（管理表）
create table student2(
  id string,
  name string,
  age int,
  sex string,
  clazz string
);

-- 外部表
create EXTERNAL table student3(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
);



-- Create Table As Select（CTAS）建表
create table student4 as select * from student2;


-- Create Table Like
create table student5 like student2;




查看表
● 显示所有表
语法：
SHOW TABLES [IN database_name] LIKE ['identifier_with_wildcards'];
● 查看表信息
语法：
DESCRIBE [EXTENDED | FORMATTED] [db_name.]table_name
EXTENDED：展示详细信息
FORMATTED：对详细信息进行格式化的展示
修改表
● 重命名表
语法：
ALTER TABLE table_name RENAME TO new_table_name
● 修改列信息
-- 增加列
-- 该语句允许用户增加新的列，新增列的位置位于末尾。
ALTER TABLE table_name ADD COLUMNS (col_name data_type [COMMENT col_comment], ...)
-- 更新列
-- 该语句允许用户修改指定列的列名、数据类型、注释信息以及在表中的位置。
ALTER TABLE table_name CHANGE [COLUMN] col_old_name col_new_name column_type [COMMENT col_comment] [FIRST|AFTER column_name]
-- 替换列
-- 该语句允许用户用新的列集替换表中原有的全部列。
ALTER TABLE table_name REPLACE COLUMNS (col_name data_type [COMMENT col_comment], ...)
删除表
语法：
DROP TABLE [IF EXISTS] table_name;
清空表
语法：
TRUNCATE [TABLE] table_name
注意：truncate只能清空管理表，不能删除外部表中数据。

---- 内部表（管理表）
create table if not exists bigdata.student9(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
row format DELIMITED fields terminated by ',';

-- 外部表
create EXTERNAL table if not exists bigdata.student8(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
row format DELIMITED fields terminated by ',';



create table if not exists bigdata.student7(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
row format DELIMITED fields terminated by ','
location '/bigdata/student7';



create table if not exists bigdata.student6(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
row format DELIMITED fields terminated by ','
location '/data/student6';



create table if not exists bigdata.student4(
  id string comment '学号',
  name string comment '姓名',
  age int comment '年龄',
  sex string comment '性别',
  clazz string comment '班级'
)
row format DELIMITED fields terminated by ',';


insert into table student5
select
  *
from student6;



insert into table student4 values('1500100001','施笑槐',22,'女','文科六班');



insert into table student4(id,name,age) values('1500101005','张三',23);
2、DML数据操作
Load
语法：
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] INTO TABLE tablename [PARTITION (partcol1=val1, partcol2=val2 ...)];
Insert
（1）将查询结果插入表中
语法：
INSERT (INTO | OVERWRITE) TABLE tablename [PARTITION (partcol1=val1, partcol2=val2 ...)] select_statement;
（2）将给定Values插入表中
语法：
INSERT (INTO | OVERWRITE) TABLE tablename [PARTITION (partcol1[=val1], partcol2[=val2] ...)] VALUES values_row [, values_row ...]
（3）将查询结果写入目标路径
语法：
INSERT OVERWRITE [LOCAL] DIRECTORY directory
[ROW FORMAT row_format] [STORED AS file_format] select_statement;
Export&Import
语法：
--导出
EXPORT TABLE tablename TO 'export_target_path'

--导入
IMPORT [EXTERNAL] TABLE new_or_original_tablename FROM 'source_path' [LOCATION 'import_target_path']
3、分区表和分桶表
分区表
语法：
create table dept_partition
(
deptno int,    --部门编号
dname  string, --部门名称
loc    string  --部门位置
)
partitioned by (day string)
row format delimited fields terminated by '\t';
分区表读写数据：
● 写数据
-- load
-- insert
● 读数据
select deptno, dname, loc ,day
from dept_partition
where day = '2025-06-12';
分区表基本操作:
-- 查看所有分区信息
show partitions dept_partition;
-- 增加分区
-- --创建单个分区 
alter table dept_partition 
add partition(day='20250612');
-- --同时创建多个分区（分区之间不能有逗号）
alter table dept_partition 
add partition(day='20250612') partition(day='20250612');
-- 删除分区
-- --删除单个分区
alter table dept_partition 
drop partition (day='20250612');
-- --同时删除多个分区（分区之间必须有逗号）
alter table dept_partition 
drop partition (day='20250612'), partition(day='20250612');
-- 修复分区
Hive将分区表的所有分区信息都保存在了元数据中，只有元数据与HDFS上的分区路径一致时，分区表才能正常读写数据。若用户手动创建/删除分区路径，Hive都是感知不到的，这样就会导致Hive的元数据和HDFS的分区路径不一致。再比如，若分区表为外部表，用户执行drop partition命令后，分区元数据会被删除，而HDFS的分区路径不会被删除，同样会导致Hive的元数据和HDFS的分区路径不一致。
若出现元数据和HDFS路径不一致的情况，可通过如下几种手段进行修复。
（1）add partition
若手动创建HDFS的分区路径，Hive无法识别，可通过add partition命令增加分区元数据信息，从而使元数据和分区路径保持一致。
（2）drop partition
若手动删除HDFS的分区路径，Hive无法识别，可通过drop partition命令删除分区元数据信息，从而使元数据和分区路径保持一致。
（3）msck
若分区元数据和HDFS的分区路径不一致，还可使用msck命令进行修复，以下是该命令的用法说明。
msck repair table table_name [add/drop/sync partitions];
说明：
msck repair table table_name add partitions：该命令会增加HDFS路径存在但元数据缺失的分区信息。
msck repair table table_name drop partitions：该命令会删除HDFS路径已经删除但元数据仍然存在的分区信息。
msck repair table table_name sync partitions：该命令会同步HDFS路径和元数据分区信息，相当于同时执行上述的两个命令。
msck repair table table_name：等价于msck repair table table_name add partitions命令。
二级分区表
语法：
hive (default)>
create table dept_partition2(
deptno int,    -- 部门编号
dname string, -- 部门名称
loc string     -- 部门位置
)
partitioned by (day string, hour string)
row format delimited fields terminated by '\t';
分桶表
语法：
create table stu_buck(
id int, 
name string
)
clustered by(id) 
into 4 buckets
row format delimited fields terminated by '\t';
分桶排序表
语法：
create table stu_buck_sort(
id int, 
name string
)
clustered by(id) sorted by(id)
into 4 buckets
row format delimited fields terminated by '\t';
4、Hive文件格式
Text File
create table bigdata.students_textfile(
    id STRING comment '学号',
    name STRING comment '姓名',
    age INT comment '年龄',
    sex STRING comment '性别',
    clazz STRING comment '班级'
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/data/bigdata/students_textfile';
ORC
Parquet
5、压缩





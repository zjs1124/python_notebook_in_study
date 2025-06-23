/*
DML语言
插入：insert
修改：update
删除：delete

1、插入语句
方式一：经典的插入语句 *
语法：
insert into 表名(列名,...) values(值1,...);
方式二：
语法：
insert into 表名
set 列名=值,列名=值,......
方式一和方式二对比：
(1)方式一支持插入多行，方式二不支持；
(2)方式一支持子查询，方式二不支持；

2、修改语句
（1）修改单表的记录*
语法：
update 表名（1）
set 列=新值，列=新值,......（3）
where 筛选条件；（2）
（2）修改多表的记录（补充）
sql92语法：
update 表1 别名，表2 别名
set 列=值,......
where 连接条件
and 筛选条件；

sql99语法：
update 表1 别名
inner ｜left｜right join 表2 别名
on连接条件
set 列=值,......
where 筛选条件;

3、删除语句
方式一：delete

（1）单表删除（*）
语法：	
delete from 表名 where 筛选条件；
（2）多表删除（补充）
sql92语法：
delete 表1的别名，表2的别名
from 表1 别名，表2 别名
where 连接条件
and 筛选条件；


sql99语法：
delete 表1的别名 ，表2的别名
from 表1 别名
inner ｜ left｜right join 表2 别名 on 连接条件
where 筛选条件；

方式二：truncate
语法：
truncate table 表名；
delete和truncate对比：
（1）delete可以加where条件，truncate不能加
（2）truncate删除，效率高一点
（3）加入要删除的表中有自增长列，如果用delete删除后，再插入数据，自增长列的值从断点开始，
而truncate删除后，再插入数据自增长列的值从1开始
（4）truncate删除没有返回值，delete删除有返回值
（5）truncate删除不能回滚，delete删除可以回滚


*/


# 插入语句
# 插入的值类型要与列的类型一致或兼容

/*
CREATE TABLE `beauty` (
  `id` int DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `sex` char(1) DEFAULT (_utf8mb4'女'),
  `boyfriend_id` int DEFAULT NULL,
  `borndate` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
*/

-- -----------------------方式一----------------------------------------
INSERT INTO beauty (id,`name`,sex,boyfriend_id,borndate,phone,photo)
VALUES(1,'章子怡','女',1,'1979-02-09','13888888888',NULL)


# 不可以为null的列必须插入值，可以为null的列如何插入值？

INSERT INTO beauty (id,`name`,sex,boyfriend_id,phone)
VALUES(2,'唐艺昕','女',1,'15288888888')


# 列的顺序是可以调换的
INSERT INTO beauty (`name`,sex,phone,id)
VALUES('毛晓彤','女','19888888888',3)

# 列数和值的个数必须一致，不然报错

-- INSERT INTO beauty (`name`,sex,phone,id)
-- VALUES('毛晓彤','女','19888888888',3,'1979-02-09')

-- 1136 - Column count doesn't match value count at row 1

# 可以省列名、默认所有列，而且列的顺序和表中列的顺序一致
INSERT INTO beauty (id,`name`,sex,boyfriend_id,borndate,phone,photo)
VALUES(4,'关晓彤','女',2,NULL,'19288888888',NULL)


INSERT INTO beauty 
VALUES(6,'张静怡','女',3,NULL,'15288888888',NULL)

-- -----------------------方式二----------------------------------------
INSERT INTO beauty
SET id=5,`name`='金晨',phone='15277777777';


-- 方式一和方式二对比
# 1、方式一支持插入多行，方式二不支持；
INSERT INTO beauty
VALUES ( 7, '章子怡1', '女', 1,'1979-02-09', '13888888888', NULL  )
,( 8, '章子怡2', '女', 1,'1979-02-09', '13888888888', NULL )
,( 9, '章子怡3', '女', 1,'1979-02-09', '13888888888', NULL );

-- INSERT INTO beauty
-- SET id=10,`name`='金晨1',phone='15277777777' ,
-- SET id=11,`name`='金晨2',phone='15277777777';



# 2、方式一支持子查询，方式二不支持；

INSERT INTO beauty(id,name,phone)
SELECT 22,'辛梓蕾','17888888888';



-- ---------------------------修改---------------------------------------
-- 修改单表的记录
# eg 修改beauty表中姓章的女神的电话为：19988888881
UPDATE beauty SET phone = '19988888881'
WHERE
  `name` LIKE '章%';

SELECT * FROM beauty

# eg 修改boys表中id号为3的名称为：李晨，魅力值为50
UPDATE boys SET boyName = '李晨',userCP = 50
WHERE
  id = 3

-- 修改多表的记录
# eg 修改汪峰的女朋友们的手机号为119
UPDATE boys bo 
INNER JOIN beauty b 
ON bo.id = b.boyfriend_id
SET phone = '119'
WHERE
  bo.boyName = '汪峰'

# 修改没有男朋友的女神的男朋友编号都为3
UPDATE beauty 
SET boyfriend_id = 3
WHERE
  boyfriend_id IS NULL;


-- -------------------------删除------------------------------------
-- 方式一 delete
# 单表删除
# eg 删除手机号以19开头的女神信息
DELETE FROM beauty WHERE phone LIKE '19%';

# 多表删除
# 删除汪峰女朋友的信息
DELETE b
FROM
  beauty b 
INNER JOIN boys bo 
ON b.boyfriend_id = bo.id
WHERE
  bo.boyName = '汪峰'

-- 方式二 truncate
# eg 将魅力值大于100的男神信息删除
truncate TABLE boys WHERE userCP > 100;  -- 报错
truncate TABLE boys;

SELECT * FROM boys

INSERT INTO boys(boyName,userCP) VALUES('李四',1800);
INSERT INTO boys(boyName,userCP) VALUES('李四',1700);
INSERT INTO boys(boyName,userCP) VALUES('李四',1800);


/*
1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'WHERE userCP > 100' at line 1

*/

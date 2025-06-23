/*
常见函数
概念：将一组逻辑语句封装在方法提中，对外暴露方法名。类似于python中的方法
好处：
1、隐藏了实现细节
2、提高代码的重用性
调用：select 函数名(实参列表) [ from 表名];
特点：
1、叫什么（函数名称）
2、干什么（函数功能）
分类：
1、单行函数
如：concat、ifnull、length
包含：字符函数、数学函数、日期函数、其他函数、流程控制函数-if函数、流程控制函数-case结构
2、分组函数
功能：做统计使用又称统计函数（聚合函数、组函数）。
*/

/*
字符函数
*/
-- 1、length():获取参数值的字节个数
# 注意：对于非ASCII字符（如汉字），length函数返回的不是字符的个数，而是字符串的字节数

# 使用CHAR_LENGTH() 计算字符串中的字符的数量（即字符长度）
SELECT LENGTH('hello');
SELECT LENGTH('你好hello')
SELECT CHAR_LENGTH('你好hello');


-- show VARIABLES LIKE '%char%';
show variables

-- 2、concat():凭借字符串
# concat函数用于将两个或多个字符串连接成一个字符串。
# 它可以连接任意数量的字符串，并且返回一个组合后的字符串。
# concat_ws()函数：用于指定分隔符连接字符串。
SELECT concat(last_name,'_',first_name) FROM employees;

SELECT CONCAT_WS('-','2025','05','27');

-- 3、upper 、lower
# upper：函数用于将字符串转换为大写
# lower：函数用于将字符串转换为小写
SELECT UPPER('hello');
SELECT LOWER('HELLO');

-- 能不能首字母大写
SELECT
  CONCAT(UPPER(last_name),'_',LOWER(first_name)) AS 姓名
FROM
  employees;


-- substr、substring
# substr：函数用于从字符串中提取子串
# substring ：原始字符串
# start_position :子字符串的起始位置 从1开始


# eg:截取从指定索引处后面的所有字符串
SELECT
  SUBSTR('欢迎来到兰智数加学院',7) out_put;
  
# eg:截取从指定索引处指定字符串的长度字符
SELECT
  SUBSTR('欢迎来到兰智数加学院',7,2) out_put;


# eg:姓名中的姓首字符大写，其他字符小写，然后用_拼接，显示为out_put

-- 思考：K_ing  ---> K__ing  如何处理？
# De Haan
SELECT
  CONCAT(UPPER(SUBSTR(last_name,1,1)),'_',LOWER(SUBSTR(last_name,2))) AS out_put
FROM
  employees;


-- instr ：返回字串第一次出现的索引，如果找不到则返回0
# INSTR 函数用于返回一个子字符串在另一个字符串中第一次出现的位置。
        # 如果找不到则返回0，不区分大小写
SELECT 
  INSTR('AAaBbbbb','a') out_put;



-- trim 
# trim：函数用于删除字符串开头和结尾的空格字符串或其他指定字符。
-- str ：要进行修剪的字符串
-- remstr：要删除的字符。如果省略，默认删除空格字符。
-- BOTH：删除字符串开头和结尾的指定字符（默认）
-- LEADING：仅删除字符串开头的指定字符。
-- TRAILING：仅删除字符串结尾的指定字符。
SELECT
  LENGTH(TRIM('   数加   ')) out_put;
  
-- lpad :用于指定字符串实现左填充指定长度
# string 要进行填充的原始字符串
# length 填充后的字符串总长度
# pad_string 用于填充的字符


-- 思考：18000***9999
SELECT
  LPAD('数加',4,'*') as out_put;

SELECT
  RPAD('数加',5,'*')as out_put;


-- replace替换
SELECT
  REPLACE('欢迎来到兰智数加学院','学院','大学') as out_put;



/*
数学函数
*/

-- round
# round函数用于将数值四舍五入到指定的小数位数
# 语法：参数1：要进行四舍五入的数值；参数2要保留小数位数。
# 注意：参数2如果默认，则取整
SELECT ROUND(12.2345,2) as output;
SELECT ROUND(12.2345);

-- ceil
# ceil函数用于将数值向上取整，返回大于或等于该数值的最小整数
# 语法：参数1要向上取整的数值
SELECT CEIL(12.14);


-- floor
# floor函数用于将数值向下取整，返回小于或等于该数值的最大整数
# 语法参数1要向下取整的数值
SELECT FLOOR(-123.456)


-- truncate
# truncate函数用于将数值截断到指定的小数位数，直接去掉多余的小数位而不进行四舍五入
# 语法：X：要截断的数值；D：保留的小数位数

SELECT TRUNCATE(123.456,1)
SELECT TRUNCATE(123.456,0)


-- mod 取余
# mod函数用于计算两个数之间的余数（模运算）
# 语法  N：被除数   M：除数
-- MOD(N,M) 返回 N 除以 M 的余数 ，如果M为0，则返回 null

SELECT 10 % 3;
SELECT MOD(10,0) as out_put;


/*
日期函数
*/
-- now
# now函数用于返回当前的日期和时间
# 语法 now()
# 返回的结果：年月日时分秒    YYYY-MM-DD HH:MM:SS
SELECT NOW();


-- curdate
# curdate 函数用于返回当前的日期，不包括时间部分
# 返回的结果：年月日 YYYY-MM-DD
SELECT CURDATE();

-- curtime
# curtime 函数用于返回当前的时间，不包括日期部分
# 返回的结果：时分秒 HH:MM:SS
SELECT CURTIME();



# eg ：获取指定的年 月 日 时 分 秒 

-- 获取年
SELECT YEAR(NOW()) AS 年;

SELECT YEAR('2025-05-27') AS 年;

SELECT YEAR(hiredate) as 年 FROM employees;


-- 获取月
SELECT MONTH(NOW()) AS 月;
SELECT MONTH('2025-05-27') AS 月;

SELECT MONTHNAME(NOW()) AS mon_name;

-- 获取日
SELECT DAY(NOW()) as 日;

SELECT DAYNAME(NOW()) as day_name;


-- 获取小时
SELECT HOUR(NOW()) AS 时;

-- 获取分钟
SELECT MINUTE(NOW()) as 分;

-- 获取秒
SELECT SECOND(NOW()) as 秒;



-- str_to_date  (**)
# str_to_date 函数用于将字符串转换为日期和时间格式
# 语法： str：要转换的时间字符串；format：指定的字符串格式

-- 格式化符号：
# %Y :四位数字的年份
# %y :两位数字的年份
# %m :两位数字的月份（01~12）
# %cc :月份，数值（0~12）
# %d :两位数的日期，（00~31）
# %e :日期，数值（0~31）
# %H :两位数字的小时 24小时制（00 ~23）
# %h :两位数字的小时 12小时制 （01~12）
# %i :两位数字的分钟，（00~59）
# %s :两位数字的秒（00~59）
# p: AM or PM

SELECT STR_TO_DATE('2025-05-27','%Y-%m-%d') as out_put;


# eg:查询入职日期为1992-4-3的员工信息
SELECT
  *
FROM
  employees
WHERE
  hiredate = '1992-4-3';
  
SELECT
  *
FROM
  employees
WHERE
  hiredate = STR_TO_DATE('4-3 1992','%c-%d %Y') ;



-- date_format
# date_format 函数用于将日期或日期时间值格式化为指定的字符串格式
# 语法：DATE_FORMAT() date：要格式化的日期或日期时间值；format：指定结果字符串格式
-- 格式化符号：
# %Y :四位数字的年份
# %y :两位数字的年份
# %m :两位数字的月份（01~12）
# %cc :月份，数值（0~12）
# %d :两位数的日期，（00~31）
# %e :日期，数值（0~31）
# %H :两位数字的小时 24小时制（00 ~23）
# %h :两位数字的小时 12小时制 （01~12）
# %i :两位数字的分钟，（00~59）
# %s :两位数字的秒（00~59）
# p: AM or PM
# %W：星期名称（Sunday 到 Saturday）。
# %w：星期中的天（0 = Sunday, 6 = Saturday）。
# %j：一年中的天数（001 到 366）。

SELECT DATE_FORMAT(now(),'%y年%m月%d日') as out_put;


# eg:查询有奖金的员工名和入职日期（xx月/xx日 xx年）
# 员工名 first_name
# 入职日期 hiredate

SELECT
  first_name,
  DATE_FORMAT(hiredate,'%m月/%d日 %y年')
FROM
  employees
WHERE
  commission_pct is not NULL;


/*
其他函数
*/
-- version()
# version()函数返回当前mysql的服务器的版本

SELECT VERSION();

-- user()
# user() 函数返回当前mysql会话的用户和主机信息
SELECT USER();


/*

流程控制函数
*/
-- if函数
#if函数是用于在查询中进行条件判断的流程控制函数
# 语法：IF(expr1,expr2,expr3)
# expr1要评估的表达式，如果条件为真（非零或非空），则返回true_value,，否则返回false_value
# expr2 条件为真时，要返回的值
# expr3条件为假时，要返回的值
SELECT IF(2<3,'大','小');    

# eg:查询员工的姓和名以及奖金率，如果有奖金率则返回有，没有则返回无并以备注为列名
SELECT
  last_name,
  first_name,
  commission_pct,
  IF(commission_pct IS NULL,'无奖金','有奖金') AS 备注
FROM
  employees;



-- case 函数（结构）
# case函数：函数或者表达式，是一种流程控制函数，类似于java语言中的switch语句
/*
简单形式：
CASE case_expression
    WHEN when_expression1 THEN result1
    WHEN when_expression2 THEN result2
    ...
    ELSE else_result
END


其中：
  case_expression：需要进行比较的表达式或列。
  when_expression1, when_expression2, ...：与 case_expression 进行比较的表达式或值。
  result1, result2, ...：当 case_expression 等于 when_expression 时返回的结果。
  else_result：如果没有 when_expression 匹配时返回的默认结果。

搜索形式：
CASE
    WHEN condition1 THEN result1
    WHEN condition2 THEN result2
    ...
    ELSE else_result
END
其中：
  condition1, condition2, ...：条件表达式，可以是任何布尔表达式。
  result1, result2, ...：当条件表达式为真时返回的结果。
  else_result：如果没有条件表达式为真时返回的默认结果。
*/


/*
eg 查询员工的工资，要求：
（1）部门号=30，显示的工资为1.1倍
（2）部门号=40，显示的工资为1.2倍
（3）部门号=50，显示的工资为1.3倍
（4）其他部门，显示的工资为原工资
*/ 

-- 简单形式
/*
分析：
  查询的表： employees
  查询的字段：
              salary
              department_id
              新工资  case。。。。。。
  
  查询的条件： 无
  排序的条件：无
*/
SELECT
  salary,
  department_id,
--   as 新工资
  CASE department_id
    WHEN 30 THEN
      salary * 1.1
    WHEN 40 THEN
      salary * 1.2
    WHEN 50 THEN
      salary * 1.3
    ELSE
      salary
  END AS 新工资
FROM
  employees;


-- -------------------
SELECT
  salary,
  department_id,
--   as 新工资
  CASE 
    WHEN department_id=30 THEN
      salary * 1.1
    WHEN department_id=40 THEN
      salary * 1.2
    WHEN department_id=50 THEN
      salary * 1.3
    ELSE
      salary
  END AS 新工资
FROM
  employees;


-- -------------------

-- 搜索形式
/*
eg 查询员工的工资的情况
（1）如果工资大于20000，显示A级别
（2）如果工资大于15000，显示B级别
（3）如果工资大于10000，显示C级别
（4）否则，显示D级别
*/

SELECT salary, --   工资的级别
CASE WHEN salary > 20000 THEN
  'A' 
  WHEN salary > 15000 THEN
  'B' 
  WHEN salary > 10000 THEN
  'C' ELSE 'D' 
END AS 工资级别 
FROM
  employees;
  


-- 1. 显示系统时间(注：日期+时间)
SELECT NOW();
-- 2. 查询员工号，姓名，工资，以及工资提高百分之 20%后的结果（new salary）
SELECT
  employee_id,
  CONCAT(last_name,first_name) AS '姓名',
  salary,
  salary * 1.2 AS 'new_salary'
FROM
  employees;


-- 3. 将员工的姓名按首字母排序，并写出姓名的长度（length）
SELECT
  LENGTH(CONCAT(last_name,first_name)) AS 长度,
--   SUBSTR(CONCAT(last_name,first_name),1,1)  AS 首字母,
  CONCAT(last_name,first_name) AS 姓名
FROM
  employees
ORDER BY SUBSTR(CONCAT(last_name,first_name),1,1);

/*4. 做一个查询，产生下面的结果
<last_name> earns <salary> monthly but wants <salary*3>
              Dream Salary
King earns 24000 monthly but wants 72000
*/

SELECT
  CONCAT(last_name,' earns ',salary,' monthly but wants ',salary*3) AS 'Dream Salary'
FROM
  employees;






/*5. 使用 case-when，按照下面的条件：
    job 			grade
    AD_PRES 		A
    ST_MAN 			B
    IT_PROG 		C
    SA_REP 			D
    ST_CLERK 		E
    产生下面的结果:
    Last_name 	Job_id 		Grade
      king 			AD_PRES 		A
*/
















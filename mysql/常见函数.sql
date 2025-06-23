/*
常见函数
概念：将一组逻辑语句封装在方法体中,对外暴露方法名，类似于python中的方法
好处：
1、隐藏了实现细节
2、提高了代码重用性
调用：
select 
函数名(实参列表)
[from 表名]
特点：
1、叫什么(函数名称)
2、干什么(函数功能)
分类:
1、单行函数
如:concat、ifnull、length
包含:字符函数、数学函数、日期函数、其他函数、流程控制函数-if函数、流程控制函数-case结构
2、分组函数
功能:做统计使用又称为统计函数(聚合函数、组函数)
*/

/*
字符函数
1、length():获取参数值的字节个数
注意: 对于非ASCII字符(如汉字),length函数返回的不是字符的个数,而是字节数

使用char_length() 计算字符串中的字符的数量(即字符长度)
*/
select length('hello');

select length('你好hello') select char_length('你好hello');

-- 2、concat()：凭借字符串
# concat函数用于将两个或多个字符串连接成一个字符串。
# 它可以连接任意数量的字符串，并且返回一个组合后的字符串。
# concat_ws()函数：用于指定分隔符连接字符串。

select 
    concat(last_name,"_",first_name)
from 
    employees;

select concat_ws('-', '2025', '05', '27');

-- 3、upper()、lower()
# upper : 函数用于将字符串转换为大写
# lower : 函数用于将字符串转换为小写

select upper('hello');

select lower('HELLO');
-- substr、substring
# substr:函数用于从字符串中提取子串
# substring : 原始字符串
# start_position : 子字符串的起始位置 从1开始

# eg:截取从指定索引处后面的所有字符串
select 
    substr('欢迎来到兰智数加学院',7) out_put;
#数加学院

# eg:截取从指定索引处指定字符串的长度字符
select
    substr('欢迎来到兰智数加学院',7,2) out_put;
# 数加

# eg:姓名中的姓首字母大写,其他字符小写，然后用_拼接,显示为out_put

-- 思考: K_ing ---> K__ing 如何处理？
select if(
        substr(last_name, 2, 1) = '_', concat(
            upper(substr(last_name, 1, 1)), lower(substr(last_name, 2))
        ), concat(
            upper(substr(last_name, 1, 1)), "_", lower(substr(last_name, 2))
        )
    )
from employees;
#De Haan

select  
    concat(upper(substr(last_name,1,1)),'_',lower(substr(last_name,2))) as out_put
from 
    employees;

-- instr : 返回字串第一次出现的索引,如果找不到则返回e
# instr 函数用于返回一个子字符串在另一个字符串中第一次出现的位置。
# 如果找不到则返回0,不区分大小写

select 
    instr('AAaBbbb','a') out_put;

-- trim
# trim:函数用于删除字符串开头和结尾的空格字符串或其他指定字符串。
--str : 要进行修剪的字符串
-- remstr : 要删除的字符。如果省略,默认删除空格字符串。
-- both：删除字符串开头和结尾的指定字符（默认）
-- leading : 仅删除字符串开头指定字符
-- trailing:仅删除字符串结尾的指定字符
select
    -- char_length(trim(' 数加  ')) out_put;
    -- char_length(trim(both ' ' from '  数加  ')) output
    -- char_length(trim(leading ' ' from '  数加  ')) output;
    char_length(
        trim(
            trailing ' '
            from '  数加  '
        )
    ) output;

-- lpad : 用于指定字符串实现左填充指定长度
# string 要进行填充的原始字符串
# length 填充后的字符串总长度
# pad_string 用于填充的字符

-- 思考: 18000***9999
select lpad('数加', 4, '*') as out_put;

select rpad('数加', 4, '*') as out_put;

-- replace替换
select replace ('欢迎来到兰智数加学院', '学院', '大学') as out_Put;

/*
数学函数
*/

-- round
# round函数用于将数值四舍五入到指定的小数位数
# 语法: 参数1 : 要进行四舍五入的数值，参数2: 要保留的是小数位数
# 注意: 参数2如果默认,则取整

select 
    -- round(12.2345,2) as output;
    round(12.2345) as output;

-- ceil
# ceil函数用于将数值向上取整,返回大于或等于该数值的最小整数
# 语法： 参数1：要向上取整的数值

select
    ceil(12.14);

-- floor
# floor函数用于将数值向下取整,返回小于或等于该数值的最大整数
# 语法: 参数1 : 要向下取整的数值

select
    floor(-123.456)

-- truncate
# truncate 函数用于将数值截断到指定的小数位数,直接去掉多余的小数位而不进行四舍五入
# 语法: x:要截断的数值 D:保留的小数位数

select 
    truncate(123.456,1)

select truncate (123.456, 0)

-- mod 取余
# mod函数用于计算两个数之间的余数(模运算)
# 语法  N：被除数   M：除数

-- mod(N,M) 返回N除以M的余数, 如果M为0，则返回null

select 10 % 3;

select MOD(10, 3) as output;

/*
日期函数
*/

-- now()
# now函数用于返回当前的日期和时间
# 语法 now()
# 返回的结果: 年 月 日 时 分 秒  YYYY-MM-DD HH:MM:SS

select 
    now();

-- curdate
# curdate 函数用于返回当前的日期，不包括时间部分
# 返回的结果: 年月日 YYYY-MM-DD

select
    curdate();

-- curtime
# curtime 函数用于返回当前的时间,不包括日期部分
# 返回的结果: 时分秒 HH:MM:SS
select 
    curtime();

# eg: 获取指定的年月日时分秒

-- 获取年
select year(now()) as '年';

-- 获取月
select month(now()) as '月';

select monthname(now()) as '月';

-- 获取日
select day(now()) as '日';

select dayname(now()) as day_name;

-- 获取小时
select hour(now()) as '时';

-- 获取分钟
select minute(now()) as '分';

-- 获取秒

select second(now()) as '秒';

-- str_to_date (**)
# str_to_date 函数用于将字符串转换为日期和时间格式
# 语法： str : 要转换的时间字符串: format: 指定的字符串格式

-- 格式化符号:
# %Y : 四位数字的年份
# %y : 两位数字的年份
# %m : 两位数字的月份(01~12)
# %c : 月份，数值（0~12）
# %d ：两位数的日期 (00~31)
# %e : 日期，数值(0~31)
# %H : 两位数字的小时 24小时制 (00~23)
# %h : 两位数字的小时 12小时制 (01~12)
# %i : 两位数字的分钟 (00~59)
# %s : 两位数字的秒 (00~59)
# p :AM or PM

select
    str_to_date('2025-05-27','%Y-%m-%d') as output;

# eg:查询入职日期为1992-4-3 的员工信息

select
    *
from
    employees
where
    hiredate = '1992-4-3';

select *
from employees
where
    hiredate = str_to_date('4-3 1992', '%c-%d %Y');

-- date_format
# date_format 函数用于将日期或日期时间值格式化为指定的字符串格式
# 语法:date_format()
# date： 要格式化的日期或日期时间值;
# format: 指定结果字符串格式
-- 格式化符号:
# %Y : 四位数字的年份
# %y : 两位数字的年份
# %m : 两位数字的月份(01~12)
# %c : 月份，数值（0~12）
# %d ：两位数的日期 (00~31)
# %e : 日期，数值(0~31)
# %H : 两位数字的小时 24小时制 (00~23)
# %h : 两位数字的小时 12小时制 (01~12)
# %i : 两位数字的分钟 (00~59)
# %s : 两位数字的秒 (00~59)
# p :AM or PM
# %W : 星期名称(sunday 到 saturday)
# %w : 星期中的天 (0 = sunday ,6 = saturday)
# %j : 一年中的天数(001 到 366)

select
    date_format(now(),'%Y年%m月%d日') as out_put;

# eg:查询有奖金的员工名和入职日期(xx月/xx日 xx年)
# 员工名 first_name
# 入职日期 hiredate

select 
    first_name,
    date_format(hiredate,'%m月/%d日 %y年')
from
    employees
where
    commission_pct is not null;

/*
其他函数
-- version()
# version()函数返回当前mysql的服务器的版本
*/
select version();

-- user()
# user() 函数返回当前mysql会话的用户和主机信息
select
    user();

/*
流程控制函数
*/
-- if函数
# if函数是用于在查询中进行条件判断的流程控制函数
# 语法: if(expr1,expr2,expr3)
# expr1要评估的表达式,如果条件为真(非零或非空),则返回true_value,否则返回false_value
# expr2 条件为真,要返回的值
# expr3 条件为假,要返回的值
select if(2 < 3,'小','大');

# eg：查询员工的姓和名以及奖金率,如果有奖金率则返回有，没有则返回无 并以备注为列名

select
    last_name,
    first_name,
    commission_pct,
    if(commission_pct is null ,'无奖金','有奖金') as 备注
from
    employees;

-- case函数
# case函数：函数或者表达式,是一种流程控制函数,类似于java中的switch语句
/*
简单形式:
case case_expression
    when when_expression1 then result1
    when when_expression2 then result2
    ....
    else else_result
end

其中:
    case_expression: 需要进行比较的表达式或列
    when_expression1, when_expression2, ... 与 case_expression 进行比较的表达式或值
    result1,result2, ... 当case_expression 等于 when_expression 时返回的结果.
    else_result: 如果没有when_expression 匹配时返回的默认结果.

搜索形式:
case
    when condition1 then result1
    when condition2 then result2
    ...
    else else_result
end
其中:
    condition1,condition2, ... :条件表达式,可以是任何布尔表达式。
    result1,result2, ... :当条件表达式为为真时返回的结果。
    else_result : 如果没有条件表达式为真时返回默认结果。

*/

/*
eg 查询员工的工资,要求:
(1) 部门号 = 30 ,显示的工资为1.1倍
(2) 部门号 = 40 ,显示的工资为1.2倍
(3) 部门号 = 50 ,显示的工资为1.2倍
(4) 其他部门,显示的工资为原工资
*/

-- 简单形式
/*
分析:
查询的表: employees
查询的字段:
salary
department_id
新工资 case...

查询的条件： 无
排序的条件:  无
*/

select
    salary,
    department_id,
    case department_id
        when 30 then salary * 1.1
        when 40 then salary * 1.2
        when 50 then salary * 1.3
        else salary
    end as '新工资'

select
    salary,
    department_id,
    case
        when department_id = 30 then salary * 1.1
        when department_id = 40 then salary * 1.2
        when department_id = 50 then salary * 1.3
        else salary
    end as 新工资
from employees;

-- 1、显示系统时间(注: 日期和时间)
select now();

-- 2. 查询员工号,姓名,工资,以及工资提高百分之 20后的效果(new salary)

select
    employee_id,
    concat(last_name, first_name) as '姓名',
    salary,
    salary * 1.2 as 'new_salary'
from employees;

-- 3.将员工的姓名按照首字母排序,并写出姓名的长度(length)

select length(concat(last_name, first_name)) as 长度, concat(last_name, first_name) as 姓名
from employees
order by substr(
        concat(last_name, first_name), 1, 1
    );

/*
4. 做一个查询,产生下面的结果
<last_name> earns <salary> monthly but wants <salary * 3>
dream salary
King earns 24000 monthly but wants 72000
*/

select concat(
        last_name, ' earns ', salary, ' monthly but wants ', salary * 3
    ) as 'dream salary'
from employees;

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

select
    last_name,
    job_id,
    case
        when job_id = 'AD_PRES' then 'A'
        when job_id = 'ST_MAN' then 'B'
        when job_id = 'IT_PROG' then 'C'
        when job_id = 'SA_REP' then 'D'
        when job_id = 'ST_CLERK' then 'E'
    end as grade
from employees;

-- ------------------------------------
show tables
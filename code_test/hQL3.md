1、窗口函数的使用
1.1 聚合类的窗口函数
只分组
-- 产生mapreduce的关键字；分组，排序，去重，join
-- 计算每个科目分数占总分的比例
-- 会参数两个MapReduce，执行效率低
select 
    a.id,
    a.cid,
    a.score,
    b.sum_score,
    round(a.score/b.sum_score,4) as p 
from 
bigdata.scores as a
join
(
    select id,sum(score) as sum_score
    from bigdata.scores
    group by id
) as b
on a.id=b.id;




-- sum()
-- 只会产生一个mapreduce，效率高
select
  id,
  cid,
  score,
  sum_score,
  round(score / sum_score,4) as p
from(
  select 
    id,
    cid,
    score,
    sum(score) over(partition by id) as sum_score
  from bigdata.scores
) as a;


-- max()

select 
  id,
  cid,
  score,
  max(score) over (partition by id) as max_score
from
  bigdata.scores;

-- count()
select 
  id,
  cid,
  score,
  count(1) over(partition by id) as num
from bigdata.scores;

窗口内排序
-- 累积求和
select
  id,
  cid,
  score,
  sum(score) over(partition by id order by cid asc) as sum_score -- 排序时组内累积求和
from bigdata.scores;



-- 逐个比较求最大值
select
  id,
  cid,
  score,
  max(score) over(partition by id order by cid) as num
from bigdata.scores;


-- 逐个求平均值
select
  id,
  cid,
  score,
  avg(score) over(partition by id order by cid) as avg_score
from bigdata.scores;


1.2 排序类窗口函数
-- 1、 row_number
-- 组内排序
select
  id,
  cid,
  score,
  row_number() over(partition by id order by score desc) as r
from
  bigdata.scores;

-- 全局排序   -- 求topn
select
  id,
  sum(score) as sum_score,
  row_number() over(order by sum(score) desc) as r
from
  bigdata.scores
group by id;


-- rank
select
  id,
  sum(score),
  rank() over(order by sum(score) desc) as r
from
  bigdata.scores
group by id;



-- dense_rank
select
  id,
  sum(score),
  dense_rank() over(order by sum(score) desc) as r
from
  bigdata.scores
group by id;

1.3 取值类的窗口函数
-- lag 取前面的数据
select
  id,
  sum(score) as sum_score,
  lag(sum(score),1,0) over (order by sum(score) desc) as last_score
from bigdata.scores
group by id;

-- lead 取后面的数据
select
  id,
  sum(score) as sum_score,
  lead(sum(score),1,0) over (order by sum(score) desc) as lead_score
from bigdata.scores
group by id;


-- first_value:获取窗口内某一列的第一个值

select
  id,
  score,
  first_value(score) over ( partition by id order by score  desc) as fv_score
from bigdata.scores;



-- last_value:获取窗口内某一列的最后一个值
select
  id,
  score,
  last_value(score) over (partition by id) as lv_score
from bigdata.scores;
2、行列转换
表1
姓名,科目,分数
name,item,score
张三,数学,33
张三,英语,77
李四,数学,66
李四,英语,78
create table bigdata.table1(
    name STRING,
    item STRING,
    score DOUBLE
)ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH '/root/table1.csv' OVERWRITE INTO TABLE bigdata.table1 ;


表2
姓名,数学,英语
name,math,english
张三,33,77
李四,66,78
-- 解法： 将表1转换为表2
-- 创建表2，将表1转换为表2   科目的一列数据转换成两列数据
create table bigdata.table3 as
select
  name,
  -- 汇总数据成绩：如果item 等于‘数学’，取score成绩，否则取0，再按学生求和
  sum(
    case
      when item = '数学' then score
      else 0
    end
  ) as math,
  -- 汇总英语成绩：如果item等于‘英语’，取score成绩，否则取0，再按学生求和
  sum(
    case
      when item = '英语' then score
      else 0
    end
  ) as english
from bigdata.table1
group by name;
  


-- 将表2转换表1
select
  name,
  item,   
  score
from bigdata.table3
-- 使用lateral view explode,将每个学生的数学和英语列转换成多行记录
lateral view explode(
  map(
    '数学',math, -- map的key为数学value为_c1列的值
    '英语',english -- map的key为英语value为_c2列的值
  )
) T as item,score; -- 为map 的key命名为item，value命名为score

3、连续登录
user_id,login_date
01,2021-02-28
01,2021-03-01
01,2021-03-02
01,2021-03-04
01,2021-03-05
01,2021-03-06
01,2021-03-08
02,2021-03-01
02,2021-03-02
02,2021-03-03
02,2021-03-04
02,2021-03-06
03,2021-03-06

create table bigdata.user_login_log(
    user_id STRING,
    login_date STRING
)ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH '/root/user_login_log.csv' OVERWRITE INTO TABLE bigdata.user_login_log ;
-- 统计连续登录天数超过三天的用户
-- 解法2 利用日期与序号的差值分组
select
  user_id, -- 用户id
  min(login_date) as min_login_date, -- 连续登录开始时间
  max(login_date) as max_login_date, -- 连续登录结束时间
  -- 用login_date 与 row_number 的差值作为分组依据（相同的差值表示连续）
  date_sub(login_date,rank) as sub_date,
  -- 连续登录的天数统计
  count(1) as num
from(
  select
    user_id,
    login_date,
    -- 每个用户的登录记录按日期进行排序，并生成序列号
    row_number() over(partition by user_id order by login_date) as rank
  from
    bigdata.user_login_log
)as a
group by user_id,date_sub(login_date,rank)
having num >=3;





-- 解法2
select
  user_id, 
  min(login_date) as min_login_date, 
  max(login_date) as max_login_date, 
  date_sub(login_date,rank) as sub_date,
  count(1) as num
from(
  select
    user_id,
    login_date,
    row_number() over(partition by user_id order by login_date) as rank
  from
    bigdata.user_login_log
)as a
group by user_id,date_sub(login_date,rank)
having num >=3;



-- 解法1
-- 窗口函数+分组标记
select
  user_id,
  min(login_date) as min_login_date, -- 连续登录开始时间
  max(login_date) as max_login_date, -- 连续登录结束时间
  flag_sum,
  count(1) as num
from(
  select
    user_id,
    login_date,
    lag_login_date,
    flag,
    -- 对每个用户数据，按照login_date排序，累加flag（不连续处—加1），作为分组标记
    sum(flag) over (partition by user_id order by login_date) as flag_sum
  from(
    select 
      user_id,
      login_date,
      lag_login_date,
      -- 如果和上一次登录日期相差1天，标记0（连续）,否则标记1（不连续）
      if(datediff(login_date,lag_login_date)=1,0,1) as flag
    from(
      select
        user_id,
        login_date,
        -- 获取上一次登录日期
        lag(login_date,1) over(partition by user_id order by login_date) as lag_login_date
      from
        bigdata.user_login_log
    ) as a
  )as b
)as c
group by user_id,flag_sum
having num >= 3;







"""
https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E5%8D%B0%E5%B7%B4%E5%86%B2%E7%AA%81&page_type=searchall&page=1
https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E5%8D%B0%E5%B7%B4%E5%86%B2%E7%AA%81&page_type=searchall&page=2
https://m.weibo.cn/api/container/getIndex?containerid=1z00103type%3D1%26q%3D%E5%8D%B0%E5%B7%B4%E5%86%B2%E7%AA%81&page_type=searchall&page=3

https://m.weibo.cn/api/container/getIndex?
# containerid  100103type=1&q=印巴冲突
containerid=100103type%3D1%26q%3D%E5%8D%B0%E5%B7%B4%E5%86%B2%E7%AA%81   # 查询字符串部分
# 100103type=1&t=10&q=歌手首发阵容
100103type=1 表示要搜索类型是关键词搜索
q=$0   关键词，需要进行编码（parse.quote(word) 进行url编码）
# 搜索的筛选方式
t=10
page=1、2、3、4....    用于分页请求
"""

"""
导包
"""
import requests
import time
from urllib import parse

import re
import csv

from datetime import datetime





"""
https://m.weibo.cn/api/container/getIndex?
containerid=100103type=%3D1%26q=$0t=10    查询字符串部分
containerid=100103type=1    搜索的类型是关键词搜索
q=$0关键词，需要进行编码（parse.quote(word) 进行url编码）
t=10 搜索的筛选方式 
page=$1   用于分页请求
"""

# comment url   https://m.weibo.cn/comments/hotflow?id=5164695716891537&mid=5164695716891537&max_id_type=0
"""
id  微博的id
mid  微博的mid
max_id_type  用于控制评论分页，这里默认是第一页


"""


"""
参数配置
"""
# 关键词
word = "魔石坑道叽喳铜山"
# &   -- > %26
# 搜索的热搜url地址
base_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type=1%26q=$0%26t=10&page=$1"
# 评论的url地址
comment_url = "https://m.weibo.cn/comments/hotflow?id=$0&mid=$1&max_id_type=0"

# 正则表达式，用于去除HTML标签  <a></a>
# re_h = re.compile('</?\w+[^>]*>')

re_h = re.compile('</?\w+[^>]*>')
#text = re_h.sub("", mblog["text"])

# 数据存储的文件
weibo_list,user_list,comment_list = [],[],[]

# 定义一个去重的集合（存储已抓取的用户ID）
user_set = set()

# UA

"""
时间解析函数
"""
# 将微博的时间字符串转换为datetime对象
# 去除时区信息
# created_at": "Sat May 10 10:15:39 +0800 2025"   ---> 2025.5.10.10:15:39
def parse_time(timestr):
    timestr = re.sub(r'\+\d{4}','', timestr)   # "Sat May 10 10:15:39 2025"
    # 将字符串解析为 struct_time 时间戳
    # struct_time = time.strptime(timestr, '%a %b %d %H:%M:%S %Y')
    # 转换为 datetime 对象
    # return datetime.fromtimestamp(time.mktime(struct_time))
    # time.mktime 将字符串转换为时间戳
    return datetime.fromtimestamp(time.mktime(time.strptime(timestr,'%a %b %d %H:%M:%S %Y')))

"""
保存csv文件的函数
"""
def save_csv(filename,data):
    # 将数据写入CSV文件中
    with open(filename,'w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        # 将所有行一次性写入
        writer.writerows(data)




"""
添加用户信息的去重函数
"""
def add_user(user):
    # 添加用户数据（避免重复）
    uid = user.get("id")
    # 如果该用户未添加过则
    if uid not in user_set:
        # 将用户信息添加到user_list中
        user_list.append([
            # 用户ID
            uid,
            # 用户昵称
            user.get("screen_name",""),
            # 用户的微博数
            user.get("statuses_count",0),
            # 用户的关注数
            user.get("follow_count",0),
            # 用户的粉丝数
            user.get("followers_count",0)
        ])
        # 将用户ID添加到user_set中
        user_set.add(uid)

"""
抓取微博评论的函数
"""
def fetch_comment(id,mid):
    # 抓取某条微博的热门评论
    try:
        # 构造url请求
        url = comment_url.replace('$0',str(id)).replace('$1',str(mid))
        print(url)
        # 发送请求
        response = requests.get(url=url)
        # 解析评论数据
        data = response.json().get("data",{}).get("data",[])
        for item in data:
            comment_text = re_h.sub("",item.get("text",""))
            # 转换时间
            # created_at": "Sat May 10 09:46:08 +0800 2025",
            comment_time = parse_time(item["created_at"])
            # 向comment_list中添加数据
            comment_list.append([
                item["id"],
                comment_time,
                comment_text,
                item.get("like_count",0),
                item["user"]["id"]
            ])
            add_user(item["user"])

    except:
        pass




"""
主抓取流程
"""
for page in range(1,3):
    try:
        # 让其休眠2秒，避免频繁访问封IP
        time.sleep(2)
        # 替换关键词和页码
        # https://m.weibo.cn/api/container/getIndex?containerid=100103type=1&q=$0    &t=10&page=$1
        url = base_url.replace('$0',parse.quote(word)).replace('$1',str(page))
        # print(url)
        # 发送请求
        response = requests.get(url=url)
        # 提取微博的卡片数据
        # 获取json数据中的data ---- > cards
        cards = response.json().get("data",{}).get("cards",[])


        # 使用for循环遍历cards数据集
        for card in cards:
            # 获取每条微博的主题数据
            mblog = card.get("mblog")
            # 判断主题是否有数据，没数据则跳过
            if not mblog:
                continue

            # 微博的ID和MID
            weiboid = mblog['id']   # 5164761813877937
            mid = mblog['mid']
            print(mid)

            # 微博的发布时间
            # created_at": "Fri May 09 16:15:00 +0800 2025",
            created_at = parse_time(mblog["created_at"])

            # 微博的正文（去除HTML标签）
            # text = re_h.sub("",mblog["text"])
            text = re_h.sub("", mblog["text"])

            # 微博的主体数据添加到weibolist中
            weibo_list.append([
                # 微博的ID
                weiboid,
                # 微博的评论数
                mblog.get("comments_count",0),
                # 微博发布时间
                created_at,
                # 微博的内容
                text,
                # 转发数
                mblog.get("reposts_count",0),
                # 点赞数
                mblog.get("attitudes_count",0),
                # 微博的来源
                mblog.get("source",""),
                # 用户ID
                mblog["user"]["id"]
            ])



            # 调用添加用户的函数    添加博主（用户）信息
            add_user(mblog["user"])

            # 调用用户评论函数
            fetch_comment(weiboid,mid)

        print(f"第{page}页抓取完毕")
    except Exception as e:
        print(f"第{page}异常{e}")



"""
写入CSV
"""
save_csv("D:\\vscode_code\python train\data/weibo.csv",weibo_list)
save_csv("D:\\vscode_code\python train\data/user.csv",user_list)
save_csv("D:\\vscode_code\python train\data/comment.csv",comment_list)




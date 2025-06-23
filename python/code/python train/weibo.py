
"""
100103type=1&t=10&q=赵丽颖新恋情
"""

"""
微博搜索出来的网页
https://m.weibo.cn/api/container/getIndex?containerid=100103type
%3D =
1
%26 &
t
%3D = 
10
%26 &
q
%3D =
%E8%B5%B5%E4%B8%BD%E9%A2%96%E6%96%B0%E6%81%8B%E6%83%85
&
page_type=searchall



https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26t%3D10%26q%3D%E4%BA%AC%E4%B8%9C%E5%A4%96%E5%8D%96%E5%B4%A9%E4%BA%86&page_type=searchall&page=3

https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26t%3D10%26q%3D%E4%BA%AC%E4%B8%9C%E5%A4%96%E5%8D%96%E5%B4%A9%E4%BA%86&page_type=searchall&page=2
"""
"""
具体内容的网页
https://m.weibo.cn/comments/hotflow?id=5166176016531946&mid=5166176016531946&max_id_type=0


"""



import csv
from datetime import datetime
import re
import time
from urllib import parse
import requests

base_url= "https://m.weibo.cn/api/container/getIndex?containerid=100103type=1%26q=$0%26t=10&page=$1"
comment_base_url = "https://m.weibo.cn/comments/hotflow?id="

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

}

word = input("您想要搜索的关键词:")
# 转义后的word
# word = parse.quote(word)

start_page = int(input("开始页数"))

end_page = int(input("结束页数"))

# 正则表达式，用于去除HTML标签  <a></a>
# re_h = re.compile('</?\w+[^>]*>')
re_h = re.compile('</?\w+[^>]*>')


# 数据存储的文件
weibo_list,user_list,comment_list = [],[],[]

# 定义一个去重的集合（存储已抓取的用户ID）
user_set = set()





# 时间解析函数
# created_at": "Fri May 09 16:15:00 +0800 2025",
# 去除时区信息
def parse_time(timestr):
    timestr = re.sub(r'\+\d{4}','',timestr)
    #time.mktime 将字符串转换为时间戳
    return datetime.fromtimestamp(time.mktime(time.strptime(timestr,'%a %b %d %H:%M:%S %Y')))




# 添加用户函数
def add_user(user):
    # 添加用户数据（避免重复）
    uid = user.get("id")
    # 如果该用户未添加过则
    # if uid not in user_set:
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
        # user_set.add(uid)


# 用户评论函数
def fetch_comment(id,mid):
    try:
        url = comment_base_url + str(id) + "&mid=" + str(mid) + "&max_id_type=0"
        response = requests.get(url = url)
        data = response.json().get('data',{}).get("data",[])
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



# 保存csv文件的函数
def save_csv(filename,data):
    with open(filename,'w',encoding = 'utf-8',newline = '') as f:
        writer = csv.writer(f)
        # 将所有行一次性写入
        writer.writerows(data)


# 主抓取
for page in range(start_page,end_page):
        # 网页网址
        time.sleep(2)
        url = base_url.replace('$0',parse.quote(word)).replace('$1',str(page))
        # 获取响应
        response = requests.get(url =url,headers = headers)
        # 获取cards数据 因为返回的是json数据，所以要用json格式解析
        cards = response.json().get("data",{}).get("cards",{})
        # 使用for循环遍历cards数据集
        for card in cards:
            mblog = card.get("mblog")

            if not mblog:
                continue
            # 微博的ID和MID
            weiboid = mblog['id']
            # print(type(weiboid))
            # print(weiboid)
            mid = mblog['mid']


            #微博的发布时间
            created_at = parse_time(mblog["created_at"])

            # 微博的正文（去除HTML标签）
            text = re_h.sub("",mblog["text"])

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

"""
写入CSV
"""
save_csv("D:\\vscode_code\python train\data/weibo.csv",weibo_list)
save_csv("D:\\vscode_code\python train\data/user.csv",user_list)
save_csv("D:\\vscode_code\python train\data/comment.csv",comment_list)

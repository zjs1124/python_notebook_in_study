"""
使用requests抓取豆瓣电影
"""

# https://movie.douban.com/top250?start=0&filter=
# https://movie.douban.com/top250?start=25&filter=
# https://movie.douban.com/top250?start=50&filter=
# https://movie.douban.com/top250?start=75&filter=


import requests
from lxml import etree
import csv
import time


"""
电影的名称  翻译   title    

电影的导演    director

电影的主演    actors

电影的年份    year

电影的国家    country

电影的类型  movie_type

电影的评分  rating

评分人数   rating_num

电影的摘引  quote

"""

# UA
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

with open("douban_top250.csv","w",encoding="utf-8",newline="") as file:
    # 创建写对象
    write = csv.writer(file)
    # 写入csv表头
    write.writerow(["电影名称","电影导演","电影主演","电影年份","电影国家","电影类型","电影评分","评分人数","电影摘引"])

    # 处理豆瓣top250的页面
    for page in range(0,25,25):
        # 构造请求地址
        # print(page)
        url = f"https://movie.douban.com/top250?start={page}"
        # print(url)
        # 发送请求
        response = requests.get(url=url,headers=headers)
        # content = response.text
        # print(content)
        # 解析HTML
        html = etree.HTML(response.text)
        # 获取电影信息数据集
        items = html.xpath("//div[@class='item']")
        # print(items)
        # 使用for循环遍历列表依次取出对应的九条数据
        for item in items:
            # 电影的名称
            title = item.xpath(".//span[@class='title'][1]/text()")[0]
            # print(title)
            # 电影的导演
            # 电影导演和主演信息

            # 导演、主演、年份、国家、类型
            info = item.xpath(".//div[@class='bd']/p[1]/text()")
            # print(f"info去除之前的:{info}")
            # 去除空格
            # 使用for循环推导式来去除
            info = [i.strip() for i in info  if i.strip()]
            # print(f"info去除之后的：{info}")

            # for i in info:
            #     if i.strip():   i.strip()   true   false  []
            #         i.strip()
            # info去除之后的：['导演: 加布里尔·穆奇诺 Gabriele Muccino\xa0\xa0\xa0主演: 威尔·史密斯 Will Smith ...', '2006\xa0/\xa0美国\xa0/\xa0剧情 传记 家庭']
            # 处理导演的信息
            director = ""
            for text in info:
                if "导演:" in text:
                    # 分割并提取第一部分（去掉后面主演的信息）
                    director = text.split("主演:")[0].replace("导演:","").strip()  # 加布里尔·穆奇诺 Gabriele Muccino\xa0\xa0\xa0
                    # 处理\xa0  \xa0 前端特有的空格  特殊的
                    director = " ".join(director.split())
                    print(director)  # 加布里尔·穆奇诺 Gabriele Muccino
                    break

            # 处理主演部分
            actors = ""
            for text in info:
                if "主演:" in text:
                    actors = text.split("主演:")[1].strip()
                    print(f"------------------{actors}")   # 威尔·史密斯 Will Smith ...
                    break


            # 处理年份、国家、类型
            # ['导演: 加布里尔·穆奇诺 Gabriele Muccino\xa0\xa0\xa0主演: 威尔·史密斯 Will Smith ...', '2006\xa0/\xa0美国\xa0/\xa0剧情 传记 家庭']
            year_info = info[-1].strip().split("/")
            # 年份
            year = year_info[0].strip()
            # 国家
            # 判断，万一国家不存在
            country = year_info[1].strip()
            # 类型
            movie_type = year_info[2].strip()


            # 评分
            # //span[@class='rating_num']
            rating = item.xpath(".//span[@class='rating_num']/text()")[0]

            #评分人数
            # //div[@class='bd']/div/span[4]
            # 3163676人评价
            rating_num = item.xpath(".//div[@class='bd']/div/span[4]/text()")[0].replace("人评价","")

            # 电影的摘引
            # 摘引可能不存在
            quote = item.xpath(".//p[@class='quote']/span/text()")
            quote = quote[0] if quote else "暂无数据"

            # 写入文件中
            write.writerow([title,director,actors,year,country,movie_type,rating,rating_num,quote])
    print(f"已爬取第{page // 25 + 1}页数据")
    time.sleep(1)
print("抓取完成！")


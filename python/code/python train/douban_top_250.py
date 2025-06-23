"""


https://movie.douban.com/top250?start=0
https://movie.douban.com/top250?start=25
https://movie.douban.com/top250?start=50

https://movie.douban.com/top250?start={page}

"""
import csv
import time
import requests
from lxml import etree



#基本网址
base_url = 'https://movie.douban.com/top250?start='
#起始页数
start_page = int(input('请输入开始页数:'))
#结束页数
end_page = int(input('请输入结束页数:'))

#构建请求头
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

# 创建csv
with open('douban_top250.csv','w',encoding = 'utf-8',newline = '') as f:
    #创建写对象
    write = csv.writer(f)
    # 写入csv表头
    write.writerow(["电影名称","电影导演","电影主演","电影年份","电影国家","电影类型","电影评分","评分人数","电影摘引"])

    #翻页并获取每一页的网页源代码
    for page in range(start_page - 1,end_page):
        url = base_url + str(page * 25)
        response = requests.get(url = url,headers = headers)
        content = response.text
        # print(content) #打印网页源代码
        tree = etree.HTML(content)
        """
        数据集
        """
        items = tree.xpath("//div[@class='info']")
        # 使用for循环遍历列表依次取出对应的九条数据
        for item in items:
            """
            数据
            """
            #电影名字
            name = item.xpath(".//span[@class='title'][1]/text()")
            # 去除空格和换行
            
            info = item.xpath(".//p[1]/text()")
            print(f"info去除之前的:{info}")
            """
            ['\n                            导演: 安德鲁·斯坦顿 Andrew Stanton\xa0\xa0\xa0主演: 本·贝尔特 Ben Burtt / 艾丽...', '\n                            2008\xa0/\xa0美国\xa0/\xa0科幻 动画 冒险\n                        ']
            """
            # 遍历info字符串 使用for循环推导式来去除
            info = [i.strip() for i in info if i.strip()]
            print(f"info去除之后的:{info}")
            """
            ['导演: 安德鲁·斯坦顿 Andrew Stanton\xa0\xa0\xa0主演: 本·贝尔特 Ben Burtt / 艾丽...', '2008\xa0/\xa0美国\xa0/\xa0科幻 动画 冒险']
            """
            #导演
            director = ""
            for text in info:
                if "导演:" in text:
                    #分割并提取第一部分(去掉主演后面的信息)
                    director = text.split("主演:")[0].replace("导演:",'').strip()
                    # 处理\xa0  \xa0前端特有的空格
                    director = " ".join(director.split())
                    print(f'导演为:{director}')
                    break

            #主演
            actor = ""
            for text in info:
                if "主演:" in text:
                    actor = text.split("主演:")[1].strip()
                    print(f'主演为{actor}')
                    break
             # 处理年份、国家、类型
            # ['导演: 加布里尔·穆奇诺 Gabriele Muccino\xa0\xa0\xa0主演: 威尔·史密斯 Will Smith ...', '2006\xa0/\xa0美国\xa0/\xa0剧情 传记 家庭']
            year_info = info[-1].strip().split('/')
            #时间
            year = year_info[0].strip()
            #国家
            country = year_info[1].strip()
            #类型
            movie_type = year_info[-1].strip()
            #评分
            rating_1 = item.xpath(".//span[@class='rating_num']/text()")
            print(f'评分未取出时为{rating_1}')
            """
            评分未取出时为['8.8']
            """
            rating = item.xpath(".//span[@class='rating_num']/text()")[0]
            print(f'评分为{rating}')
            #评分人数1
            rating_num = item.xpath("//div[@class='bd']/div/span[4]/text()")[0]
            #摘要
            quote = item.xpath(".//p[@class='quote']/span/text()")
            quote = quote[0] if quote else ""
            # 写入csv
            write.writerow([name, director, actor, year, country, movie_type, rating, rating_num, quote])
    print(f"已爬取第{page+1}页数据")
    time.sleep(1)
print("抓取完成！")


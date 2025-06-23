from typing import Iterable, Any
"""
创建scrapy项目三步骤：
1、创建scrapy项目
scrapy startproject 项目的名称    eg：scrapy startproject baidu_pro 
2、创建爬虫文件
（1）进入spider目录下
cd .\Baidu_pro\Baidu_pro\spiders\
（2）创建爬虫文件
scrapy genspider 爬虫的名称  爬虫的域名   eg：scrapy genspider baidu baidu.com
3、运行爬虫
scrapy crawl 爬虫的名称   eg：scrapy crawl baidu
"""
import scrapy

# 百度爬虫类
class BaiduSpider(scrapy.Spider):
    # 成员变量

    # 爬虫的名称     ---唯一的
    name = "baidu"
    # 爬虫的域名，允许爬虫行走范围
    allowed_domains = ["www.baidu.com"]
    # 起始url列表
    start_urls = ["https://www.baidu.com"]

    # 成员方法
    # 解析函数
    # urllib
    # request = urllib.request.Request(url...)
    # response = urllib.request.urlopen(request)
    # requests
    # response = requests.get(url)

    # def start_requests(self):
    #     pass

    def parse(self, response):
        # print("你好，Scrapy！")

        # xpath
        result = response.text
        print(response.status)
        print(response.headers)
        # print(result)

        name = response.xpath("//input[@id='su']/@value").get()
        print(name)


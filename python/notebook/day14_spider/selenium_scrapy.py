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

在settings中将robots_obey改为False
"""



"""
1、下载selenium
pip install selenium

2、下载谷歌驱动（找到对应自己谷歌浏览器的版本）  （点击右上角三个点--->点击设置---->点击关于 Chrome）
https://googlechromelabs.github.io/chrome-for-testing/

3、查看文档
https://www.selenium.dev/zh-cn/documentation/webdriver/getting_started/using_selenium/
https://selenium-python-zh.readthedocs.io/en/latest/


4、使用selenium三步骤
（1）# 导入selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
（2）# 创建浏览器操作对象
service = Service("D:\pythoncode\python-learn\day14_spider\chromedriver.exe")
browser = webdriver.Chrome(service=service)
（3）# 访问网站
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from lxml import etree

#创建浏览器对象
service = Service("D:\chorme_driver\chromedriver-win64\chromedriver.exe")
browser = webdriver.Chrome(service = service)

#访问网站
url  = 'https://www.baidu.com/'
browser.get(url)
time.sleep(2)

#获取网页源代码
content = browser.page_source
tree = etree.HTML(content)
name = tree.xpath("//input[@id='su']/@value")
print(name)
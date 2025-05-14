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
# 导入selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from lxml import etree
import time

# 创建浏览器操作对象
service = Service("D:\pythoncode\chromedriver.exe")
browser = webdriver.Chrome(service=service)
# 访问网站
url = "https://www.baidu.com/"
browser.get(url)
time.sleep(5)

# 获取网页源代码
content = browser.page_source
# print(content)
tree = etree.HTML(content)
name = tree.xpath("//input[@id='su']/@value")
print(name)


# 退出
browser.quit()
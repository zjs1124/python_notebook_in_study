"""
元素定位
元素定位：自动化要做的就是模拟鼠标和键盘来操作来操作这些元素，点击、输入等等。
操作这些元素前首先 要找到它们，WebDriver提供很多定位元素的方法
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.by import By

service = Service("D:\pythoncode\python-learn\day14_spider\chromedriver.exe")
browser = webdriver.Chrome(service=service)
browser.get("https://www.baidu.com/")
# time.sleep(2)

# *******************************元素的定位***************************************
# 根据id来找对象
# button = browser.find_element(By.ID,"su")
# print(button)

# 根据标签属性的属性值来获取对象
# button = browser.find_element(By.NAME,"wd")
# print(button)


# 根据xpath语句获取对象
# button = browser.find_element(By.XPATH,"//input[@id='su']")
# print(button)



# 根据标签的名字来获取对象
# button = browser.find_element(By.TAG_NAME,"input")
# print(button)


# 根据Bs4来获取对象
# button = browser.find_element(By.CSS_SELECTOR,"#su")
# print(button)


# 获取链接文本
# button = browser.find_element(By.LINK_TEXT,"新闻")
# print(button)

input = browser.find_element(By.ID,"su")
# 获取元素的属性
print(input.get_attribute("class"))  # bg s_btn


# 获取标签的名称
print(input.tag_name)  #input.


button = browser.find_element(By.LINK_TEXT,"新闻")
print(button.text)
browser.quit()
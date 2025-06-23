"""
selenium 交互操作
"""
# 导包
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.by import By

# 创建对象
service = Service("D:\pythoncode\python-learn\day14_spider\chromedriver.exe")
brower = webdriver.Chrome(service=service)

# 访问网页
url = "https://www.baidu.com/"
brower.get(url)
time.sleep(3)

# *******************************交互***************************************

# 获取文本框对象
input = brower.find_element(By.ID,"kw")

# 在文本框中输入内容   send_keys
input.send_keys("京东")
time.sleep(2)


# 获取百度一下按钮
button = brower.find_element(By.ID,"su")

# 点击按钮   click
button.click()
time.sleep(2)




# 滑到底部（执行javaScript滑动到底部）
# js="window.scrollTo(0, document.body.scrollHeight)"
brower.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)


# 获取下一页按钮对象

# next = brower.find_element(By.XPATH,"//a[@class='n']")
next = brower.find_element(By.XPATH,"//div[@class='page-inner_2jZi2']/a[@class='n ']")
next.click()
time.sleep(5)
# brower.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(5)

# 回到上一页
brower.back()
time.sleep(5)

# 回去
brower.forward()
time.sleep(5)



# 退出
brower.quit()
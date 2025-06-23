"""
无头模式
chrome handless 模式:不打开web浏览器界面进行搜索
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
# chrome handless 模式导包
from selenium.webdriver.chrome.options import Options


# 封装成函数
def setting_headless():
    options = Options()
    options.add_argument('--headless')  # 无界面模式
    options.add_argument('--disable-gpu')  # disable  禁用 gpu
    # 可写可不写（建议带上）
    service = Service('D:\pythoncode\python-learn\day14_spider\chromedriver.exe')
    # 创建无头浏览器对象
    brower = webdriver.Chrome(service=service, options=options)
    return brower

# 调用函数
brower = setting_headless()

# 访问网址
brower.get("https://www.baidu.com/")

# 截图
brower.save_screenshot('index.png')

brower.quit()
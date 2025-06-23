# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from lxml import etree
# from selenium.webdriver.common.by import By
# #chrome headless 模式导包
# from selenium.webdriver.chrome.options import Options

# # 封装成函数
# def setting_headless():
#     options = Options()
#     options.add_argument('--keadless') #无界面模式
#     options.add_argument('--disable-gpu')# 禁用GPU
#     # 可写可不写（建议带上）
#     service = Service('D:\chorme_driver\chromedriver-win64\chromedriver.exe')
#     # 创建无头浏览器对象
#     brower = webdriver.Chrome(service=service, options=options)
#     return brower

# #调用函数
# brower = setting_headless()
# # 访问网址
# brower.get("https://www.baidu.com/")
# # 截图
# brower.save_screenshot('index.png')

# brower.quit()




# # 创建浏览器创建对象
# service = Service('D:\chorme_driver\chromedriver-win64\chromedriver.exe')
# brower = webdriver.Chrome(service = service)

# # 获取网页
# url = 'https://www.baidu.com/'
# brower.get(url)
# time.sleep(3)


# #获取文本对象
# input = brower.find_element(By.ID,"kw")

# # 在文本框中输入内容
# input.send_keys("京东")
# time.sleep(2)


# # 获取百度一下按钮
# button = brower.find_element(By.ID,'su')\

# # 点击按钮 click()
# button.click()
# time.sleep(2)

# #滑到底部
# # js="window.scrollTo(0, document.body.scrollHeight)"
# brower.execute_script("window.scrollTo(0,document.body.scrollHeight);")
# time.sleep(2)

# # 获取下一页按钮对象
# next = brower.find_element(By.XPATH,"//div[@class='page-inner_2jZi2']/a[@class='n ']")
# next.click()
# time.sleep(5)

# #回到上一页
# brower.back()
# time.sleep(5)

# # 回去
# brower.forward()
# time.sleep(5)


# # 退出
# brower.quit()






# # 网页源代码
# content = browser.page_source
# # print(content)
# tree = etree.HTML(content)
# name = tree.xpath("//input[@id='su']/@value")
# print(name)


# #关闭浏览器
# browser.quit()
# """
# 元素定位
# 元素定位：自动化要做的就是模拟鼠标和键盘来操作来操作这些元素，点击、输入等等。
# 操作这些元素前首先 要找到它们，WebDriver提供很多定位元素的方法
# """

# # *******************************元素的定位***************************************

# #根据ID来找对象
# button = browser.find_element(By.ID,"su")
# print(button)


# # 根据标签属性值来获取对象
# button = browser.find_element(By.NAME,'wd')
# print(button)

# # 根据xpath来获取对象
# button = browser.find_element(By.XPATH,'')
# print(button)

# # 根据标签名字来获取对象
# button = browser.find_element(By.Tag_NAME,"input")
# print(button)

# # 根据bs4获取对象
# button = browser.find_element(By.CSS_SELECTOR,"#su")
# print(button)

# # 获取链接文本
# button = browser.find_element(By.LINK_TEXT,"新闻")
# print(button)

# input =  browser.find_element(By.ID,"su")
# # 获取属性
# print(input.get_attribute('class'))

# # 获取标签的名称
# print(input.tag_name)
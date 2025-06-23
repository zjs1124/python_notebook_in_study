"""
1、安装requests
pip install requests
2、 导包
import requests
3、类型及属性
# 一个类型
# <class 'requests.models.Response'>
# 六个属性


"""
# requests 的类型及属性

# import requests

# url = "https://www.baidu.com/"

# response = requests.get(url)
# # print(response) #<Response [200]>
# # print(type(response))  # <class 'requests.models.Response'>

# # 六个属性
# # 1、encoding:设置响应的编码格式
# response.encoding = 'utf-8'

# # 2、text:以字符串的实行返回网页源代码
# print(response.text)

# # 3、url：返回一个url地址
# print(response.url) #https://www.baidu.com/

# # 4、content 返回一个二进制数据(以b开头)
# print(response.content)

# # 5、 status_code 响应的状态码
# print(response.status_code)

# # 6、headers:返回响应头
# print(response.headers)
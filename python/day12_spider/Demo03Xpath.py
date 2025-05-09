"""
解析服务器响应文件
"""
import urllib.request
from lxml import etree

url = "https://www.baidu.com/"
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# 请求对象定制
request = urllib.request.Request(url=url,headers=headers)
# 模拟浏览器向百度服务器发送请求
response = urllib.request.urlopen(request)

# 获取网页源代码
content = response.read().decode("utf-8")
# 解析服务器响应文件
tree = etree.HTML(content)

# 使用xpath提取想要的数据：百度一下
result = tree.xpath('//input[@id="su"]/@value')[0]
print(result)
# print(type(result))
text = tree.xpath("//ul[@id='hotsearch-content-wrapper']/li[1]/a/span[2]/text()")
print(text[0])



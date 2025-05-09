"""
# 模拟头部信息
urllib.request.Request
"""

# URL的组成
# https://www.baidu.com/s?&wd=python
# 协议：http/https
# 主机：www.baidu.com
# 端口号：http 80    https 443
# 路径：s
# 参数：wd=python
# 锚点：#

# import urllib.request
# url = "https://www.baidu.com/"
# response = urllib.request.urlopen(url)
# html = response.read().decode("utf-8")
# print(html)   # 如果频繁反问就会出现反爬（导致html内容出现很少）


"""
UA:user-agent中文名：用户代理，简称UA。它是一个特殊的字符串头，使得服务器能够识别客户使用的操作系统及版本、CPU类型、浏览器版本。
（浏览器内核、浏览器渲染引擎、浏览器语言、浏览器插件）
"""

import urllib.request
url = "https://www.baidu.com/"

# 模拟请求头
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
# 因为urlopen方法不能存储字典类型，索引headers是不能传递进去的
# response = urllib.request.urlopen()
# 请求头定制
# 注意：url,headers不能使用位置传参，因为存在参数顺序
# request = urllib.request.Request(url,headers)
request = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
html = response.read().decode("utf-8")
print(html)
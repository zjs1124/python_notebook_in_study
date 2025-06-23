"""
handler处理器
使用handler处理器访问百度，获取源代码
"""
import urllib.request


url = "https://www.baidu.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
request = urllib.request.Request(url=url,headers=headers)

# 1、获取handler对象
handler = urllib.request.HTTPHandler()  # <urllib.request.HTTPHandler object at 0x000001B192394790>
# print(handler)

# 2、获取opener对象
opener = urllib.request.build_opener(handler)

# 3、调用opener的open方法，发送请求，获取响应
response =opener.open(request)


# response = urllib.request.urlopen(request)
#
content = response.read().decode("utf-8")
print(content)
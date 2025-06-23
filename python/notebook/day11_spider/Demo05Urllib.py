"""
Post请求
"""
import urllib.request
import urllib.parse
import json

# 百度翻译
# https://fanyi.baidu.com/sug
url = "https://fanyi.baidu.com/sug"
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

data = {
    "kw":"中国"
}

# TypeError: POST data should be bytes, an iterable of bytes, or a file object. It cannot be of type str.
# post请求参数必须要进行编码urlencode()后需要加入encode("utf-8")
data = urllib.parse.urlencode(data).encode("utf-8")
# print(data)  # kw=spider

# post请求的参数是不会拼接在url后面，而是需要放在请求对象定制的参数中
request = urllib.request.Request(url=url,data=data,headers=headers)
# print(request)  # <urllib.request.Request object at 0x000001C73E9E53F0>

# 模拟浏览器向服务器发送请求
response = urllib.request.urlopen(request)
# print(response)   # <http.client.HTTPResonse object at 0x000002977892F640>

# 获取响应的数据
content = response.read().decode("utf-8")
# print(content)
# print(type(content))  # <class 'str'>

# 将字符串转换成json
obj = json.loads(content)
print(obj)

"""
总结：
post请求注意事项：
    1、post请求方式的参数必须编码   data = urllib.parse.urlencode(data)
    2、编码之后，必须调用encode()方法  data = urllib.parse.urlencode(data).encode("utf-8")
    3、参数是放在请求对象Request()定制中

get请求
    1、get请求方式的参数必须编码，参数是拼接在url后面，编码之后不需要encode()方法

"""
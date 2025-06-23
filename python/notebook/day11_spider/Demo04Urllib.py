"""
urlencode() 多个参数传递
"""
# https://www.baidu.com/s?wd=%E8%BF%AA%E4%B8%BD%E7%83%AD%E5%B7%B4&sex=%E5%A5%B3&location=%E6%96%B0%E7%96%86
import urllib.request
import urllib.parse

base_url = "https://www.baidu.com/s?"

data = {
    "wd": "迪丽热巴",
    "sex": "女",
    "location": "新疆"
}
new_data = urllib.parse.urlencode(data)
url = base_url + new_data

# 请求头
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# 请求对象定制
request = urllib.request.Request(url=url, headers=headers)

# 发送请求
response = urllib.request.urlopen(request)

content = response.read().decode("utf-8")
print(content)
"""
IP代理
"""
import urllib.request

url = "https://www.baidu.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

request = urllib.request.Request(url=url,headers=headers)

# IP代理池
# 183.160.75.52
# 203.74.125.18 8888
proxies = {
    "https": "114.35.177.252:8089"
}
# 1、获取handler对象
handler = urllib.request.ProxyHandler(proxies=proxies)

# 2、获取opener对象
opener = urllib.request.build_opener(handler)

# 3、调用open方法
response = opener.open(request)

# 4、获取响应内容
content = response.read().decode("utf-8")
print(content)
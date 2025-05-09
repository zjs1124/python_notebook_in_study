"""
urllib.error:定义了在请求过程中可能引发的异常
常见的异常处理：
HTTPError
URLError


1、HTTPError是URLError的子类
urllib.error.HTTPError
urllib.error.URLError
2、HTTP错误是针对浏览器无法连接到服务器而增加出来的错误提示
"""

import urllib.request
import urllib.error

# https://www.kfc.com.cn/kfccda/index1.aspx
url = "https://blog.csdn.net/weixin_52270091/article/details/126891869"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
try:
    request = urllib.request.Request(url=url,headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")
    print(content)
except urllib.error.HTTPError:
    print("HTTPError")
except  urllib.error.URLError:
    print("URLError")
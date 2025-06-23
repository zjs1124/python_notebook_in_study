"""
编解码
"""
# https://www.baidu.com/s?wd=汽车之家
# 编码 quote()
# 解码 unquote()
import urllib.request
import urllib.parse
url = "https://www.baidu.com/s?wd="
# wd=汽车之家
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
# 将汽车之家四个字进行编码操作，Unicode编码
word = urllib.parse.quote("汽车之家")
# print(word)
# %E6%B1%BD%E8%BD%A6%E4%B9%8B%E5%AE%B6
# %E6%B1%BD%E8%BD%A6%E4%B9%8B%E5%AE%B6
word_test = urllib.parse.unquote("%E6%B1%BD%E8%BD%A6%E4%B9%8B%E5%AE%B6")
print(word_test)


url = url + word
print(url)  # https://www.baidu.com/s?wd=%E6%B1%BD%E8%BD%A6%E4%B9%8B%E5%AE%B6

# # 请求头定制
# request = urllib.request.Request(url=url,headers=headers)
# # 发送请求
# response = urllib.request.urlopen(request)
# html = response.read().decode("utf-8")
# print(html)
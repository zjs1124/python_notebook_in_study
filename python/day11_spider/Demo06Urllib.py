"""
ajax的get请求
"""
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=20&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=40&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=60&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=80&limit=20


import urllib.request

url = "https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 请求对象定制
request = urllib.request.Request(url=url, headers=headers)
# 获取响应数据
response = urllib.request.urlopen(request)
content = response.read().decode("utf-8")

# print(content)
# 将json数据下载到本地

with open("douban.json","w",encoding="utf-8") as file:
    file.write(content)
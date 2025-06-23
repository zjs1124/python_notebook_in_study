"""
麦当劳案例
https://www.mcdonalds.com.cn/index/Food/menu/burger
需求：拿到所有汉堡的名称
"""

import urllib.request
from  bs4 import BeautifulSoup


url = "https://www.mcdonalds.com.cn/index/Food/menu/burger"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

request = urllib.request.Request(url=url, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode("utf-8")
# print(content)

# 创建soup对象
soup = BeautifulSoup(content,'lxml')
# print(soup)

# //div[@class='col-md-3 col-sm-4 col-xs-6']/a/span   xpath语法
name_list = soup.select("div[class='col-md-3 col-sm-4 col-xs-6'] span")
print(name_list)
for name in name_list:
    print(name.get_text())


# //div[@class='col-md-3 col-sm-4 col-xs-6']/a/div/img/@src   xpath语法
# 推导式[img['src'] for img in soup.select("div.col-md-3 col-sm-4 col-xs-6 div img")]
# img_list = [img['src'] for img in soup.select("div.col-md-3.col-sm-4.col-xs-6 div img")]
# 第一步
# img_list = soup.select("div.col-md-3.col-sm-4.col-xs-6 div img")
# 第二步
# div[@class='col-md-3 col-sm-4 col-xs-6']
img_list = [img['src'] for img in soup.select("div.col-md-3.col-sm-4.col-xs-6 div img")]
print(img_list)

# for img in img_list:
#     print(img)
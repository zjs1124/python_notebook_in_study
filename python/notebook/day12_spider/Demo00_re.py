import re

import requests


# https://www.dytt8.com/

url = "https://www.dytt8.com/"

response = requests.get(url)  # 忽略安全认证
# 设置编码格式
response.encoding = "gb2312"
# print(response.text)

# 匹配2025新片精品下的所有的内容
obj1 = re.compile(r'2025新片精品.*?<ul>(?P<ul>.*?)</ul>',re.S)   # re.S或略换行符

result = obj1.finditer(response.text)
print(result)  # <callable_iterator object at 0x00000291B58156F0>


for i in result:
    print(i.group("ul"))





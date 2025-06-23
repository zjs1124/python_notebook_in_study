"""
百度翻译
post请求
"""

import requests
import json
url = "https://fanyi.baidu.com/sug"

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

data = {
    "kw":"蜘蛛"
}

response = requests.post(url=url,data=data,headers=headers)
content = response.text
# print(content)
obj = json.loads(content)
print(obj)
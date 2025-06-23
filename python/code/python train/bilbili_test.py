import json
import time
import requests


"""

https://live.bilibili.com/p/eden/area-tags?visit_id=2ab0s4n63lus&areaId=102&parentAreaId=2

"""

"""
url 构成
https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=2&area_id=102&sort_type=online%3Bar%3D1&page=$0&web_location=444.43&w_rid=$1&wts=
page=2(翻页数量)
w_rid=6caf9d4fa2a4624ab12a7f4fff6afbf4
wts=1746860198



"""
"""
b站网游
"""

# url = 'https://api.live.bilibili.com/room/v1/area/getList?parent_id=2&platform=web'
# # wts = str(int(time.time()))

# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
#     "Referer":"https://live.bilibili.com/"
# }

# #构建请求头


# #获取响应
# response = requests.get(url = url,headers = headers)
# #获取网页源代码
# content = response.text

# print(content)









"""
# 模拟头部信息
urllib.request.Request
"""

# URL的组成
# https://www.baidu.com/s?&wd=python
# 协议：http/https
# 主机：www.baidu.com
# 端口号：http 80    https 443
# 路径：s
# 参数：wd=python
# 锚点：#

import urllib.request
url = "https://www.baidu.com/"
response = urllib.request.urlopen(url)
html = response.read().decode("utf-8")
print(html)   # 如果频繁反问就会出现反爬（导致html内容出现很少）
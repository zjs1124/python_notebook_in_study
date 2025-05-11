"""
https://pic.netbian.com/4kfengjing/
"""

import requests
from lxml import etree
url = "https://pic.netbian.com/4kmeinv/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "cookie":"cf_clearance=Kfwdc1nUs4dbdrgdcTqmUJQF7.iQH4IlrJsKCMVBdBE-1746757843-1.2.1.1-ehyl7BBrBN8XOoh9h8XQq0jVRVfdDuPuHyDUHrfgv7wmPWERyhjcC5NthSrpmfta469Xbbhu8CG5tdWxFua.cuOEDxC62RE9T1ggh3t9SsoxFhvpHQQAQhmcCKlRfKWSeCvDogpPD3.S3.VvRkrwIfSR8AdfuCAKVYF4.qYMsXydnJQY381rnPUEZA4bHauLL6amAO7y_Pl1vNlxIB78EtpPWJVYOoumAkxFyJH88xoB5Yv.ztQputgGZzgTaSN3XnPCIF.yzdEir9PbRVz_zP6bfRSq3OU3v5OOrLFo4UDiuPli8cqOraz8A10hPsb.qgAgrXK4aiQO.i18pGAQCqQOVf5fG9MrstmBJUpgkyaQfaGztfCEs9njz4z.PJ1t; zkhanecookieclassrecord=%2C53%2C54%2C; PHPSESSID=uijqned1d1231bfglsdu9d45j2; zkhanmlusername=qq_%BF%EC%C0%D6%D0%C7%C7%F2%D4%DA%CC%D3%BE%D3%C3%F1559; zkhanmluserid=7974545; zkhanmlgroupid=1; zkhanmlrnd=JJJ74KPiI46Azy043IB8; zkhanmlauth=bafa7549aeec584cc856e12a7ca54bf1",
    # 防盗链
    "referer":"https://pic.netbian.com/new/"
}


response = requests.get(url=url,headers=headers)
response.encoding = "gbk"

tree = etree.HTML(response.text)

# 获取img地址
img_list = tree.xpath("//ul[@class='clearfix']/li/a/img/@src")
# print(img_list)
# for img in img_list:
#     img_url = "https://pic.netbian.com/" + img
#     print(img_url)


# 获取img名称
name_list = tree.xpath("//ul[@class='clearfix']/li/a/b/text()")
print(name_list)
for name in name_list:
    name = name.replace(" ","")
    print(name)

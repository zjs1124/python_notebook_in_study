"""
抓取彼岸图一页所有图片
https://pic.netbian.com/4kfengjing/


"""
import requests

from lxml import etree



# url = "https://pic.netbian.com/4kfengjing/"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "cookie":"cf_clearance=Kfwdc1nUs4dbdrgdcTqmUJQF7.iQH4IlrJsKCMVBdBE-1746757843-1.2.1.1-ehyl7BBrBN8XOoh9h8XQq0jVRVfdDuPuHyDUHrfgv7wmPWERyhjcC5NthSrpmfta469Xbbhu8CG5tdWxFua.cuOEDxC62RE9T1ggh3t9SsoxFhvpHQQAQhmcCKlRfKWSeCvDogpPD3.S3.VvRkrwIfSR8AdfuCAKVYF4.qYMsXydnJQY381rnPUEZA4bHauLL6amAO7y_Pl1vNlxIB78EtpPWJVYOoumAkxFyJH88xoB5Yv.ztQputgGZzgTaSN3XnPCIF.yzdEir9PbRVz_zP6bfRSq3OU3v5OOrLFo4UDiuPli8cqOraz8A10hPsb.qgAgrXK4aiQO.i18pGAQCqQOVf5fG9MrstmBJUpgkyaQfaGztfCEs9njz4z.PJ1t; zkhanecookieclassrecord=%2C53%2C54%2C; PHPSESSID=uijqned1d1231bfglsdu9d45j2",
#     # 防盗链
#     "referer":"https://pic.netbian.com/new/"
# }
# response = requests.get(url=url,headers=headers)
# response.encoding = "gbk"
# content = response.text
# print(content)
"""
https://pic.netbian.com/4kfengjing/
https://pic.netbian.com/4kfengjing/index_2.html
https://pic.netbian.com/4kfengjing/index_3.html
https://pic.netbian.com/4kfengjing/index_4.html
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "cookie":"cf_clearance=Kfwdc1nUs4dbdrgdcTqmUJQF7.iQH4IlrJsKCMVBdBE-1746757843-1.2.1.1-ehyl7BBrBN8XOoh9h8XQq0jVRVfdDuPuHyDUHrfgv7wmPWERyhjcC5NthSrpmfta469Xbbhu8CG5tdWxFua.cuOEDxC62RE9T1ggh3t9SsoxFhvpHQQAQhmcCKlRfKWSeCvDogpPD3.S3.VvRkrwIfSR8AdfuCAKVYF4.qYMsXydnJQY381rnPUEZA4bHauLL6amAO7y_Pl1vNlxIB78EtpPWJVYOoumAkxFyJH88xoB5Yv.ztQputgGZzgTaSN3XnPCIF.yzdEir9PbRVz_zP6bfRSq3OU3v5OOrLFo4UDiuPli8cqOraz8A10hPsb.qgAgrXK4aiQO.i18pGAQCqQOVf5fG9MrstmBJUpgkyaQfaGztfCEs9njz4z.PJ1t; zkhanecookieclassrecord=%2C53%2C54%2C; PHPSESSID=uijqned1d1231bfglsdu9d45j2",
    # 防盗链
    "referer":"https://pic.netbian.com/new/"
}
# 发送请求
def get_request(page):
    if page == 1:
        url = "https://pic.netbian.com/4kfengjing/"
    else:
        url = "https://pic.netbian.com/4kfengjing/index_" + str(page) + ".html"

    # 发送请求
    response = requests.get(url=url,headers=headers)
    return response


# 获取网页源代码
def get_content(response):
    response.encoding = "gbk"
    content = response.text
    return content

# 下载图片数据
def down_load(content):
    tree = etree.HTML(content)
    # 获取数据集
    img_list = tree.xpath("//div[@class='slist']/ul/li")
    for img in img_list:
        # 获取图片地址
        img_url = img.xpath("./a/img/@src")[0]
        # 获取图片名称
        img_name = img.xpath("./a/img/@alt")[0]
        img_url = "https://pic.netbian.com/" + img_url
        img_name = img_name + ".jpg"
        img_data = requests.get(url=img_url,headers=headers).content
        with open("img/" + img_name,mode="wb") as f:
            f.write(img_data)


# 主程序


if __name__ == '__main__':
    # 起始页
    start_page = int(input("请输入起始页码："))
    # 结束页
    end_page = int(input("请输入结束页码："))
    # 使用for循环遍历所有页面
    for page in range(start_page,end_page + 1):
        response = get_request(page)
        content = get_content(response)
        down_load(content)

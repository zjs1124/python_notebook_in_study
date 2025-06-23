import requests
from lxml import etree
import urllib
"""

https://pic.netbian.com/4kdongwu/index.html
https://pic.netbian.com/4kdongwu/index_2.html
https://pic.netbian.com/4kdongwu/index_3.html
"""




# 开始数据配置
base_url = "https://pic.netbian.com/4kdongwu/index"

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "referer":'"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"'

}
# 图片前面的共有地址
img_base_url = 'https://pic.netbian.com/'
# 开始页数
start_page = int(input("请输入开始的页数："))

# 结束页数
end_page = int(input("请输入结束的页数："))


for page in range(start_page,end_page):
    if page == 1:
        url = base_url + ".html"
    else:
        url = base_url + "_" + str(page) + ".html"
    response = requests.get(url = url,headers = headers)
    response.encoding = 'gbk'
    # content = response.text
    # print(content)
    tree = etree.HTML(response.text)
    #图片
    items = tree.xpath("//div[@class='slist']//a")
    for item in items:
        # 图片的部分地址
        img_url = item.xpath("./img/@src")[0]
        #图片完整地址
        img_url = img_base_url + img_url
        #图片的名字
        img_name = item.xpath("./b/text()")[0]
        img_name = img_name + ".jpg"
        # 下载转为二进制数
        img_data = requests.get(url = img_url,headers = headers).content
        with open("D:\\vscode_code\\python train\\img/" + img_name,mode = 'wb') as f:
            f.write(img_data)
        # with open("img/" + img_name,mode="wb") as f:
        #     f.write(img_data)

        




























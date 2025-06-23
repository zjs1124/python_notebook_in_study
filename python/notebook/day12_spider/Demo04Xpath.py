"""
https://pic.netbian.com/4kfengjing/
"""
import urllib.request
import urllib.parse
from lxml import etree
#
# url = "https://sc.chinaz.com/tupian/taikongkexuetupian.html"
# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
# }
#
# # 请求头定制
# request = urllib.request.Request(url=url,headers=headers)
# # 发送请求
# response = urllib.request.urlopen(request)
#
# # 获取数据
# content = response.read().decode("utf-8")
# print(content)



# 请求头定制
def create_request(page):
    if page == 1:
        url = "https://sc.chinaz.com/tupian/taikongkexuetupian.html"
        # print(url)
    else:
        url = "https://sc.chinaz.com/tupian/taikongkexuetupian_" + str(page) + ".html"
        # print(url)

    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url=url,headers=headers)
    return  request

# 获取数据
def get_content(request):
    response = urllib.request.urlopen(request)
    content =  response.read().decode("utf-8")
    return content


# 下载
def down_load(content):
    tree = etree.HTML(content)
    # //div[@class='container']//img/@src
    name_list = tree.xpath("//div[@class='container']//img/@alt")
    # print(name_list)
    img_list = tree.xpath("//div[@class='container']//img/@data-original")
    print(img_list)

    # 使用for循环遍历
    for i in range(len(name_list)):
        name = name_list[i]
        src = img_list[i]
        url = "https:" + src
        urllib.request.urlretrieve(url=url,filename="./img/" + name + ".jpg")
    
    
"""
https://sc.chinaz.com/tupian/taikongkexuetupian.html
https://sc.chinaz.com/tupian/taikongkexuetupian_2.html
https://sc.chinaz.com/tupian/taikongkexuetupian_3.html
https://sc.chinaz.com/tupian/taikongkexuetupian_4.html

"""
# 主程序
if __name__ == '__main__':
    # 起始页
    start_page = int(input("请输入起始页码："))
    # 结束页
    end_page = int(input("请输入结束页码："))
    # 使用for循环遍历所有页面
    for page in range(start_page,end_page + 1):
        # 请求头定制
        request = create_request(page)
        # 获取数据
        content = get_content(request)
        # 下载数据
        down_load(content)





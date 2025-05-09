# import urllib.request
# url = 'https://www.baidu.com/'
# response = urllib.request.urlopen(url)
# 1.read() 读取一个一个字节
# content = response.read(5)
# print(content)
# print(content)
# 2.readline()读取一行
# content = response.readline()
# print(content)
# 3.readlines() 读取所有行
# content = response.readlines()
# print(content)
# 4，getcode()获取状态码
# print(response.getcode())
'''
状态码
200 成功获取
404 notfound
505 http version not supported
504 gateway time-out 充当网关或者代理的服务器，未及时获取远端服务器的请求

'''
# 5.geturl()获取url
# print(response.geturl())https://www.baidu.com/

#6. getheaders() 获取响应头
# print(response.getheaders())

# 7.下载
#urllib.request.urlretrieve
# img_url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
# urllib.request.urlretrieve(img_url,'logo1.png')

"""
url的组成
https://www.baidu.com/s?&wd=python
1.协议:http/https
2.主机:www.baidu.com
3.端口号 http:80 https:443
4.路径:s
5.参数:wd=python
6.锚点:#
"""
# import urllib.request
# url = "https://www.baidu.com/"
# response = urllib.request.urlopen(url)
# html = response.read().decode('utf-8') decode解码,encode编码
# print(html)

"""
UA:user-agent:中文代理，简称UA，是一个特殊的字符串头，使得服务器能够识别客户使用的操作系统及版本
（浏览器内核、浏览器渲染引擎、浏览器语言、浏览器插件）
"""
# url = "https://www.baidu.com/"
# #模拟请求头
# headers = {
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
# }
# # 因为urlopen方法不能存储字典类型，索引headers是不能传递进去的
# # 请求头定制
# # 注意: url,headers不能使用位置传参,因为存在参数顺序

# request = urllib.request.Request(url = url,headers = headers)
# response = urllib.request.urlopen(request)#urlopen 可以传入一个Request 对象
# html = response.read().decode('utf-8')
# print(html)

"""
编解码
"""
# # https://www.baidu.com/s?wd=汽车之家
# # 编码 quote()
# # 解码 unquote()
# import urllib.request
# import urllib.parse
# url = "https://www.baidu.com/s?wd="
# # wd = 汽车之家
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
# }
# #将汽车之家四个字进行编码操作，unicode编码
# word = urllib.parse.quote('汽车之家')
# word_test = urllib.parse.unquote('%E6%B1%BD%E8%BD%A6%E4%B9%8B%E5%AE%B6')
# print(word_test)

# url = url + word
# print(url)

"""
urlencode()多个参数传递
"""
# https://www.baidu.com/s?wd=%E8%BF%AA%E4%B8%BD%E7%83%AD%E5%B7%B4&sex=%E5%A5%B3&location=%E6%96%B0%E7%96%86
# import urllib.request
# import urllib.parse

# base_url = "https://www.baidu.com/s?"

# data = {
#     'wd':'迪丽热巴',
#     'sex':'女',
#     'location':'新疆'
# }
# new_data = urllib.parse.urlencode(data)
# print(new_data)
# url = base_url + new_data

# #请求头
# headers = {
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
# }

# # 请求对象定制
# request = urllib.request.Request(url = url, headers = headers)

# #发送请求
# response = urllib.request.urlopen(request)

# content = response.read().decode('utf-8')
# print(content)

"""
post 请求
"""
# import urllib.request
# import urllib.parse
# import json

# # 百度翻译
# # https://fanyi.baidu.com/sug
# url = "https://fanyi.baidu.com/sug"
# headers = {
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
# }

# data = {
#     'kw':'中国'
# }

# #post请求参数必须要进行编码urlopen()后加入encode('utf-8')
# data = urllib.parse.urlencode(data).encode('utf-8')
# # print(data) #b'kw=%E6%9C%80%E7%BB%88%E5%B9%BB%E6%83%B314'

# #post请求的参数是不会拼接在url后面,而是需要放在请求对象定制的参数中
# request = urllib.request.Request(url = url,data = data,headers = headers)

# # 模拟浏览器向服务器发送请求
# response = urllib.request.urlopen(request)

# #获取响应的数据
# content = response.read().decode('utf-8')
# # print(type(content))  # <class 'str'>

# # 将字符串转换为json
# obj = json.loads(content)
# print(obj)

"""
总结：
post请求注意事项:
    1、post请求方式的参数必须编码  data = urllib.parse.urlencode(data)
    2、编码之后,必须调用encode()方法   data = urllib.parse.urlencode(data).encode('utf-8')
    3、参数是放在请求对象Request()定制中

get请求
    1、get请求方式的参数必须编码,参数是拼接在url后面,编码之后不需要encode()方法    

"""

"""
ajax的get请求
"""
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=20&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=40&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=60&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=80&limit=20

# import urllib.request

# url = 'https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20'

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
# }

# #请求对象定制

# request = urllib.request.Request(url = url,headers = headers)

# #获取响应数据
# response = urllib.request.urlopen(request)
# content = response.read().decode('utf-8')

# #将json数据下载到本地
# with open('douban.json','w',encoding = 'utf-8') as file:
#     file.write(content)


"""
抓取豆瓣电影10页json数据
"""


# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=20&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=40&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=60&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=80&limit=20



# import urllib.request
# import urllib.parse

# #发送请求
# def create_request(page):
#     base_url = "https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&"
#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'

#     }
#     data = {
#         'start':(page - 1) * 20,
#         'limit':20
#     }
#     data = urllib.parse.urlencode(data)
#     url = base_url + data
#     request = urllib.request.Request(url = url,headers = headers)
#     return request

# #获取数据
# def get_content(request):
#     response = urllib.request.urlopen(request)
#     content = response.read().decode('utf-8')
#     return content

# #下载数据
# def down_load(page,content):
#     with open('douban' + str(page) + '.json','w',encoding = 'utf-8') as f:
#         f.write(content)

# #主程序

# if __name__ == '__main__':
#     #开始
#     start_page = int(input('请输入起始页码:'))
#     #结束
#     end_page = int(input('请输入结束页码'))

#     #使用for循环抓取10页内容
#     for page in range(start_page,end_page + 1):
#         #发送请求(请求头定制)
#         request = create_request(page)
#         #获取响应
#         content = get_content(request)
#         #下载
#         down_load(page,content)

"""
ajax的post请求
"""
"""
https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname

cname: 合肥
pid: 
pageIndex: 3
pageSize: 10
"""

# import urllib.request
# import urllib.parse
# # 请求头定制
# def create_request(page):
#     base_url = "https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
#     headers = {
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
#     }

#     data = {
#         "cname": "合肥",
#         "pid": "",
#         "pageIndex": page,
#         "pageSize": 10
#     }

#     data = urllib.parse.urlencode(data).encode('utf-8')
#     request = urllib.request.Request(url = base_url, data =data ,headers = headers)
#     return request

# #获取数据
# def get_content(request):
#     response = urllib.request.urlopen(request)
#     content = response.read().decode('utf-8')
#     return content

# #下载数据
# def down_load(page,content):
#     with open('kfc' + str(page) + '.json','w',encoding = 'utf-8') as file:
#         file.write(content)



# # 主程序
# if __name__ == '__main__':
#     start_page = int(input("请输入起始页码:"))
#     end_page = int(input("请输入结束页码:"))
#     for page in range(start_page,end_page + 1):
#         # 请求头定制
#         request = create_request(page)
#         #获取数据
#         content = get_content(request)
#         #下载数据
#         down_load(page,content)

# import urllib.request

# url = "https://www.baidu.com/"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
# }
# request = urllib.request.Request(url=url,headers=headers)

# #1.获取handler对象
# handler = urllib.request.HTTPHandler()
# #2.获取opener对象
# opener = urllib.request.build_opener(handler)
# #3.调用opener的open方法,发送请求,获取响应
# response = opener.open(request)
# #4.读取数据

# content = response.read().decode('utf-8')
# print(content)

"""
IP代理
"""
# import urllib.request
# url = "https://www.baidu.com/"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
# }
# #请求头定制
# request = urllib.request.Request(url = url,headers = headers)

# #IP代理池
# proxies = {
#     "https": "114.35.177.252:8089"
# }

# #1 获取handler对象
# handler = urllib.request.ProxyHandler(proxies = proxies)

# #2  获取opener对象
# opener = urllib.request.build_opener(handler)

# #3 调用open方法
# response = opener.open(request)

# #4 获取响应
# content = response.read().decode('utf-8')

# print(content)


"""
xpath
(1) 节点(node)：
    a、元素节点:XML的基本构成单元,对应xml中的标签,如:<html></html>
    b、属性节点:元素的属性,如:<ul class = 'xxxx'>
    c、文本节点；元素或属性中的文本内容,<span>xxxx</span>
    d、根节点:整个xml文档的根元素,
    e、父节点、子节点、兄弟节点:节点之间的关系

(2) 路径表达式
    a、绝对路径:从根节点开始选择节点:如:/html/body/div/div/a
    b、相对路径:从当前节点开始选择节点: 如：a

2、基本语法
    (1)节点选择
        a、元素节点： /html/body/div/div/a
        b、属性节点 /html/body/@class
        c、文本节点 /html/body/div/div/a[1]/text()
    (2)运算符
    a、斜杠 / 从跟节点选择
    b、双斜杠 // 从匹配选择的当前节点选择文本中的节点：
    c、点 . 选取当前节点
    d、双点 .. 选取父节点
    e、属性符号 @ 选取属性

    (3)谓词
    a 通过位置选择
    第一个 //div[@id='s-top-left']/a[1]
    最后一个 //div[@id='s-top-left']/a[last()]
    前4个   //div[@id='s-top-left']/a[position() < 4]
    b 通过属性选择
    /html/body[@class='cos-pc']/div/div[@class='s_tab']
    （4）函数
    a 字符串函数
        contains :检查字符串是否包含子字符串
        starts-with: 检查字符串是否以子字符串开头
        string-length： 检查字符串是否以子字符串开头
    b 数字函数
        sum:计算节点集的和
        floor:向下取整
        ceiling:向上取整
    c 布尔函数:
        boolean:将值转换为布尔值
    （5）逻辑运算符
        and：用于连接两个条件，只有当两个条件都为真时才返回真
        or ：用于连接两个条件，只要有一个条件为真，则返回真
        not ：用于返回条件的否定
"""

"""
使用Xpath解析
1、本地文件
2、服务器响应文件（重点）
"""

"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>合肥</title>
</head>
<body>
    <ul>
        <li id="hflz1" class="c1">合肥</li>
        <li id="l2">蜀山区</li>
        <li id="bhl3">包河区</li>
        <li>瑶海区</li>
        <li id="l5" class="c5">庐阳区</li>
        <li id="l6">高新区</li>
        <li id="l7">政务区</li>
    </ul>
</body>
</html>

"""

from lxml import etree

#解析本地文件
html_etree = etree.parse('D:\\vscode_code\\day12_spider\\hello.html')
# print(html_etree)

#1.查找ul下面的li标签
# li_list = html_etree.xpath('/html/body/ul/li')
# print(li_list)
# li_list  = html_etree.xpath('//ul/li')
# print(li_list)
# li_list  = html_etree.xpath('//li/.')
# print(li_list)


# 2、查找所有id属性的li标签
# li_list  = html_etree.xpath('//li[@id]')
# print(li_list)
"""
[<Element li at 0x1f689917b80>, <Element li at 0x1f689917f40>, <Element li at 0x1f689917f00>, <Element li at 0x1f689917f80>, <Element 
li at 0x1f689917fc0>, <Element li at 0x1f689928080>]
"""
# li_list  = html_etree.xpath('//li[@id]/text()')
# print(li_list)#['合肥', '蜀山区', '包河区', '庐阳区', '高新区', '政务区']

# 3.查找id为l2的li标签
# li_list  = html_etree.xpath('//ul/li[@id = "l2"]/text()')
# print(li_list)#['蜀山区']

#4.查找id为l5标签的class属性值
# li_list  = html_etree.xpath('//ul/li[@id = "l5"]/@class')
# print(li_list)#['c5']

# 5、查找id中包含lz的li标签
# li_list = html_etree.xpath('//ul/li[contains(@id,"lz")]/text()')
# print(li_list)#['合肥']


# 6、查找id的值以l开头的li标签
# li_list = html_etree.xpath('//ul/li[starts-with(@id,"l")]/text()')
# print(li_list)#['蜀山区', '庐阳区', '高新区', '政务区']


# 7、查找id为 l6 和 l7的li标签
# li_list  = html_etree.xpath('//ul/li[@id = "l6"] or li[@id = "l7"]')   # 错误示范
# li_list  = html_etree.xpath('//ul/li[@id="l5" and @class="c5"]/text()')
# print(li_list)#['庐阳区']


# 8、查找前三li标签
# li_list = html_etree.xpath('//ul/li[position() < 4]/text()')
# print(li_list)#['合肥', '蜀山区', '包河区']


"""
解析服务器响应文件
"""

# import urllib.request
# from  lxml import etree

# url = "https://www.baidu.com/"
# headers={
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
# }

# # 请求对象定制
# request = urllib.request.Request(url = url,headers = headers)

# # 模拟浏览器发送请求
# response = urllib.request.urlopen(request)

# #获取源代码
# content = response.read().decode('utf-8')

# #解析服务器响应文件
# tree = etree.HTML(content)

# #使用xpath提取想要的数据
# result = tree.xpath('//input[@id = "su"]/@value')[0]

# text = tree.xpath('//ul[@id = "hotsearch-content-wrapper"]/li[1]/a/span[2]/text()')
# print(text)#['中俄元首会谈达成哪些新的重要共识']

"""
https://pic.netbian.com/4kfengjing/
"""
# import urllib.request
# import urllib.parse
# from lxml import etree

# #请求头定制
# def create_request(page):
#     if page == 1:
#         url = "https://sc.chinaz.com/tupian/taikongkexuetupian.html"
#     else:
#         url = "https://sc.chinaz.com/tupian/taikongkexuetupian_" + str(page) + ".html"
    
#     headers = {
#         "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
#     }

#     request = urllib.request.Request(url = url,headers = headers)
#     return request

# #获取数据
# def get_content(request):
#     response = urllib.urlopen(request)
#     content = response.read().decode('utf-8')
#     return content

# #下载
# def down_load(content):
#     tree = etree.HTML(content)
#     name_list = tree.xpath('//div[@class = "container"]//img/@alt')
#     img_list = tree.xpath('//div[@class="container"]//img/@data-original')

#     for i in range(len(name_list)):
#         name = name_list[i]
#         src = img_list[i]
#         url = 'https:' + src
#         urllib.request.urlretrieve(url = url,filename = './img/' + name + ".jpg")



# if __name__ == '__main__':
#     #起始页:
#     start_page = int(input("请输入起始页面"))
#     # 结束页
#     end_page = int(input("请输入结束页码："))
#     # 使用for循环遍历所有页面
#     for page in range(start_page,end_page + 1):
#         # 请求头定制
#         request = create_request(page)
#         # 获取数据
#         content = get_content(request)
#         # 下载数据
#         down_load(content)
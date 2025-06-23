import csv
import json
# import scrapy
# from scrapy import Request
import requests
from lxml import etree

"""
开始界面
url = https://www.autohome.com.cn/hefei/?from=m

新能源汽车名字
https://car-web-api.autohome.com.cn/car/search/searchcar?searchtype=6&pageindex=1&pagesize=20&orderid=0&state=2
https://car-web-api.autohome.com.cn/car/search/searchcar?searchtype=6&pageindex=2&pagesize=20&orderid=0&state=2

seriesid: 车id
seriesname:车名字
seriesminprice:开始价格
seriesmaxprice:结束价格
average:口碑评分
specnum:符合条件类型的车数量
specids:符合条件类型的车的id列表




汽车头标
https://car-web-api.autohome.com.cn/car/series/seires_city?seriesids=5499%2C6388%2C7658%2C7569%2C6669%2C7076%2C5346%2C7752%2C7877%2C7928%2C5714%2C7588%2C8005%2C6643%2C6576%2C7915%2C7674%2C7353%2C7851%2C7859&cityid=340100&filteranktag=1

newsprice：指导价
dealerid：店地址id
cityid：上牌id
tag：排名
date：日期

汽车具体页面
https://www.autohome.com.cn/spec/71933/


小店：
https://dealer.autohome.com.cn/2094804/


"""


# 得出汽车数据和id列表
def car_data(data_list):
    #遍历汽车数据
    car_list = []
    seriesid_list = []
    for data in data_list:
        #定义一个 seriesid_list用于打开汽车头标网页
        car_id = data.get('seriesid')
        car_name = data.get('seriesname')
        car_min_price = data.get('seriesminprice')
        car_max_price = data.get('seriesmaxprice')
        car_star = data.get('average')
        car_similar_num = data.get('specnum')
        # car_similar_id = data.get('specids')
        # 汽车数据的列表
        car_list.append([car_id,
                        car_name,
                        car_min_price,
                        car_max_price,
                        car_star,
                        car_similar_num,
                        # car_similar_id
                        ])
        #汽车id的列表
        seriesid_list.append(car_id)
        # print(seriesid_list)
    return car_list,seriesid_list

# 汽车头部信息
def car_head(seriesid_list,car_list):
    # 构建url
   
    url = "https://car-web-api.autohome.com.cn/car/series/seires_city?seriesids="
    url = url + str(seriesid_list[0])
    seriesid_list.pop(0)
    # print(seriesid_list)
    for seriesid in seriesid_list:
        url = url + '%2C' + str(seriesid)
    url = url + '&cityid=340100&filteranktag=1'
    # print(url)
    response = requests.get(url = url,headers = headers)
    content = json.loads(response.text)
    # 获取数据列表
    headlist = content.get('result').get('serieslist')
    # print(headlist)
    i = 0
    for head in headlist:
        newsprice = head.get('dealeraskprice').get('newsprice','暂无')
        tag = head.get('taginfo').get('tag')
        if tag == '':
            tag = '暂无'
        # print(tag)
        date = head.get('taginfo').get('filter','暂无')
        if date != '暂无':
            date = head.get('taginfo').get('filter','暂无').get('date','暂无')
        car_list[i].append(newsprice)
        car_list[i].append(tag)
        car_list[i].append(date)
        i += 1
    # print(car_list)
    return car_list

# 将数据写入到csv文件中
def save_csv(filename,data):
    with open(filename,'w',encoding = 'utf-8',newline = '') as f:
        writer = csv.writer(f)
        # 将所有行一次性写入
        writer.writerow(["车id",
                    "车名字",
                    "最小价格",
                    "最大价格",
                    "口碑评分",
                    "符合条件类型的车数量",
                    # "符合条件类型的车的id列表",
                    '指导价',
                    '排名',
                    '日期'])
        writer.writerows(data)

#符合车类型的车名字
"""
汽车具体页面
https://www.autohome.com.cn/spec/71933/
"""
# def similar_car_name(car_list):
#     for car in car_list:
#         car_nameid_list = car[6]
#         for id in car_nameid_list:

    
# #给出指导价的店名字
# def shop_name():
#     pass
# 主抓去

#开始页面
start_page = int(input('请输入开始页数:'))
#结束页面
end_page = int(input('请输入结束页数:'))

headers = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    'referer':'https://www.autohome.com.cn/'
}

# class AutohomeSpider(scrapy.Spider):
#     name = "autohome"
#     # allowed_domains = ["autohome.com"]
#     # start_urls = ["https://autohome.com"]

    # def start_reqursts(self):
# car_list = []
# seriesid_list = []
final_car_list = []
for num in range(start_page,end_page):
    url = 'https://car-web-api.autohome.com.cn/car/search/searchcar?searchtype=6&pageindex='+str(num)+'&pagesize=20&orderid=0&state=2'
    # print(url)
    response = requests.get(url = url,headers = headers)
    content = response.text
    data = json.loads(content)
    #获取汽车搜索页面的汽车数据列表,一面20页
    data_list = data.get('result').get('seriesgrouplist')
    car_list,seriesid_list = car_data(data_list)
    car_list = car_head(seriesid_list,car_list)
    # print(car_list)
    final_car_list.extend(car_list)
    # print(final_car_list)
save_csv('D:\\vscode_code\python train\data/car.csv',final_car_list)


# print(data_list)
# print(content)

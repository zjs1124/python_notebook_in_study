import json
import scrapy
from scrapy import Request



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

#开始页面
start_page = int(input('请输入开始页面'))
#结束页面
end_page = int(input('请输入结束页面'))

headers = {
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    'referer':'https://www.autohome.com.cn/'
}

class AutohomeSpider(scrapy.Spider):
    name = "autohome"
    # allowed_domains = ["autohome.com"]
    # start_urls = ["https://autohome.com"]

    def start_reqursts(self):
        url = 'https://car-web-api.autohome.com.cn/car/search/searchcar?searchtype=6&pageindex=1&pagesize=20&orderid=0&state=2'
        yield Request(url = url,headers = headers,callback = self.parse)

    def parse(self, response):
        car_info = json.loads(response)
        print(car_info)

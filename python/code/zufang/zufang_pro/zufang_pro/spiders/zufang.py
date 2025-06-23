from email.policy import default
import json
import scrapy

from scrapy import Request
from zufang_pro.items import ZufangProItem

"""

https://hf.lianjia.com/zufang/pg1/
https://hf.lianjia.com/zufang/pg2/
https://hf.lianjia.com/zufang/pg3/
"""

"""
base_url = "https://hf.lianjia.com/zufang"
"""

# 爬虫类
class ZufangSpider(scrapy.Spider):
    #爬虫名称
    name = "zufang"
    # 爬虫域名
    # allowed_domains = ["lianjia.com"]
    # 爬虫起始url列表
    # start_urls = ["https://lianjia.com"]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36" 
    }

    # 当前页
    local_page = 1
    # 结束页
    end_page = 0

    # 获取第一页的数据
    # 重写父类的start_requests方法
    def start_requests(self):
        url = "https://hf.lianjia.com/zufang/"
        # 生成请求对象
        yield Request(url=url,headers=self.headers,callback = self.parse)

    # 解析函数
    def parse(self, response):
        # 获取所有数据的数据集
        house_info = response.xpath("//div[@class='content__list--item--main']")
        #使用for循环遍历数据集
        for house in house_info:
            # 依次取出数据
            # 租房类型
            rental_type = house.xpath("./p[1]/a/text()").get().strip()
            # 房屋的市区位置
            city = house.xpath("./p[2]/a[1]/text()").get()
            # 房屋的街道位置
            street = house.xpath("./p[2]/a[2]/text()").get()
            # 小区的名称
            name = house.xpath("./p[2]/a[3]/text()").get()
            # 房屋的面积
            area = house.xpath("./p[2]/i[1]/following-sibling::text()[1]").get(default = "暂无数据").strip()
            # 房屋的朝向
            direction = house.xpath("./p[2]/i[2]/following-sibling::text()[1]").get(default = "暂无数据").strip()
            # 房屋的户型
            house_type = house.xpath("./p[2]/i[3]/following-sibling::text()[1]").get(default = "暂无数据").strip()
            # 房屋的月租
            month_rent = house.xpath("./span/em/text()").get(default = "暂无数据").strip()
            # 赋值给具体的类型
            items = ZufangProItem()
            items['rental_type'] = rental_type
            items['city'] = city
            items['street'] = street
            items['name'] = name
            items['area'] = area
            items['direction'] = direction
            items['house_type'] = house_type
            items['month_rent'] = month_rent

            #获取详情页的url
            base_url = house.xpath('./p[1]/a/@href').extract_first()
            url = "https://hf.lianjia.com" + base_url
            # 发送请求
            yield Request(url = url,headers = self.headers,meta = {'items':items},callback = self.detail_parse)
        
        #获取下一页的url，并生成一个request请求
        if self.local_page == 1:
            self.end_page = response.xpath("//div[@class='content__pg']/@data-totalpage").get()
            # 类型转换，将end_page从字符串类型转换成int类型
            self.end_page = int(self.end_page)
        # 下一页的值
        self.local_page += 1
        # 判断当前页数是否越界
        if self.local_page <= 10:
            nex_url = "https://hf.lianjia.com/zufang/pg%d"%(self.local_page) + "/#contentList"
            yield Request(url=nex_url,headers=self.headers,callback=self.parse)

    # 详情页解析
    def detail_parse(self, response):   
        # 获取主页面房屋信息数据
        item = response.meta['items']

        # 获取中介信息
        agent_info = response.xpath("//div[@class='ke-agent-data']/@data-agent").get()
        # 由于观察详情页面的数据，发现经纪人信息并不是都存在，所以需要判断
        if agent_info:

            try:
                result_dict = json.loads(agent_info)
            except json.JSONDecodeError as e:
                print(f"Json解析错误{e}")
                result_dict = {}
        else:
            result_dict = {}
         # 中介信息
        # name_value  feedbackScore  jobTitle
        name_value = result_dict.get("name")
        # 反馈评分
        feedbackScore = result_dict.get("feedbackScore")
        # 经纪人职位
        jobTitle = result_dict.get("jobTitle")

        item['name_value'] = name_value
        item['feedbackScore'] = feedbackScore
        item['jobTitle'] = jobTitle

        yield item
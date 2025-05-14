from email.policy import default

import scrapy  # 导包
import json
from scrapy import Request

from zufang_pro.items import ZufangProItem


# rental_type   city  street  name area  direction  house_type  month_rent

# 爬虫的类
class HefeiSpider(scrapy.Spider):
    # 爬虫的名称
    name = "hefei"
    # 爬虫的域名
    # allowed_domains = ["hf.lianjia.com"]
    # 起始url列表
    # start_urls = ["https://hf.lianjia.com"]
    """
    https://hf.lianjia.com/zufang/pg1
    https://hf.lianjia.com/zufang/pg2
    https://hf.lianjia.com/zufang/pg3
    
    https://hf.lianjia.com/zufang/
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    # 当前页
    current_page = 1
    # 结束页面
    end_page = 0



    # 重写父类的start_requests方法
    def start_requests(self):
        url = "https://hf.lianjia.com/zufang/"
        # 生成请求对象
        yield  Request(url=url,headers=self.headers)

    # 解析函数
    def parse(self, response):
        # xpath
        # print(response.status)
        # print(response.text)
        # 获取所有数据的数据集
        house_info = response.xpath("//div[@class='content__list--item--main']")
        print(house_info)
        #使用for循环遍历house_info
        for info in house_info:
            # 依次取出数据
            # 租房类型
            rental_type = info.xpath("p[1]/a/text()").get().strip()
            print(rental_type)
            # 房屋的市区
            city = info.xpath("p[2]/a[1]/text()").get()
            # 房屋的街道
            street = info.xpath("p[2]/a[2]/text()").get()
            # 小区的名称
            name = info.xpath("p[2]/a[3]/text()").get()   # extract() 提取
            # 房屋的面积
            # 租房数据中包含公寓信息（广告），可能存在area数据不存在
            area = info.xpath("p[2]/i[1]/following-sibling::text()[1]").get(default="暂无数据").strip()
            # 朝向
            direction = info.xpath("p[2]/i[2]/following-sibling::text()[1]").get(default="暂无数据").strip()
            # 房屋的类型
            house_type = info.xpath("p[2]/i[3]/following-sibling::text()[1]").get(default="暂无数据").strip()
            # 月租
            month_rent = info.xpath("span/em/text()").get()
            items = ZufangProItem()
            items['rental_type'] = rental_type
            items['city'] = city
            items['street'] = street
            items['name'] = name
            items['area'] = area
            items['direction'] = direction
            items['house_type'] = house_type
            items['month_rent'] = month_rent
            # yield items

            # 获取详情页的url
            base_url = info.xpath("p[1]/a/@href").extract_first()  # /zufang/HF2025773506649653248.html
            url = "https://hf.lianjia.com" + base_url
            # print(url)
            # 发送请求
            yield  Request(url=url,headers=self.headers,meta={'items':items},callback=self.parse_detail)


        #获取下一页的url，并生成一个request请求
        if self.current_page == 1:
            self.end_page =response.xpath("//div[@class='content__pg']/@data-totalpage").get()
            # 类型转换，将end_page从字符串类型转换成int类型
            self.end_page = int(self.end_page)
        # 下一页的值
        self.current_page += 1
        # 判断当前页数是否越界
        if self.current_page <= 10:
            nex_url = "https://hf.lianjia.com/zufang/pg%d"%(self.current_page) + "/#contentList"
            yield Request(url=nex_url,headers=self.headers,callback=self.parse)

    # 详情页解析函数
    def parse_detail(self,response):
        # 获取主页面房屋信息数据
        item = response.meta['items']

        # 获取中介信息
        agent_info = response.xpath("//div[@class='ke-agent-data']/@data-agent").get()
        # result_dict = json.loads(agent_info)
        # print(result_dict)
        # 由于观察详情页面的数据，发现经纪人信息并不是都存在，所以需要判断
        if agent_info:
            # 捕获异常的形式
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



        # 房屋信息
        # # 找到一个房屋信息的数据集
        # house_info = response.xpath("//div[@id='info']")
        # # 使用for循环遍历
        # for info in house_info:

        yield item



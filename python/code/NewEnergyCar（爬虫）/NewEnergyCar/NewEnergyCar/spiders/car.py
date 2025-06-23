

import scrapy
from scrapy import Request

from NewEnergyCar.items import NewenergycarItem


class CarSpider(scrapy.Spider):
    name = "car"
    allowed_domains = ["che168.com"]
    start_urls = ["https://www.che168.com/shanghai/a0_0msdgscncgpi1ltocsp1exf4/?pvareaid=102179"]
    current_page = 1
    end_page = 30
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # 设置请求间隔为2秒
        'COOKIES_ENABLED': True,  # 启用Cookies
        'AUTOTHROTTLE_ENABLED': True,  # 启用AutoThrottle
        'AUTOTHROTTLE_START_DELAY': 1,  # 初始下载延迟
        'AUTOTHROTTLE_MAX_DELAY': 60,  # 最大下载延迟
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # 并发请求数
        'AUTOTHROTTLE_DEBUG': False,  # 是否调试AutoThrottle
        'DOWNLOADER_MIDDLEWARES': {
            'NewEnergyCar.middlewares.SeleniumMiddleware': 800,
        },
    }

    def start_requests(self):
        url = "https://www.che168.com/shanghai/a0_0msdgscncgpi1ltocsp1exf4/?pvareaid=102179"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        yield Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        car_info = response.xpath("//ul[@class='viewlist_ul']/li/a[@class='carinfo']")
        for car in car_info:
            items = NewenergycarItem()
            # 汽车名称
            car_name = car.xpath("div[@class='cards-bottom']/h4[@class='card-name']/text()").get()
            print(car_name)
            # 汽车信息（表显里程/上牌时间/车辆所在地/会员级别）
            cards_unit = car.xpath("div[@class='cards-bottom']/p[@class='cards-unit']/text()").get()
            # 汽车价格
            price = car.xpath("div[@class='cards-bottom']/div[@class='cards-price-box']/span[@class='pirce']/em/text()").get()
            # 新车含税价
            price_tax = car.xpath("div[@class='cards-bottom']/div[@class='cards-price-box']/s/text()").get()
            items['car_name'] = car_name
            items['cards_unit'] = cards_unit
            items['price'] = price
            items['price_tax'] = price_tax

            # 获取详情页链接
            car_base__url = car.xpath("@href").get()
            car_url = "https://www.che168.com" + car_base__url
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
            }
            yield Request(url=car_url, headers=headers, meta={"items": items}, callback=self.car_info_details_parse)

        # 获取下一页url并发送request请求
        if self.current_page < self.end_page:
            next_page = self.current_page + 1
            next_url = f"https://www.che168.com/shanghai/a0_0msdgscncgpi1ltocsp{next_page}exf4/?pvareaid=102179"
            self.current_page += 1
            yield Request(url=next_url, headers=headers, callback=self.parse)

    def car_info_details_parse(self, response):
        items = response.meta['items']
        vehicle_profile = response.xpath("//div[@class='all-basic-content fn-clear']")
        for vehicle in vehicle_profile:
            # 变速箱
            gearbox = vehicle.xpath("ul[1]/li[3]/text()").get()
            # 燃料类型
            fuel_type = vehicle.xpath("ul[1]/li[4]/text()").get()
            # CLTC纯电续航里程
            cltc_pure_electricity_endurance_mileage = vehicle.xpath("ul[1]/li[5]/text()").get()
            # 发布时间
            release_time = vehicle.xpath("ul[1]/li[6]/text()").get()
            # 年检到期
            annual_inspection_expiration = vehicle.xpath("ul[2]/li[1]/text()").get()
            # 保险到期
            insurance_expiration = vehicle.xpath("ul[2]/li[2]/text()").get()
            # 质保到期
            warranty_expiration = vehicle.xpath("ul[2]/li[3]/text()").get()
            # 过户次数
            transfer_times = vehicle.xpath("ul[2]/li[5]/text()").get()
            # 标准快充
            standard_fast_charge = vehicle.xpath("ul[2]/li[7]/text()").get()
            # 发动机
            engine = vehicle.xpath("ul[3]/li[1]/text()").get()
            # 车辆级别
            vehicle_level = vehicle.xpath("ul[3]/li[2]/text()").get()
            # 车身颜色
            vehicle_color = vehicle.xpath("ul[3]/li[3]/text()").get()
            # 驱动方式
            drive_mode = vehicle.xpath("ul[3]/li[4]/text()").get()
            # 标准容量
            standard_capacity = vehicle.xpath("ul[3]/li[6]/text()").get()
            # 标准慢充
            standard_slow_charge = vehicle.xpath("ul[3]/li[7]/text()").get()
            items['gearbox'] = gearbox
            items['fuel_type'] = fuel_type
            items['cltc_pure_electricity_endurance_mileage'] = cltc_pure_electricity_endurance_mileage
            items['release_time'] = release_time
            items['annual_inspection_expiration'] = annual_inspection_expiration
            items['insurance_expiration'] = insurance_expiration
            items['warranty_expiration'] = warranty_expiration
            items['transfer_times'] = transfer_times
            items['standard_fast_charge'] = standard_fast_charge
            items['engine'] = engine
            items['vehicle_level'] = vehicle_level
            items['vehicle_color'] = vehicle_color
            items['drive_mode'] = drive_mode
            items['standard_capacity'] = standard_capacity
            items['standard_slow_charge'] = standard_slow_charge

        # 配置亮点
        configuration_highlights = response.xpath("//ul[@id='caroptionulid']/li/p[@class='item-status']/text()").getall()
        configuration_highlights_text = '/'.join(configuration_highlights).strip()
        items['configuration_highlights_text'] = configuration_highlights_text

        yield items
"""
car_name(汽车名称)
cards_unit(汽车信息（表显里程/上牌时间/车辆所在地/会员级别）)
price(汽车价格)
price_tax(新车含税价)
gearbox(变速箱)
fuel_type(燃料类型)
cltc_pure_electricity_endurance_mileage(CLTC纯电续航里程)
release_time(发布时间)
annual_inspection_expiration(年检到期)
insurance_expiration(保险到期)
warranty_expiration(质保到期)
transfer_times(过户次数)
standard_fast_charge（标准快充）
engine(发动机)
vehicle_level(车辆级别)
vehicle_color(车身颜色)
drive_mode(驱动方式)
standard_capacity(标准容量)
standard_slow_charge(标准慢充)
configuration_highlights_text(配置亮点)
"""
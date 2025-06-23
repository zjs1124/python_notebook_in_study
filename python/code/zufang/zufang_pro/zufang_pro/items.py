# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangProItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
     # 租房类型
    rental_type = scrapy.Field()
    # 房屋的市区位置
    city = scrapy.Field()
    # 房屋的街道位置
    street = scrapy.Field()
    # 小区的名称
    name = scrapy.Field()
    # 房屋的面积
    area = scrapy.Field()
    # 房屋的朝向
    direction = scrapy.Field()
    # 房屋的户型
    house_type = scrapy.Field()
    # 房屋的月租
    month_rent = scrapy.Field()

    # 中介信息
    # name_value  feedbackScore  jobTitle
    name_value = scrapy.Field()
    feedbackScore = scrapy.Field()
    jobTitle = scrapy.Field()










    pass

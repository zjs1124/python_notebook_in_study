# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewenergycarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    car_name = scrapy.Field()
    cards_unit = scrapy.Field()
    price = scrapy.Field()
    price_tax = scrapy.Field()
    gearbox = scrapy.Field()
    fuel_type = scrapy.Field()
    cltc_pure_electricity_endurance_mileage = scrapy.Field()
    release_time = scrapy.Field()
    annual_inspection_expiration = scrapy.Field()
    insurance_expiration = scrapy.Field()
    warranty_expiration = scrapy.Field()
    transfer_times = scrapy.Field()
    standard_fast_charge = scrapy.Field()
    vehicle_level = scrapy.Field()
    engine = scrapy.Field()
    vehicle_color = scrapy.Field()
    drive_mode = scrapy.Field()
    standard_capacity = scrapy.Field()
    standard_slow_charge = scrapy.Field()
    configuration_highlights_text = scrapy.Field()

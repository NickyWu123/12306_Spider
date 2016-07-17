# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ProvinceItem(scrapy.Item):
    name = scrapy.Field()    

class AgencyItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    windows = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()

class CommitItem(scrapy.Item):
    pass

class StationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bureau = scrapy.Field()
    station = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    passenger = scrapy.Field()
    luggage = scrapy.Field()
    package = scrapy.Field()

class BriefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()

class InfoItem(scrapy.Item):
    train_no=scrapy.Field()
    no=scrapy.Field()
    station=scrapy.Field()
    type=scrapy.Field()
    start_time=scrapy.Field()
    arrive_time=scrapy.Field()
    stopover_time=scrapy.Field()

class CodeItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    turn = scrapy.Field()

class BriefDeltaItem(scrapy.Item):
    code = scrapy.Field()
    seat_type = scrapy.Field()


class TicketItem(scrapy.Item):
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    swz = scrapy.Field()
    tz = scrapy.Field()
    zy = scrapy.Field()
    ze = scrapy.Field()
    gr = scrapy.Field()
    rw = scrapy.Field()
    yw = scrapy.Field()
    rz = scrapy.Field()
    yz = scrapy.Field()
    wz = scrapy.Field()
    qt = scrapy.Field()

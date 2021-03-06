# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from tutorial.items import StationItem
from tutorial.items import CommitItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class StationsSpider(scrapy.Spider):
    name = "stations"
    # start_urls = (
    #     'http://www.12306.cn/mormhweb/kyyyz/',
    # )
    custom_settings = {
        'ITEM_PIPELINES': {
                'tutorial.pipelines.StationSQLPipeline': 300,
         },
         'DOWNLOADER_MIDDLEWARES': {
                'tutorial.middle.DownloaderMiddleware': 500,
            },
        'DUPEFILTER_CLASS': "tutorial.filter.URLTurnFilter",
        'JOBDIR': "s/stations",
    }
    def __init__(self, *a, **kw):
        super(StationsSpider, self).__init__(self.name, **kw)
        self.turn = a[0]
        self.logger.info("%s. this turn %d" % (self.name, self.turn)) 

    def start_requests(self):
        yield Request("http://www.12306.cn/mormhweb/kyyyz/", callback = self.parse, meta = {"turn":self.turn})

    def parse(self, response):
        names = response.css("#secTable > tbody > tr > td::text").extract()
        sub_urls = response.css("#mainTable td.submenu_bg > a::attr(href)").extract()
        for i in range(0, len(names)):
           sub_url1=response.url+sub_urls[i*2][2:]
           yield Request(sub_url1,callback=self.parse_stations,meta={'bureau':names[i],'station':True ,"turn":response.meta["turn"]})
           sub_url2=response.url+sub_urls[i*2+1][2:]
           yield Request(sub_url2,callback=self.parse_stations,meta={'bureau':names[i],'station':True , "turn":response.meta["turn"]})

    def parse_stations(self,response):
        datas=response.css('table table tr')
        #self.logger.debug(datas)
        if len(datas)<2:
           #self.logger.info('no item ' + response.meta["bureau"] + ' ' + response.meta["station"])
           return 
        for i in range(0,len(datas)):
           if i<2:
              continue
           infos=datas[i].css('td::text').extract()
           item=StationItem()
           if len(item)<=3:
               item['luggage']=0
               item["package"]=0
           else:
               item['luggage']=infos[3].strip() != u""
               item["package"] = infos[4].strip() != u""
           item["bureau"] = response.meta["bureau"]
           item["station"] = response.meta["station"]
           item["name"] = infos[0]
           item["address"] = infos[1]
           item["passenger"] = infos[2].strip() != u""
           item["turn"] = response.meta["turn"]
           yield item  
        yield CommitItem()
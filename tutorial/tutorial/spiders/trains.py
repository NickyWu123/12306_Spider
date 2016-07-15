# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import json
import urllib

import scrapy
from scrapy.http.request import Request
from tutorial.items import BriefItem
from tutorial.items import InfoItem
from tutorial.items import CommitItem

class TrainsSpider(scrapy.Spider):
    name = "trains"
    #allowed_domains = ["kyfw.12306.cn/otn/queryTrainInfo/getTrainName"]
    # start_urls = (
    #     'https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?',
    # )
    custom_settings={ 'ITEM_PIPELINES': {
                        'tutorial.pipelines.TrainsSQLPipline': 300,
                    },
    }
    def start_requests(self):
        url = "https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?"
        t = (datetime.datetime.now() + datetime.timedelta(days = 3)).strftime("%Y-%m-%d")
        params = {"date":t}
        
        s_url = url + urllib.urlencode(params)
        self.logger.debug("start url " + s_url)
        yield Request(s_url, callback = self.parse, meta = {"t":t})



    def parse(self, response):
        datas = json.loads(response.body)
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
        for data in datas["data"]:
            item = BriefItem() 
            briefs = data["station_train_code"].split("(")
            item["train_no"] = data["train_no"]
            item["code"] = briefs[0]
            briefs = briefs[1].split("-")
            item["start"] = briefs[0]
            item["end"] = briefs[1][:-1]
            yield item
            params = u"train_no=" + data["train_no"] + u"&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=" + response.meta["t"]
            yield Request(url+params,callback=self.parse_trains_schedule,meta={"train_no":data["train_no"]})

    def parse_trains_schedule(self,response):
        stations = json.loads(response.body)
        nos=[]
        datas = stations["data"]["data"]
        size = len(datas)
        for i in range(0, size):
            data = datas[i]

            info = InfoItem()
            info["train_no"] = response.meta["train_no"];
            info["no"] = int(data["station_no"])
            info["station"] = data["station_name"]
            nos.append(info["no"])
            #主要考虑到no的不确定，可以将一个车次的所有no放入一个集合之中，然后根据集合元素所在的索引判断type
            # print nos.index(info["no"])
            # print len(nos)
            if nos.index(info["no"]) == 0:
                info["type"] = 0
            elif nos.index(info["no"])==size-1:
                info["type"] = 1
            else:
                info["type"] = 2
            
            if data["start_time"] != u"----":
                info["start_time"] = data["start_time"] + u":00";
            else:
                info["start_time"] = None

            if data["arrive_time"] != u"----":
                info["arrive_time"] = data["arrive_time"] + u":00";
            else:
                info["arrive_time"] = None

            if data["stopover_time"] != u"----":
                info["stopover_time"] = data["stopover_time"] + u":00";
            else:
                info["stopover_time"] = None
            # print nos
            yield info
        yield CommitItem()
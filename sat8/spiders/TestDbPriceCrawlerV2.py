# -*- coding: utf-8 -*-
# Dành cho việc test xpath
# @author Justin <cong.itsoft@gmail.com>
# @date 2016-04-07

import scrapy
import datetime
from DbCrawlPriceV2Spider import DbCrawlPriceV2Spider
from scrapy.conf import settings

class TestDbPriceCrawlerV2(DbCrawlPriceV2Spider):

    env = 'testing'

    def parse_detail_content(self, response):
        print self.get_product(response)

    def parseJsonDetailContent(self, response):
        print self.getProductJson(response)

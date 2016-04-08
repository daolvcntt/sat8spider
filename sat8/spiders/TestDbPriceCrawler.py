# -*- coding: utf-8 -*-
# Dành cho việc test xpath
# @author Justin <cong.itsoft@gmail.com>
# @date 2016-04-07

import scrapy
import datetime
from DbPriceCrawler import DbPriceSpider
from scrapy.conf import settings

class TestDbPriceCrawler(DbPriceSpider):

    env = 'testing'

    def parse_detail_content(self, response):
        print self.get_product(response)

# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import DpreviewItemLoader, DpreviewItem
from urlparse import urlparse
from time import gmtime, strftime
from scrapy.conf import settings

from sat8.Functions import parseJson4Params
from sat8.Functions import echo

import json,urllib
from urlparse import urljoin

from sat8.Helpers.Functions import *

class PhonearenaSpider(CrawlSpider):
    name = "dpreview_spider"
    allowed_domains = []
    start_urls = [

    ]

    rules = ()

    env = 'production'

    def __init__(self, env="production"):
        self.env = env;
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@id="combinedProductList"]//td[@class="product"]//div[@class="name"]/a/@href')

        for link in links:
            url = response.urljoin(link.extract());
            yield scrapy.Request(url, callback=self.parseDetailLink)

    def parseDetailLink(self, response):
        item = DpreviewItemLoader(item = DpreviewItem(), response=response)

        item.add_xpath('name', '//*[@class="headerContainer"]//h1/text()')
        item.add_xpath('announce', '//*[@class="shortSpecs"]/text()')

        item = item.load_item()

        item['announce'] = item['announce'].replace("\r\n", '')
        item['announce'] = item['announce'].replace(u"\u2022", '')
        item['announce'] = item['announce'].replace(',', '')
        item['announce'] = item['announce'].strip()

        m,d,y = item['announce'].split(' ')

        if m == 'Jan':
            m = 1
        elif m == 'Feb':
            m = 2
        elif m == 'Mar':
            m = 3
        elif m == 'Apr':
            m = 4
        elif m == 'May':
            m = 5
        elif m == 'Jun':
            m = 6
        elif m == 'July':
            m = 7
        elif m == 'Aug':
            m = 8
        elif m == 'Sep':
            m = 9
        elif m == 'Oct':
            m = 10
        elif m == 'Nov':
            m = 11
        elif m == 'Dec':
            m = 12

        s = str(d) + '/' + str(m) + '/' + str(y)
        t = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
        t = int(t)

        sql = "INSERT INTO dpreviews(name, announce, type) VALUES(%s, %s, %s)"
        self.cursor.execute(sql, (item['name'], t, 'camera'))
        self.conn.commit()

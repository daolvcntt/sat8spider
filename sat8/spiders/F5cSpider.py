# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class F5cSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['f5c.vn']
    start_urls = [

    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@id="widget_product_list"]//a[@class="name-product"]/@href',
        'source' : 'f5c.vn',
        'title' : '//*[@class="entry-detail"]/h1//text()',
        'price' : '//*[@class="entry-detail"]//span[@class="price_new"]//text()',
        'source_id' : 75,
    }


    def start_requests(self):

        urls = []
        for i in range(1,37):
            page = i * 24
            urls.append('http://f5c.vn/laptop.html?cat=11&display_type=0&per_page=' + str(page))

        for i in range(1,3):
            page = i * 24
            urls.append('http://f5c.vn/may-tinh-bang-tablet.html?cat=297&display_type=0&per_page=' + str(page))

        for i in range(1,3):
            page = i * 24
            urls.append('http://f5c.vn/smartphone.html?cat=406&display_type=0&per_page='+ str(page))


        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

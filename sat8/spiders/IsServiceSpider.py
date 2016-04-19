# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime

import json,urllib

class IsServicePriceSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ['www.iservice.vn']

    start_urls = [

    ]

    rules = ()


    def parse_item(self, response):

        jsonresponse = json.loads(response.body_as_unicode())

        product_links = jsonresponse['products']

        for pl in product_links:
            url = pl['href']
            request = scrapy.Request(url, callback = self.parse_detail_content)
            request.meta['product'] = pl
            yield request

    def parse_detail_content(self, response):
        link = response.url

        productMeta = response.meta['product']

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_value('title', productMeta['name'])
        pil.add_value('price', productMeta['price'])
        pil.add_value('source', 'www.iservice.vn')
        pil.add_value('source_id', 105);
        pil.add_value('brand_id', 0);
        pil.add_value('is_phone', 0);
        pil.add_value('is_laptop', 0);
        pil.add_value('is_tablet', 0);
        pil.add_value('link', link)

        product = pil.load_item()

        # Price
        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        product['title'] = product['title'].strip(' \t\n\r')
        product['title'] = product['title'].strip()
        product['name']  = product['title']

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['crawled_at'] = strftime("%Y-%m-%d %H:%M:%S")
        # product['brand']      = (pil.get_value(product['title'])).split(" ")[0]

        yield(product)


    def start_requests(self):
        urls = [
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=20&page=[0-9]+',
                'page' : 3
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=18&page=[0-9]+',
                'page' : 3
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=33&page=[0-9]+',
                'page' : 3
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=57',
                'page' : 1
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=25',
                'page' : 1
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=24',
                'page' : 1
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=76',
                'page' : 1
            },
            {
                'href' : 'http://www.iservice.vn/index.php?route=product/category/ajax&path=133',
                'page' : 1
            },
        ]


        for url in urls:
            for i in range(1, url['page']+1):
                requestUrl = url['href'].replace('[0-9]+', str(i))
                request = scrapy.Request(requestUrl, callback=self.parse_item)
                yield request
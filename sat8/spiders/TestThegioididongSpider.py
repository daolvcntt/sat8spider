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

class TestThegioididongSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ['www.thegioididong.com']

    start_urls = [
        'https://www.thegioididong.com/dtdd/microsoft-lumia-950'
    ]

    rules = ()

    def parse(self, response):
        link = response.url

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@id="topdetail"]//div[@class="rowtop"]/h1[1]/text()')
        pil.add_xpath('price', '//*[@id="topdetail"]//*[@class="boxright"]//*[@class="price_sale"]/strong/text() | //*[@id="topdetail"]//*[@class="boxright"]//strong[@class="pricesell"]/text()')

        pil.add_value('source', 'www.thegioididong.com')
        pil.add_value('source_id', 1);
        pil.add_value('brand_id', 0);
        pil.add_value('is_phone', 0);
        pil.add_value('is_laptop', 0);
        pil.add_value('is_tablet', 0);
        pil.add_value('link', link)

        product = pil.load_item()

        print product
        return

        # Price
        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        # product['title'] = product['title'].strip(' \t\n\r')
        # product['title'] = product['title'].strip()
        # product['name']  = product['title']

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['crawled_at'] = strftime("%Y-%m-%d %H:%M:%S")
        # product['brand']      = (pil.get_value(product['title'])).split(" ")[0]

        print product
        return

        yield(product)


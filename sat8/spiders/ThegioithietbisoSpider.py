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

class ThegioithietbisoSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = []

    start_urls = [

    ]

    rules = ()


    def parse_item(self, response):

        jsonresponse = json.loads(response.body_as_unicode())

        sel = Selector(text=jsonresponse['html'])

        product_links = sel.xpath('//*[@class="product_image"]/a[1]/@href')

        for pl in product_links:
            url = response.urljoin(pl.extract())
            request = scrapy.Request(url, callback = self.parse_detail_content)
            yield request

    def parse_detail_content(self, response):
        link = response.url

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@class="detail_info fl"]/h2[@class="product_name"]/text()')
        pil.add_xpath('price', '//*[@class="content_attribute "]//p[@class="price"]//text()')
        pil.add_value('source', 'thegioithietbiso.vn')
        pil.add_value('source_id', 87);
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

        print product


    def start_requests(self):
        urls = [
            {
                'href' : 'http://thegioithietbiso.vn/ajax/ajax_load_more_product.php',
                'data' : {
                    'id_cat': "2",
                    'type': "",
                    'page': "1",
                    'count': "73",
                    'page_size': "30"
                },
                'max_page' : "2",
                'jump_step' : "1",
                'param_page' : 'page'
            }
        ]

        for url in urls:
            for i in range(1, int(url['max_page'])+1):

                headers = {
                    "X-Requested-With" : "XMLHttpRequest",
                    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
                }

                method = 'POST'

                formData = url['data']

                formData[url['param_page']] = i * url['jump_step']

                request = scrapy.FormRequest(url=url['href'], method=method, formdata=formData, callback=self.parse_item)
                yield request







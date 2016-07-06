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

class BvtMobileSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = []

    start_urls = [

    ]

    rules = ()


    def parse_item(self, response):

        sel = Selector(response)

        product_links = sel.xpath('//*[@class="infomation_1"]/@href')

        for pl in product_links:
            url = response.urljoin(pl.extract())
            request = scrapy.Request(url, callback = self.parse_detail_content)
            yield request

    def parse_detail_content(self, response):
        link = response.url

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@class="detailProduct"]/h1/text()')
        pil.add_xpath('price', '//*[@id="_giasp"]//text()')
        pil.add_value('source', 'bvtmobile.com')
        pil.add_value('source_id', 115);
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

        yield product


    def start_requests(self):
        urls = [
            {
                'href' : 'http://bvtmobile.com/ajax&do=ajax_product',
                'data' : {
                    "sort": "hight-to-low",
                    "number": "20",
                    "cate": "70032622",
                    "page": "1",
                    "txt_search": "",
                    "sub":"cat",
                    "action":"sort_product"
                },
                'max_page' : "2",
                'jump_step' : "1",
                'param_page' : 'page'
            },
            {
                'href' : 'http://bvtmobile.com/ajax&do=ajax_product',
                'data' : {
                    "sort": "hight-to-low",
                    "number": "20",
                    "cate": "552803",
                    "page": "1",
                    "txt_search": "",
                    "sub":"cat",
                    "action":"sort_product"
                },
                'max_page' : "5",
                'jump_step' : "1",
                'param_page' : 'page'
            },
            {
                'href' : 'http://bvtmobile.com/ajax&do=ajax_product',
                'data' : {
                    "sort": "hight-to-low",
                    "number": "20",
                    "cate": "552797",
                    "page": "1",
                    "txt_search": "",
                    "sub":"cat",
                    "action":"sort_product"
                },
                'max_page' : "5",
                'jump_step' : "1",
                'param_page' : 'page'
            },
            {
                'href' : 'http://bvtmobile.com/ajax&do=ajax_product',
                'data' : {
                    "sort": "hight-to-low",
                    "number": "20",
                    "cate": "70013550",
                    "page": "1",
                    "txt_search": "",
                    "sub":"cat",
                    "action":"sort_product"
                },
                'max_page' : "5",
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







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

class HungmobileSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ['hungmobile.vn']

    start_urls = [
        'http://hungmobile.vn/Services/Loaddulieu.aspx/LoadDataCat'
    ]

    rules = ()

    def parse(self, response):

        view_state = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
        view_state_generator = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()

        data = {
            "cid": "03",
            "gia": "",
            "manhinh": "0",
            "ncount": "10",
            "order": "",
            "tt": "all",
            '__VIEWSTATE' : view_state,
            '__VIEWSTATEGENERATOR' : view_state_generator
        }

        headers = {
            "X-Requested-With" : "XMLHttpRequest",
            "Content-Type": "application/json; charset=utf-8",
        }

        method = 'POST'

        formData = data

        # formData[url['param_page']] = i * url['jump_step']

        request = scrapy.FormRequest(url='http://hungmobile.vn/Services/Loaddulieu.aspx/LoadDataCat', method=method, formdata=formData, callback=self.parse_detail_content)
        yield request





    def parse_detail_content(self, response):


        link = response.url

        sel = Selector(response)

        print sel
        return

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@class="righttext col-md-7 col-sm-7 col-xs-12"]/h1/text()')
        pil.add_xpath('price', '//*[@class="price-news"]//text()')
        pil.add_value('source', 'hungmobile.vn')
        pil.add_value('source_id', 88);
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


    # def start_requests(self):
    #     urls = [
    #         {
    #             'href' : 'http://hungmobile.vn/Services/Loaddulieu.aspx/LoadDataCat',
    #             'data' : {
    #                 "cid": "03",
    #                 "gia": "",
    #                 "manhinh": "0",
    #                 "ncount": "10",
    #                 "order": "",
    #                 "tt": "all",
    #             },
    #             'max_page' : "1",
    #             'jump_step' : "10",
    #             'param_page' : 'ncount'
    #         }
    #     ]

    #     for url in urls:
    #         for i in range(1, int(url['max_page'])+1):

    #             headers = {
    #                 "X-Requested-With" : "XMLHttpRequest",
    #                 "Content-Type": "application/json; charset=utf-8"
    #             }

    #             method = 'POST'

    #             formData = url['data']

    #             # formData[url['param_page']] = i * url['jump_step']

    #             request = scrapy.FormRequest(url=url['href'], method=method, formdata=formData, callback=self.parse_item)
    #             yield request







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

class AbstractPriceSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = []
    start_urls = []
    rules = ()

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath(self.configs['product_links']);
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', self.configs['title'])
        pil.add_xpath('price', self.configs['price'])
        pil.add_value('source', self.configs['source'])
        pil.add_value('link', link)

        product = pil.load_item()

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        # arrStringShit = ['ĐTDĐ', 'Điện thoại di dộng', 'Điện thoại', 'Mua Trả Góp', 'Điện Thoại', 'Máy tính bảng', 'Máy Tính Bảng' ,'Máy tính xách tay', 'Máy tính', 'máy tính', 'Laptop', 'laptop', 'Di Động']
        # for strValue in arrStringShit:
        #     product['title'] = re.sub(strValue.decode('utf-8'), '', product['title'])

        product['title'] = product['title'].strip(' \t\n\r')
        product['title'] = product['title'].strip()
        product['name']  = product['title']

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")
        # product['brand']      = (pil.get_value(product['title'])).split(" ")[0]

        # print product
        # return

        yield(product)

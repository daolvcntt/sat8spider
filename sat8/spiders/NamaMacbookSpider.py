# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader

from time import gmtime, strftime

import json,urllib

class NamaMacbookSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = ["nama.com.vn"]
    start_urls = [
        'http://nama.com.vn/Macbook'
    ]
    rules = (

    )

    images = [];

    def parse(self, response):
        sel = Selector(response)

        product_links = sel.xpath('//*[@class="df_PrLst"]//a[1]/@href');

        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', '//*[@class="pdt_tt"]/h1//text()')
        pil.add_xpath('image', '//*[@class="pdt_asp"]//div[@class="imgs"]//img[1]/@src')
        pil.add_xpath('spec', '//*[@id="tab002"]/div/table[1]')
        # pil.add_xpath('images', '//*[@class="owl-item"]/div/a/img/@src')
        pil.add_xpath('price', '//*[@id="page"]/div[3]/div/div/div[2]/div[2]/div[3]/form/div[1]/b/font/span//text()');
        pil.add_value('brand', 'Apple'.decode('utf-8'));

        image_urls = []

        product = pil.load_item()

        product['image'] = urllib.quote(product['image'])
        product['image'] = 'http://nama.com.vn/' + product['image']

        image_urls.append(product['image'])

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        product['price']      = price
        product['link']       = response.url
        product['image_urls'] = image_urls
        product['image']      = hashlib.sha1(product['image']).hexdigest() + '.jpg'
        product['images'] = ''
        product['hash_name']  = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['brand']      = pil.get_value(product['brand'])
        product['typ']        = 'product'
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        yield(product)

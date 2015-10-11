# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader

class ProductSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = ["cellphones.com.vn"]
    start_urls = ['http://cellphones.com.vn/mobile.html',]
    rules = (
        Rule (LinkExtractor(allow=('mobile\.html\?p\=[0-9]+'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item', follow= True),
    )

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="product-image"]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', '//*[@id="product_addtocart_form"]/div[2]/div[1]/div[1]/h1//text()')
        pil.add_xpath('image', '//*[@id="image"]/@src')
        pil.add_css('spec', '.content-thongso > ul')
        product = pil.load_item()
        product['link'] = response.url
        product['image_urls'] = [pil.get_value(product['image'])]
        product['image'] = hashlib.md5(pil.get_value(product['image']).encode('utf-8')).hexdigest() + '.jpg'
        product['hash_name'] = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['brand'] = (pil.get_value(product['name'])).split(" ")[0]
        yield(product)

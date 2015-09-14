# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import Spider
from scrapy.selector import Selector
from sat8.items import ProductItem, ProductItemLoader

class ProductSpider(Spider):
    name = "product_spider"
    allowed_domains = ["cellphones.com.vn"]
    start_urls = [
    'http://cellphones.com.vn/mobile.html',
    # 'http://cellphones.com.vn/mobile.html?p=2',
    # 'http://cellphones.com.vn/mobile.html?p=3',
    # 'http://cellphones.com.vn/mobile.html?p=4',
    # 'http://cellphones.com.vn/mobile.html?p=5',
    # 'http://cellphones.com.vn/mobile.html?p=6',
    # 'http://cellphones.com.vn/mobile.html?p=7'
    ]

    def parse(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="product-image"]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_value('link', response.url)
        pil.add_xpath('name', '//*[@id="product_addtocart_form"]/div[2]/div[1]/div[1]/h1//text()')
        pil.add_xpath('price', '//*[@id="price"]//text()')
        pil.add_xpath('image', '//*[@id="image"]/@src')
        pil.add_css('spec', '.content-thongso > ul')
        yield(pil.load_item())

# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class LapNewSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['lapnew.vn']
    start_urls = [
        'http://lapnew.vn/laptop-chinhhang/laptop-dell?limit=100',
        'http://lapnew.vn/laptop-chinhhang/laptop-acer-chinhhang?limit=100',
        'http://lapnew.vn/laptop-chinhhang/laptop-Asus-chinh-hang?limit=100',
        'http://lapnew.vn/laptop-chinhhang/laptop-hp?limit=100',
        'http://lapnew.vn/laptop-chinhhang/laptop-lenovo?limit=100',
        'http://lapnew.vn/laptop-chinhhang/Laptop-Business-pro?limit=100',
        'http://lapnew.vn/laptop-chinhhang/Laptop-Workstation?limit=100',
        'http://lapnew.vn/laptop-chinhhang/Laptop-Gaming?limit=100',
        'http://lapnew.vn/laptop-chinhhang/Laptop-Multimedia?limit=100'
    ]

    rules = ()

    configs = {
        'product_links' : '//*[@class="name"]//a[1]/@href',
        'source' : 'lapnew.vn',
        'title' : '//*[@id="content"]//h2[1]/text()',
        'price' : '//*[@class="price"]//div[@class="price-new"]/text()'
    }

    def parse(self, response):
        return self.parse_item(response)
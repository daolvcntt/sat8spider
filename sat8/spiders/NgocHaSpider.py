# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class NgocHaSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['ngocha.com.vn']
    start_urls = [
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=1',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=2',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=3',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=4',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=5',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=6',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=7',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=8',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=9',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=10',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=11',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=12',
        'http://ngocha.com.vn/ajaxproductlist.html?categoryId=4&brandId=0&min=0&max=0&order=0&filter=&page=13',
    ]

    rules = (

    )

    configs = {
        'product_links' : '//*[@class="cssName"]/a/@href',
        'source' : 'wngocha.com.vn',
        'title' : '//*[@class="product-name"]//text()',
        'price' : '//*[@class="product-price"]/text()'
    }

    def parse(self, response):
        return self.parse_item(response)
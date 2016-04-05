# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MaytinhvietnamSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['www.maytinhvietnam.vn']
    start_urls = [
        'http://www.maytinhvietnam.vn/laptop-sony-vaio/c26.html',
        'http://www.maytinhvietnam.vn/laptop-hp-compaq/c27.html',
        'http://www.maytinhvietnam.vn/laptop-lenovo-ibm/c28.html',
        'http://www.maytinhvietnam.vn/laptop-dell/c29.html',
        'http://www.maytinhvietnam.vn/laptop-toshiba/c30.html',
        'http://www.maytinhvietnam.vn/acer/c31.html',
        'http://www.maytinhvietnam.vn/asus/c32.html',
        'http://www.maytinhvietnam.vn/samsung/c284.html',
        'http://www.maytinhvietnam.vn/msi-gaming/c329.html'
    ]

    rules = (
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/laptop-sony-vaio/c26.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/laptop-hp-compaq/c27.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/laptop-lenovo-ibm/c28.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/laptop-dell/c29.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/laptop-toshiba/c30.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/acer/c31.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/asus/c32.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/samsung/c284.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('http://www.maytinhvietnam.vn/msi-gaming/c329.html\?page=[0-9]+'), restrict_xpaths=('//div[@class="num_page"]')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="box-list"]//div[@class="name-pd"]/a/@href',
        'source' : 'www.maytinhvietnam.vn',
        'title' : '//*[@class="pd-infoRight"]//h1//text()',
        'price' : '//*[@class="pd-infoRight"]//div[@class="big-price"]//text()'
    }
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider
from scrapy.selector import Selector

import json,urllib

class FptShopSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ['fptshop.com.vn']
    start_urls = [
        # phone
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=0&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=14&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=33&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=57&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=79&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=105&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=127&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=148&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=172&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=197&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=222&typeView=Hot&url=http://fptshop.com.vn/dien-thoai',

        # Tablet
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=0&typeView=Hot&url=http://fptshop.com.vn/may-tinh-bang',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=21&typeView=Hot&url=http://fptshop.com.vn/may-tinh-bang',

        #Laptop
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=18&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=36&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=54&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=72&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=90&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=108&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=126&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=126&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=144&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=162&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=180&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=198&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay',
    ]

    rules = ()

    configs = {
        'product_links' : '//*[@class="p-item-bound"]/a[@class="p-link-prod"]/@href',
        'source' : 'fptshop.com.vn',
        'title' : '//*[@class="box-name"]//h1[@class="detail-name"]//text() | //*[@class="fshop-dt-proname"]/text()',
        'price' : '//*[@class="detail-price-status clearfix"]//div[@class="detail-current-price"]//text() | //*[@class="fshop-dt-price"]//text()',
        'source_id' : 39
    }


    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        sel = Selector(text=jsonresponse["content"])
        product_links = sel.xpath(self.configs['product_links']);
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)


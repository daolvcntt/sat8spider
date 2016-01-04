# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class MobileProSpider(AbstractPriceSpider):
   name = "product_link"
   allowed_domains = ['mobilepro.com.vn']
   start_urls = [
      'http://mobilepro.com.vn/iphone.html',
      'http://mobilepro.com.vn/ipad.html'
   ]
   rules = ()

   configs = {
      'product_links' : '//*[@class="hinh3"]/a[1]/@href',
      'source' : 'mobilepro.com.vn',
      'title' : '//*[@class="toprightdt"]/h2[1]//text()',
      'price' : '//*[@class="toprightdt"]/span[@class="price"]//text()'
   }


   def parse(self, response):
      return self.parse_item(response)
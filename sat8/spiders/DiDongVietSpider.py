# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DiDongVietSpider(AbstractPriceSpider):
   name = "product_link"
   allowed_domains = ['didongviet.vn']
   start_urls = [
      'http://didongviet.vn/dien-thoai.html',
      'http://didongviet.vn/may-tinh-bang.html'
   ]
   rules = ()

   configs = {
      'product_links' : '//*[@class="homeproduct"]/ul/li/a[1]/@href',
      'source' : 'didongviet.vn',
      'title' : '//*[@class="banner_content col-xs-7"]/h1//text()',
      'price' : '//*[@class="block_gia"]/h2[1]//text()'
   }


   def parse(self, response):
      return self.parse_item(response)
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class DienMayXanhSpider(AbstractPriceSpider):
   name = "product_link"
   allowed_domains = ['www.dienmayxanh.com']
   start_urls = [
      'https://www.dienmayxanh.com/dien-thoai?page=1',
      'https://www.dienmayxanh.com/dien-thoai?page=2',
      'https://www.dienmayxanh.com/dien-thoai?page=3',
      'https://www.dienmayxanh.com/dien-thoai?page=4',
      'https://www.dienmayxanh.com/dien-thoai?page=5',
      'https://www.dienmayxanh.com/dien-thoai?page=6',
      'https://www.dienmayxanh.com/dien-thoai?page=7',
      'https://www.dienmayxanh.com/may-tinh-bang?page=1',
      'https://www.dienmayxanh.com/may-tinh-bang?page=2',
      'https://www.dienmayxanh.com/laptop?page=1',
      'https://www.dienmayxanh.com/laptop?page=2'
   ]
   rules = ()

   configs = {
      'product_links': '//*[@class="listcate"]/a/@href',
      'source' : 'www.dienmayxanh.com',
      'title' : '//*[@id="ecombox"]/h1[1]/text()',
      'price' : '//*[@class="pricesell"]//text()'
   }

   def parse(self, response):
      return self.parse_item(response)
# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class TabletplazaSpider(AbstractPriceSpider):
   name = "product_link"
   allowed_domains = ['tabletplaza.vn']
   start_urls = [
      'https://tabletplaza.vn/dien-thoai-di-dong/',
   ]
   rules = (
      Rule (LinkExtractor(allow=('https://tabletplaza.vn/dien-thoai-di-dong/\&page=[0-9]+')), callback='parse_item', follow= True),
   )

   configs = {
      'product_links' : '//*[@class="lmhref"]/@href',
      'source' : 'tabletplaza.vn',
      'title' : '//*[@class="ptitle"]/h1//text()',
      'price' : '//*[@class="pprice"]/span//text()'
   }
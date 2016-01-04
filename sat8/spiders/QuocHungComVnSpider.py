# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class QuocHungComVnSpider(AbstractPriceSpider):
   name = "product_link"
   allowed_domains = ['quochung.com.vn']
   start_urls = [
      'http://quochung.com.vn/index.php?route=product/category&category_id=211',
   ]
   rules = (
      Rule (LinkExtractor(allow=('http://quochung.com.vn/index.php?route=product/category&category_id=211\&page=[0-9]+')), callback='parse_item', follow= True),
   )

   configs = {
      'product_links': '//*[@class="lmhref"]/@href',
      'source' : 'quochung.com.vn',
      'title' : '//*[@class="ptitle"]/h1//text()',
      'price' : '//*[@class="pprice"]/span//text()'
   }
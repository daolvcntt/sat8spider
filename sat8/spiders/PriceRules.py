import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime

class PriceRule:

	def rules(self):
		return [
			{
				'start_urls' : [
		        	'http://phongvu.vn/may-tinh/may-tinh-xach-tay-laptop-1670c.html',
		        	'http://phongvu.vn/dien-thoai/dien-thoai-di-dong-1192c.html',
		        	'http://phongvu.vn/san-pham-apple/iphone-1676c.html',
		        	'http://phongvu.vn/san-pham-apple/ipad-1675c.html'
			   ],
				'rules' : (
			      Rule (LinkExtractor(allow=('http://phongvu.vn/may-tinh/may-tinh-xach-tay-laptop-1670/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
			      Rule (LinkExtractor(allow=('http://phongvu.vn/dien-thoai/dien-thoai-di-dong-1192/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
			      Rule (LinkExtractor(allow=('http://phongvu.vn/san-pham-apple/iphone-1676c/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
			   ),
				'link_list' : '//*[@class="picsp"]/a[1]/@href',
				'source' : 'phongvu.vn',
			   'brand' : '//*[@class="breadcrumb"]/ul/li/a[3]/text()',
				'title' : '//*[@class="chitietsp"]/h1/text()',
				'price' : '//*[@class="giasp"]/text()'
			},
			{
				'start_urls' : ['https://www.thegioididong.com/dtdd?trang=1',],
				'rules' : (
					Rule (LinkExtractor(allow=('trang=[0-9]+')), callback='parse_item', follow= True),
				),
				'link_list' : '//*[@id="lstprods"]/li/a/@href',
				'source' : 'thegioididong.com',
			   'brand' : '//*[@class="breadcrumb"]/li[@class="brand"]/a[1]/text()',
				'title' : '//*[@id="topdetail"]/div/div/h1/text()',
				'price' : '//*[@id="topdetail"]/section/div/aside[2]/strong'
			},
		]
# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime


class TgdtSpider(CrawlSpider):
	name = "tgdd_spider"

	allowed_domains = ['thegioididong.com', ]
	start_urls = ['https://www.thegioididong.com/dtdd?trang=1',]

	rules = (
		Rule (LinkExtractor(allow=('trang=[0-9]+')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):

		sel = Selector(response)

		product_links = sel.xpath('//*[@id="lstprods"]/li/a/@href')
		for href in product_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		link = response.url
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)

		pil.add_xpath('title', '//*[@id="topdetail"]/div/div/h1/text()')
		pil.add_xpath('brand', '//*[@class="breadcrumb"]/li[@class="brand"]/a[1]/text()')
		pil.add_xpath('price', '//*[@id="topdetail"]/section/div/aside[2]/strong')
		pil.add_value('source', 'thegioididong.com')
		pil.add_value('link', link)
		pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		item = pil.load_item()

		try:
			item['price']
		except Exception, e:
			print "Price is null"
		else:
			yield(item)
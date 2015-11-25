# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from sat8.items import ProductPriceItem, ProductItemLoader
from time import gmtime, strftime


class TgdtSpider(CrawlSpider):
	name = "TgdtSpider"
	allowed_domains = ['thegioididong.com', ]
	start_urls = ['https://www.thegioididong.com/dtdd?trang=6',]

	def parse(self, response):
		sel = Selector(response)
		product_links = sel.xpath('//*[@id="lstprods"]/li/a/@href')
		for href in product_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		link = response.url
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('title', '//*[@class="rowtop"]/h1//text()')
		pil.add_xpath('brand', '//*[@class="breadcrumb"]/li[@class="brand"]/a[1]/text()')
		pil.add_xpath('price', '//*[@id="topdetail"]/section/div/aside[2]/strong')
		pil.add_xpath('name', '//*[@id="topdetail"]/div/div/h1/text()')
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
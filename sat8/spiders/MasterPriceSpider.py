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
from PriceRules import PriceRule

priceRule = PriceRule()

class MasterPriceSpider(CrawlSpider):
	name = "TgdtSpider"
	allowed_domains = []
	start_urls = []
	rules = ()

	def __init__(self,*a, **kw):

		domains = priceRule.rules()
		for domain in domains:
			self.allowed_domains.append(domain['source'])
			self.start_urls = domain['start_urls']
			self.rules = domain['rules']

	def parse(self, response):
		domains = priceRule.rules()

		for domain in domains:
			sel = Selector(response)
			product_links = sel.xpath(domain['link_list'])
			for href in product_links:
				url = response.urljoin(href.extract())
				request = scrapy.Request(url, callback = self.parse_detail_content)
				request.meta['item'] = domain

				yield request


	def parse_detail_content(self, response):
		domain = response.meta['item']
		link = response.url

		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('price', domain['price'])
		pil.add_xpath('title', domain['title'])
		pil.add_value('source', domain['source'])
		pil.add_xpath('brand', domain['brand'])
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

# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from time import gmtime, strftime
from urlparse import urlparse

class DigiPhoneSpider(CrawlSpider):
	name = "product_link"
	allowed_domains = ['digiphone.com.vn', ]
	start_urls = [
		'http://digiphone.com.vn/dien-thoai/',
		'http://digiphone.com.vn/may-tinh-bang/'
	]

	rules = (
		Rule (LinkExtractor(allow=('http://digiphone.com.vn/dien-thoai/\&p=[0-9]'), restrict_xpaths=('//div[@class="phantrang"]')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		product_links = sel.xpath('//*[@class="xemchitiet_sp"]/@href')

		for href in product_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		link = response.url
		url_parts = urlparse(link)
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('title', '//*[@class="name_product"]/text()')
		pil.add_xpath('price', '//*[@class="giagiam"]/text()')

		pil.add_value('source', url_parts.netloc)
		pil.add_value('link', link)
		pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))

		product = pil.load_item()

		product['brand'] = (pil.get_value(product['title'])).split(" ")[0]

		if 'price' not in  product:
			pil.add_value('price', 0)

		product = pil.load_item()

		yield(product)
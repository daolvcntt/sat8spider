# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from time import gmtime, strftime
from urlparse import urlparse

class HoangHaPriceSpider(CrawlSpider):
	name = "product_link"
	allowed_domains = ['hoanghamobile.com', ]
	start_urls = ['https://hoanghamobile.com/dien-thoai-di-dong-c14.html', ]
	rules = (
		Rule (LinkExtractor(allow=('dien-thoai-di-dong-c14.html\?sort=[0-9]+&p=[0-9]+'), restrict_xpaths=('//div[@class="paging"]')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		product_links = sel.xpath('//*[@class="mosaic-overlay"]/@href')

		for href in product_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		link = response.url
		url_parts = urlparse(link)
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('title', '//*[@class="product-details"]//h1[1]/strong/text()')
		pil.add_xpath('price', '//*[@class="product-price"]/p/span/text()')
		pil.add_xpath('brand', '//*[@class="breadcrumb"]/li[@class="active"]/h2/a/text()')
		pil.add_value('source', url_parts.netloc)
		pil.add_value('link', link)
		pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))

		product = pil.load_item()

		yield(pil.load_item())
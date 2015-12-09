# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from time import gmtime, strftime
from urlparse import urlparse

class ProductLinkSpider(CrawlSpider):
	name = "product_link"
	allowed_domains = ['thegioididong.com', 'cellphones.com.vn', ]
	start_urls = ['https://www.thegioididong.com/dtdd?trang=1', 'http://cellphones.com.vn/mobile.html', ]
	rules = (
		Rule (LinkExtractor(allow=('mobile\.html\?p\=[0-9]+'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('mobile\.html\?p\=[0-9]+'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		product_links = sel.xpath('//*[@class="product-image"]/@href')
		product_links.append(sel.xpath('//*[@id="lstprods"]/li/a/@href'))
		for href in product_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		link = response.url
		url_parts = urlparse(link)
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('title', '//*[@id="product_addtocart_form"]//h1/text()')
		pil.add_xpath('title', '//*[@id="topdetail"]/div/div/h1/text()')
		pil.add_xpath('price', '//*[@id="price"]')
		pil.add_xpath('price', '//*[@id="topdetail"]/section/div/aside[2]/strong')
		pil.add_xpath('brand', '//*[@class="brand"]/a[1]/text()')
		pil.add_xpath('brand', '//*[@id="product_addtocart_form"]//h1/text()')
		pil.add_value('source', url_parts.netloc)
		pil.add_value('link', link)
		pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		yield(pil.load_item())
# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from time import gmtime, strftime
from urlparse import urlparse

class PicoSpider(CrawlSpider):
	name = "product_link"
	allowed_domains = ['pico.vn', ]
	start_urls = ['http://pico.vn/may-tinh-xach-tay-nhom-58.html', ]
	rules = (
		Rule (LinkExtractor(allow=('may-tinh-xach-tay-nhom-58.html\?&\pageIndex=[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		product_links = sel.xpath('//*[@class="product-info"]/h6/a/@href')

		for href in product_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		link = response.url
		url_parts = urlparse(link)
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('title', '//*[@id="Home_ContentPlaceHolder_Product_Control_head_Title"]/text()')
		pil.add_xpath('price', '//*[@class="sidebar-box-content sidebar-padding-box product-single-info "]/span[@class="price"]/text()')
		pil.add_value('source', url_parts.netloc)
		pil.add_value('link', link)
		pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))

		product = pil.load_item()

		product['brand'] = (pil.get_value(product['title'])).split(" ")[0]

		yield(pil.load_item())
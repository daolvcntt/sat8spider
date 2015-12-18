# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class CellphoneSpider(AbstractPriceSpider):
	name = "CellphoneSpider"
	allowed_domains = ['cellphones.com.vn', ]
	start_urls = ['http://cellphones.com.vn/mobile.html', ]
	rules = (
		Rule (LinkExtractor(allow=('mobile\.html\?p\=[0-9]+'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@class="product-image"]/@href',
		'source' : 'cellphones.com.vn',
		'title' : '//*[@id="product_addtocart_form"]//h1/text()',
		'price' : '//*[@id="price"]'
	}
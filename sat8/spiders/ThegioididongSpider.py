# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider

class ThegioididongSpider(AbstractPriceSpider):
	name = "product_link"
	allowed_domains = ['thegioididong.com', ]
	start_urls = ['https://www.thegioididong.com/dtdd?trang=1',]

	rules = (
		Rule (LinkExtractor(allow=('trang=[0-9]+')), callback='parse_item', follow= True),
	)

	configs = {
		'product_links' : '//*[@id="lstprods"]/li/a/@href',
		'source' : 'thegioididong.com',
		'title' : '//*[@id="topdetail"]/div/div/h1/text()',
		'price' : '//*[@id="topdetail"]/section/div/aside[2]/strong'
	}
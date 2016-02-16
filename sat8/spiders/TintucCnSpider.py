# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from AbstractPostSpider import AbstractPostSpider

class TintucCnSpider(AbstractPostSpider):

	allowed_domains = ["tintuccongnghe.net", ]

	config_urls = [
		{
			"url" : "http://www.tintuccongnghe.net/news/may-tinh/page/[0-9]+",
			"max_page" : 1
		},
		{
			"url" : "http://www.tintuccongnghe.net/news/dien-thoai/page/[0-9]+",
			"max_page" : 1
		},
	]

	configs = {
		'links' : '//*[@class="entry-title"]/a[1]/@href',
		'title' : '//*[@class="entry-title"]//text()',
		'teaser' : '//*[@class="entry-content"]/p[1]//text()',
		'avatar' : '//*[@class="entry-content" or @class="post-content"]//img[1]/@src',
		'content' : '//*[@class="entry-content"]',
		'category' : '//*[@class="entry-category"]/span/a[2 or 1]/text()',
		'type' : 'post'
	}

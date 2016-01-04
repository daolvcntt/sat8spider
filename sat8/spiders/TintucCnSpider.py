# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from AbstractPostSpider import AbstractPostSpider

class TintucCnSpider(AbstractPostSpider):
	name = "blog_spider"
	allowed_domains = ["tintuccongnghe.net", ]
	start_urls = [
		'http://www.tintuccongnghe.net/news/may-tinh',
		'http://www.tintuccongnghe.net/news/dien-thoai'
		'http://www.tintuccongnghe.net/news/iphone-7-khong-con-dai-nhua-nua-va-se-chong-nuoc.ttcn'
	]

	rules = (
		Rule (LinkExtractor(allow=('news/may-tinh/page/[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('news/dien-thoai/page/[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
	)

	configs = {
		'links' : '//*[@class="entry-title"]/a[1]/@href',
		'title' : '//*[@class="entry-title"]//text()',
		'teaser' : '//*[@class="entry-content"]/p[1]//text()',
		'avatar' : '//*[@class="entry-content" or @class="post-content"]//img[1]/@src',
		'content' : '//*[@class="entry-content"]',
		'category' : '//*[@class="entry-category"]/span/a[2 or 1]/text()',
		'type' : 'post'
	}

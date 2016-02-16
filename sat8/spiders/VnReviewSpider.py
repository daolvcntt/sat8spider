# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider

class VnReviewSpider(AbstractPostSpider):
   	allowed_domains = ["vnreview.vn"]

	config_urls = [
		{
			"url" : "http://vnreview.vn/danh-gia-di-dong#cur=[0-9]+",
			"max_page" : 1
		}
	]

	configs = {
		'links' : '//*[@class="assettile"]/h1/a[1]/@href',
		'title' : '//*[@class="title-content"]/h1[1]//text()',
		'teaser' : '//*[@class="journal-content-article"]/p[1]//text()',
		'avatar' : '//*[@class="journal-content-article"]/p/img[1]/@src',
		'content' : '//*[@class="journal-content-article"]',
		'category' : '//*[@class="last-node"]/span/a/font//text()',
		'type' : 'post'
	}
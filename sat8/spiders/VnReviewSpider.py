# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


from AbstractPostSpider import AbstractPostSpider

class VnReviewSpider(AbstractPostSpider):
   	allowed_domains = ["vnreview.vn"]

	start_urls = [
		'http://vnreview.vn/danh-gia-di-dong',
		'http://vnreview.vn/danh-gia-di-dong#cur=2',
		'http://vnreview.vn/danh-gia-di-dong#cur=3',
		'http://vnreview.vn/danh-gia-di-dong#cur=4',
		'http://vnreview.vn/danh-gia-di-dong#cur=5',
		'http://vnreview.vn/danh-gia-di-dong#cur=6',
		'http://vnreview.vn/danh-gia-di-dong#cur=7',
		'http://vnreview.vn/danh-gia-di-dong#cur=8',
		'http://vnreview.vn/danh-gia-di-dong#cur=9',
		'http://vnreview.vn/danh-gia-di-dong#cur=10'
	]

	rules = ()

	configs = {
		'links' : '//*[@class="assettile"]/h1/a[1]/@href',
		'title' : '//*[@class="title-content"]/h1[1]//text()',
		'teaser' : '//*[@class="journal-content-article"]/p[1]//text()',
		'avatar' : '//*[@class="journal-content-article"]/p/img[1]/@src',
		'content' : '//*[@class="journal-content-article"]',
		'category' : '//*[@class="last-node"]/span/a/font//text()',
		'type' : 'post'
	}

	def parse(self, response):
		return self.parse_item(response)
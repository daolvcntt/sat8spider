# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sat8.items import BlogItem, PostItemLoader
from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

class TechzReviewSpider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["www.techz.vn"]
	start_urls = [
		'http://www.techz.vn/C/dien-thoai-rv',
		'http://www.techz.vn/C/danh-gia-may-tinh-bang',
		'http://www.techz.vn/C/danh-gia'
	]

	rules = (
		Rule (LinkExtractor(allow=('page/[0-9]+')),  callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('page/[0-9]+')),  callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('page/[0-9]+')),  callback='parse_item', follow= True),
	)

	def parse_item(self, response):

		sel = Selector(response)

		blog_links = sel.xpath('//*[@id="reviews-list"]/ul[1]/li/a/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@id="admwrapper"]/header/h1//text()')
		il.add_xpath('category', '//*[@id="admwrapper"]/header/div[4]/p/span/a[2]/strong//text()');
		il.add_xpath('teaser', '//*[@id="primary-content"]/div[1]/p//text()')
		il.add_css('avatar', '.news-relation-top-detail p img[src]')
		il.add_xpath('content', '//*[@class="news-relation-top-detail"]')
		il.add_value('category_id', 1)
		il.add_value('product_id', 0)
		il.add_value('user_id', 1)
		il.add_value('post_type', 'review')
		il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
		il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
		item = il.load_item()

		if 'content' not in item:
			il.add_xpath('content', '//*[@id="primary-content"]')

		if 'category' not in item:
			il.add_xpath('category', '//*[@id="admwrapper"]/header/div[4]/div/span/h2/a/strong//text()')

		item = il.load_item()

		item['typ'] = 'blog'

		if 'avatar' in item:
			item['image_urls'] = [il.get_value(item['avatar'])]
			item['avatar'] = hashlib.sha1(il.get_value(item['avatar'])).hexdigest() + '.jpg'
		else:
			item['avatar'] = '';

		yield(item)



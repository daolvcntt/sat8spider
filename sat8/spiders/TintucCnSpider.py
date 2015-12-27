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

class TintucCnSpider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["tintuccongnghe.net", ]
	start_urls = ['http://www.tintuccongnghe.net/news/may-tinh']

	rules = (
		Rule (LinkExtractor(allow=('news/may-tinh/page/[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		# if response.url == 'genk.vn':
		blog_links = sel.xpath('//*[@class="entry-title"]/a[1]/@href')

		# else:
			# blog_links = sel.xpath('//*[@id="admWrapsite"]//h2/a/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@class="entry-title"]//text()')
		il.add_xpath('teaser', '//*[@class="entry-content"]/p[1]//text()')
		il.add_xpath('avatar', '//*[@class="entry-content" or @class="post-content"]//img[1]/@src')
		il.add_xpath('content', '//*[@class="entry-content"]')
		il.add_value('category_id', 1)
		il.add_value('product_id', 0)
		il.add_value('user_id', 1)
		il.add_xpath('category', '//*[@class="entry-category"]/span/a[2 or 1]/text()');
		il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
		il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
		il.add_value('post_type', 'post')

		item = il.load_item()
		item['typ'] = 'blog'

		if 'avatar' in item:
			item['image_urls'] = [il.get_value(item['avatar'])]
			item['avatar'] = hashlib.sha1(il.get_value(item['avatar']).encode('utf-8')).hexdigest() + '.jpg'

		yield(item)

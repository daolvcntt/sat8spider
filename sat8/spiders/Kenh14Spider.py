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


class Kenh14Spider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["kenh14.vn"]
	start_urls = [
		'http://kenh14.vn/2-tek/mobile.chn'
	]

	rules = (
		Rule (LinkExtractor(allow=('2-tek/mobile/trang-[0-9]+.chn')),  callback='parse_item', follow= True),
	)


	def parse_item(self, response):

		sel = Selector(response)

		blog_links = sel.xpath('//*[@class="kcnwn-title"]/a/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@id="admWrapsite"]/div[4]/div[3]/div/div[3]/div[1]/div/div[1]/h1//text()')
		il.add_xpath('category', 'mobile');
		il.add_xpath('teaser', '//*[@id="admWrapsite"]/div[4]/div[3]/div/div[3]/div[1]/div/div[1]/div[5]//text()')
		il.add_xpath('avatar', '//*[@class="knd-content"]//img/@src')
		il.add_xpath('content', '//*[@class="knd-content"]')
		il.add_value('category_id', 1)
		il.add_value('product_id', 0)
		il.add_value('user_id', 1)
		il.add_value('post_type', 'post')
		il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
		il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
		item = il.load_item()

		item['typ'] = 'blog'
		item['image_urls'] = [il.get_value(item['avatar'])]
		item['avatar'] = hashlib.sha1(il.get_value(item['avatar'])).hexdigest() + '.jpg'

		yield(item)

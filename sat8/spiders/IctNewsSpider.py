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

class IctNewsSpider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["ictnews.vn"]
	start_urls = [ 'http://ictnews.vn/the-gioi-so/di-dong', 'http://ictnews.vn/the-gioi-so/may-tinh']

	rules = (
		Rule (LinkExtractor(allow=('http://ictnews.vn/the-gioi-so/di-dong/trang-[0-9]+')),  callback='parse_item', follow= True),
		Rule (LinkExtractor(allow=('http://ictnews.vn/the-gioi-so/may-tinh/trang-[0-9]+')),  callback='parse_item', follow= True),
	)

	def parse_item(self, response):

		sel = Selector(response)

		blog_links = sel.xpath('//*[@id="listArticles"]/div/a[1]/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@class="article-brand"]/h1[1]//text()')
		il.add_xpath('category', '//*[@class="article-brand"]//a[@class="channelname"]/text()');
		il.add_xpath('teaser', '//*[@class="article-brand"]//h2[@class="pSapo"]//text()')
		il.add_xpath('avatar', '//*[@class="content-detail"]//img[1]/@src')
		il.add_xpath('content', '//*[@class="content-detail"]')
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

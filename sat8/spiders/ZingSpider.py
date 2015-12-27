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

class ZingSpider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["news.zing.vn", ]
	start_urls = ['http://news.zing.vn/cong-nghe/dien-thoai.html']

	rules = (
		Rule (LinkExtractor(allow=('cong-nghe/dien-thoai/trang[0-9]+.html')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		# if response.url == 'genk.vn':
		blog_links = sel.xpath('//*[@class="cate_content"]/article/header/h1/a/@href')

		# else:
			# blog_links = sel.xpath('//*[@id="admWrapsite"]//h2/a/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@class="the-article-header"]/h1//text()')
		il.add_xpath('teaser', '//*[@class="the-article-summary"]//text()')
		# il.add_xpath('teaser', '//*[@class="short_intro txt_666"]/text()')
		il.add_xpath('avatar', '//*[@class="the-article-body"]//img[1]/@src')
		# il.add_xpath('avatar', '//*[@id="article_content"]/div/div[1]/img/@src')
		il.add_xpath('content', '//*[@class="the-article-body"]')
		il.add_value('category_id', 1)
		il.add_value('product_id', 0)
		il.add_value('user_id', 1)
		il.add_value('category', 'Dien thoai');
		il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		il.add_value('post_type', 'post')

		item = il.load_item()
		item['typ'] = 'blog'

		if 'avatar' in item:
			item['image_urls'] = [il.get_value(item['avatar'])]
			item['avatar'] = hashlib.sha1(il.get_value(item['avatar'])).hexdigest() + '.jpg'

		yield(item)

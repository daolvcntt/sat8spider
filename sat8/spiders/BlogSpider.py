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

class BlogSpider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["sohoa.vnexpress.net", ]
	start_urls = ['http://sohoa.vnexpress.net/tin-tuc/san-pham']

	rules = (
		Rule (LinkExtractor(allow=('page/[0-9]+\.html'), restrict_xpaths=('//div[@id="pagination"]')), callback='parse_item', follow= True),
	)

	def parse_item(self, response):
		sel = Selector(response)
		# if response.url == 'genk.vn':
		blog_links = sel.xpath('//*[@id="news_home"]/li/div/div[1]/a/@href')

		# else:
			# blog_links = sel.xpath('//*[@id="admWrapsite"]//h2/a/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@id="box_details_news"]/div/div[1]/div[1]/div[3]/h1//text()')
		il.add_xpath('teaser', '//*[@id="box_details_news"]/div/div[1]/div[1]/div[4]//text()')
		# il.add_xpath('teaser', '//*[@class="short_intro txt_666"]/text()')
		il.add_xpath('avatar', '//*[@id="left_calculator"]/div[1]/table/tbody/tr[1]/td/img/@src')
		# il.add_xpath('avatar', '//*[@id="article_content"]/div/div[1]/img/@src')
		il.add_xpath('content', '//*[@class="fck_detail width_common"]')
		il.add_value('category_id', 1)
		il.add_value('product_id', 0)
		il.add_value('user_id', 1)
		il.add_xpath('category', '//*[@id="sohoa_menu_sub"]//a[@class="active"]/text()');
		il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		il.add_value('post_type', 'review')

		item = il.load_item()
		item['typ'] = 'blog'

		if 'avatar' in item:
			item['image_urls'] = [il.get_value(item['avatar'])]
			item['avatar'] = hashlib.md5(il.get_value(item['avatar']).encode('utf-8')).hexdigest() + '.jpg'

		yield(item)

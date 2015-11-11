# -*- coding: utf-8 -*-
import scrapy
import hashlib
import re
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sat8.items import BlogItem, PostItemLoader
from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse


class TgddPostSpider(CrawlSpider):
	name = "blog_spider"
	allowed_domains = ["thegioididong.com"]
	start_urls = [
		'https://www.thegioididong.com/tin-tuc?page=1',
	]

	rules = (
      Rule (LinkExtractor(allow=('tin-tuc\?page\=[0-9]+'), restrict_xpaths=('//div[@class="pagination"]')), callback='parse_item', follow= True),
  	)

	def test(self, response):

		print "CHinh no"

	def parse_item(self, response):

		sel = Selector(response)

		blog_links = sel.xpath('//*[@class="homenews"]/li/a/@href')

		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		il = PostItemLoader(item = BlogItem(), response=response)
		il.add_value('link', response.url)
		il.add_xpath('title', '//*[@class="article "]/h1[1]//text()')
		il.add_xpath('category', '//*[@class="actnavi"]//text()');
		il.add_xpath('teaser', '//*[@class="article "]/h1[1]//text()')
		il.add_xpath('avatar', '//*[@class="cur pimg"]//img/@src')
		il.add_xpath('content', '//article')
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

		item['content'] = re.sub('<h1>.+</h1>', '', item['content']);

		yield(item)

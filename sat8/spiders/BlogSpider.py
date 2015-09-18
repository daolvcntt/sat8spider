# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import Spider
from scrapy.selector import Selector
from sat8.items import BlogItem
from time import gmtime, strftime

class BlogSpider(Spider):
	name = "blog_spider"
	allowed_domains = ["sohoa.vnexpress.net"]
	start_urls = [
		'http://timkiem.vnexpress.net/?q=iphone+5c',
		'http://timkiem.vnexpress.net/?q=iphone+5c&page=2',
		'http://timkiem.vnexpress.net/?q=iphone+5c&page=3',
		'http://timkiem.vnexpress.net/?q=iphone+5c&page=4',
	]

	# def __init__(self):
		# self.conn = settings['MYSQL_CONN']
		# self.cursor = self.conn.cursor()
		# query = "SELECT * FROM roles"
		# self.cursor.execute(query)
		# results = self.cursor.fetchall()
		# print results
		# self.start_urls =  (
			# 'http://timkiem.vnexpress.net/sohoa?q=iphone+6',
		# )

	def parse(self, response):
		sel = Selector(response)
		blog_links = sel.xpath('//*[@id="news_home"]/li/div/div[1]/a/@href')
		for href in blog_links:
			url = response.urljoin(href.extract());
			yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		sel = Selector(response)
		blog = BlogItem()
		blog['link'] = response.url
		blog['title'] = sel.xpath('//*[@id="box_details_news"]/div/div[1]/div[1]/div[3]/h1//text()').extract()[0]
		blog['teaser'] = sel.xpath('//*[@id="box_details_news"]/div/div[1]/div[1]/div[4]//text()').extract()[0]
		blog['avatar'] = sel.xpath('//*[@id="left_calculator"]/div[1]/table/tbody/tr[1]/td/img/@src').extract()[0]
		blog['image_urls'] = [blog['avatar']]
		blog['content'] = sel.xpath('//*[@id="left_calculator"]/div[1]').extract()[0]
		blog['category_id'] = 1
		blog['product_id'] = 29
		blog['user_id'] = 1
		blog['published_time'] = " ".join(sel.xpath('//*[@id="box_details_news"]/div/div[1]/div[1]/div[1]/div[1]//text()').extract()).strip()
		# blog['tags'] = sel.xpath('//*[@id="box_details_news"]/div/div[3]/a//text()').extract()
		blog['created_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		blog['updated_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		yield(blog)

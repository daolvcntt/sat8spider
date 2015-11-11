# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import Spider
from scrapy.selector import Selector
from sat8.items import VideoItem
from time import gmtime, strftime

class VideoSpider(Spider):
	name = "video_spider"
	allowed_domains = ["youtube.com"]
	start_urls = [
		'https://www.youtube.com/results?search_query=danh+gia+iphone+6',
	]

	def parse(self, response):
		sel = Selector(response)
		video_links = sel.xpath('//*[@id="item-section-167213"]/li/div/div/div[2]/h3/a/@href')
		print video_links
		# for href in video_links:
		# 	url = response.urljoin(href.extract());
		# 	yield scrapy.Request(url, callback = self.parse_detail_content)

	def parse_detail_content(self, response):
		sel = Selector(response)
		vid = VideoItem()
		vid['link'] = response.url
		vid['title'] = sel.xpath('//*[@id="eow-title"]//text()').extract()[0]
		vid['description'] = sel.xpath('/html/head/meta[2]/@content').extract()[0]
		vid['embed'] = sel.xpath('//*[@id="watch7-content"]/link[3]/@src').extract()[0]
		vid['thumbnail'] = sel.xpath('//*[@id="watch7-content"]/link[2]/@href').extract()[0]
		vid['author'] = sel.xpath('//*[@id="watch7-user-header"]/div/a//text()').extract()[0]
		vid['category_id'] = 1
		vid['product_id'] = 29
		vid['user_id'] = 1
		print vid
		# vid['published_time'] = " ".join(sel.xpath('//*[@id="box_details_news"]/div/div[1]/div[1]/div[1]/div[1]//text()').extract()).strip()
		# blog['tags'] = sel.xpath('//*[@id="box_details_news"]/div/div[3]/a//text()').extract()
		# blog['created_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		# blog['updated_at'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		# yield(blog)

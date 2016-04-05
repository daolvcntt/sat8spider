import scrapy
import pymysql.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

import logging
import time

import settings

class MyImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		if 'image_urls' in item:
			for image_url in item['image_urls']:
				yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = [x['path'].replace("full/", "") for ok, x in results if ok]

		if not image_paths:
			raise DropItem("Item contains no images")

		item['image_paths'] = image_paths;

		return item

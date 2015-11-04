import scrapy
import pymysql.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

import logging
import time

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

		if item['typ'] == 'product' :

			connection = pymysql.connect(host='localhost',user='root',password='stingdau2015',db='fp_searchon',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
			logging.info("Shit connect")
			try:
				with connection.cursor() as cursor:
					# Create a new record
					created_at = time.strftime("%Y-%m-%d %H:%M:%S")
					updated_at = time.strftime("%Y-%m-%d %H:%M:%S")

					sql = "INSERT INTO product_images (product_title, image, created_at, updated_at) VALUES (%s, %s, %s, %s)"
					cursor.execute(sql, (item['name'].encode('utf-8'), image_paths, created_at, updated_at))

				# connection is not autocommit by default. So you must commit to save
				# your changes.
				connection.commit()

			finally:
				logging.info("Shit connect")

				connection.close()


		return item

# -*- coding: utf-8 -*-
import logging
import cgi;
import re;
from scrapy.conf import settings
from elasticsearch import Elasticsearch
from sat8.Databases.DB import DB
from sat8.Elasticsearch.ES import ES
from sat8.Posts.PostES import PostES
from sat8.Products.ProductES import ProductES
from sat8.Products.ProductPriceES import ProductPriceES

from time import strftime

from sat8.Helpers.Functions import *

# Class kết nối mysql
class MySQLStorePipeline(object):
	def __init__(self):
		self.conn = settings['MYSQL_CONN']
		self.cursor = self.conn.cursor()
		self.db = DB()
		self.es = ES()
		self.post = PostES()
		self.product = ProductES()
		self.price = ProductPriceES()

	def process_item(self, item, spider):

		if spider.name == 'blog_spider' or spider.name == 'GenkSpider':
			query = "SELECT * FROM posts WHERE link = %s OR title = %s"
			self.cursor.execute(query, (item['link'], item['title']))
			result = self.cursor.fetchone()

			postId = 0

			if result:
				postId = result['id']
				sql = "UPDATE posts SET avatar = %s, content = %s, static_time = %s WHERE id = %s"
				self.cursor.execute(sql, (item['avatar'], item['content'], timestamp(), postId))
				self.conn.commit()

				logging.info("Item already stored in db: %s" % item['link'])
			else:
				content = item['content'];
				sql = "INSERT INTO posts (title, content, type, category, teaser, avatar, link, category_id, product_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (item['title'].encode('utf-8'), content, item['post_type'] ,item['category'].encode('utf-8') ,item['teaser'].encode('utf-8'), item['avatar'], item['link'], item['category_id'], item['product_id'], item['user_id'], item['created_at'], item['updated_at']))
				self.conn.commit()

				# Insert to elasticsearch
				postId = self.cursor.lastrowid
				logging.info("Item stored in db: %s" % item['link'])

			item["id"] = postId
			self.post.insertOrUpdate(postId, item.toJson())


		elif spider.name == 'product_spider':
			query = "SELECT * FROM products WHERE hash_name = %s"
			self.cursor.execute(query, (item['hash_name']))
			result = self.cursor.fetchone()

			productId = 0;

			if item['price'] > 0 :

				if result:
					productId = result['id']

					sql = "UPDATE products SET price = %s, updated_at = %s WHERE id = %s"
					self.cursor.execute(sql, (item['price'], item['updated_at'], productId))
					self.conn.commit()

					logging.info("Item already stored in db: %s" % item['name'])
				else:
					sql = "INSERT INTO products (name, price, hash_name, brand_id, image, images, is_smartphone, is_laptop, is_tablet, is_camera, link, spec, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					self.cursor.execute(sql, (item['name'].encode('utf-8'), item['price'], item['hash_name'].encode('utf-8'), item['brand_id'], item['image'].encode('utf-8'), item['images'] , item['is_mobile'], item['is_laptop'], item['is_tablet'], item['is_camera'] ,item['link'], item['spec'], item['created_at'], item['updated_at']))
					self.conn.commit()
					logging.info("Item stored in db: %s" % item['link'])

					productId = self.cursor.lastrowid

				item["id"] = productId
				self.product.insertOrUpdate(productId, item.toJson())

		elif spider.name == 'product_link':
			if item['price'] > 0:
				query = "SELECT * FROM product_prices WHERE link = %s"
				self.cursor.execute(query, (item['link'].encode('utf-8')))
				result = self.cursor.fetchone()

				priceId = 0

				if result:
					updateSql = "UPDATE product_prices SET price = %s, source_id = %s, is_phone=%s, is_tablet=%s, is_laptop=%s, updated_at = %s, crawled_at = %s WHERE link = %s"

					self.cursor.execute(updateSql, (item['price'], item['source_id'], item['is_phone'], item['is_tablet'], item['is_laptop'], item['updated_at'], item['crawled_at'], item['link'].encode('utf-8')))
					self.conn.commit()
					logging.info("Item already updated in db: %s" % item['link'])

					priceId = result['id']

				else:
					sql = "INSERT INTO product_prices (title, price, source, source_id, brand_id, is_phone, is_tablet, is_laptop, link, created_at, updated_at, crawled_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					self.cursor.execute(sql, (item['title'].encode('utf-8'), item['price'], item['source'].encode('utf-8'), item['source_id'], item['brand_id'], item['is_phone'], item['is_tablet'], item['is_laptop'], item['link'].encode('utf-8'), item['created_at'], item['updated_at'], item['crawled_at']))
					self.conn.commit()
					logging.info("Item stored in db: %s" % item['link'])

					priceId = self.cursor.lastrowid

				item["id"] = priceId

				# print item.toJson()


				# Insert to elasticsearch
				self.price.insertOrUpdate(priceId, item.toJson())

				# Update price history
				self.savePriceHistories(item)

		return item

	def savePriceHistories(self, item):
		day = strftime("%Y-%m-%d")
		sql = "INSERT INTO price_histories (price_id, price, day) VALUES (%s, %s, %s)"
		self.cursor.execute(sql, (item['id'], item['price'], day))
		self.conn.commit()


# -*- coding: utf-8 -*-
import logging
from scrapy.conf import settings

# Class kết nối mysql
class MySQLStorePipeline(object):
	def __init__(self):
		self.conn = settings['MYSQL_CONN']
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):

		if spider.name == 'blog_spider' or spider.name == 'GenkSpider':
			query = "SELECT * FROM posts WHERE link = %s"
			self.cursor.execute(query, (item['link']))
			result = self.cursor.fetchone()

			if result:
				logging.info("Item already stored in db: %s" % item['link'])
			else:
				sql = "INSERT INTO posts (title, content, type, category, teaser, avatar, link, category_id, product_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (item['title'].encode('utf-8'), item['content'].encode('utf-8'), item['post_type'] ,item['category'].encode('utf-8') ,item['teaser'].encode('utf-8'), item['avatar'], item['link'], item['category_id'], item['product_id'], item['user_id'], item['created_at'], item['updated_at']))
				self.conn.commit()
				logging.info("Item stored in db: %s" % item['link'])

		elif spider.name == 'product_spider':
			query = "SELECT * FROM products WHERE hash_name = %s"
			self.cursor.execute(query, (item['hash_name']))
			result = self.cursor.fetchone()

			if result:
				logging.info("Item already stored in db: %s" % item['name'])
			else:
				sql = "INSERT INTO products (name, price, hash_name, brand, image, images, link, spec, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (item['name'].encode('utf-8'), item['price'], item['hash_name'].encode('utf-8'), item['brand'].encode('utf-8'), item['image'].encode('utf-8'), item['images'] ,item['link'], item['spec'], item['created_at'], item['updated_at']))
				self.conn.commit()
				logging.info("Item stored in db: %s" % item['link'])

		else:
			if item['price'] > 0:
				query = "SELECT * FROM product_prices WHERE link = %s"
				self.cursor.execute(query, (item['link'].encode('utf-8')))
				result = self.cursor.fetchone()
				if result:
					updateSql = "UPDATE product_prices SET price = %s, updated_at = %s WHERE link = %s"
					self.cursor.execute(updateSql, (item['price'], item['updated_at'], item['link'].encode('utf-8')))
					self.conn.commit()
					logging.info("Item already updated in db: %s" % item['link'])
				else:
					sql = "INSERT INTO product_prices (title, brand, price, source, link, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
					self.cursor.execute(sql, (item['title'].encode('utf-8'), item['brand'], item['price'], item['source'].encode('utf-8'), item['link'].encode('utf-8'), item['created_at'], item['updated_at']))
					self.conn.commit()
					logging.info("Item stored in db: %s" % item['link'])

		return item


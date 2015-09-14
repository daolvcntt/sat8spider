# -*- coding: utf-8 -*-
import logging
from scrapy.conf import settings

# Class kết nối mysql
class MySQLStorePipeline(object):
	def __init__(self):
		self.conn = settings['MYSQL_CONN']
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if spider.name == 'blog_spider':
			query = "SELECT * FROM posts WHERE link = %s"
			self.cursor.execute(query, (item['link']))
			result = self.cursor.fetchone()

			if result:
				logging.debug("Item already stored in db: %s" % item['link'])
			else:
				sql = "INSERT INTO posts (title, content, teaser, avatar, link, category_id, product_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (item['title'].encode('utf-8'), item['content'].encode('utf-8'), item['teaser'].encode('utf-8'), item['avatar'], item['link'], item['category_id'], item['product_id'], item['user_id'], item['created_at'], item['updated_at']))
				self.conn.commit()
				logging.debug("Item stored in db: %s" % item['link'])

		elif spider.name == 'product_spider':
			query = "SELECT * FROM products WHERE link = %s"
			self.cursor.execute(query, (item['link']))
			result = self.cursor.fetchone()

			if result:
				logging.debug("Item already stored in db: %s" % item['link'])
			else:
				sql = "INSERT INTO products (name, price, image, link, spec) VALUES (%s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (item['name'].encode('utf-8'), item['price'], item['image'], item['link'], item['spec']))
				self.conn.commit()
				logging.debug("Item stored in db: %s" % item['link'])

		else:
			query = "SELECT * FROM product_prices WHERE product_id = %s AND source = %s"
			self.cursor.execute(query, (item['product_id'], item['source'].encode('utf-8')))
			result = self.cursor.fetchone()
			if item['price'] > 0:
				if result:
					updateSql = "UPDATE product_prices SET price = %s, updated_at = %s WHERE product_id = %s AND source = %s"
					self.cursor.execute(updateSql, (item['price'], item['updated_at'], item['product_id'], item['source'].encode('utf-8')))
					self.conn.commit()
					logging.debug("Item already updated in db: %s" % item['product_id'])
				else:
					sql = "INSERT INTO product_prices (product_id, price, source, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
					self.cursor.execute(sql, (item['product_id'], item['price'], item['source'].encode('utf-8'), item['created_at'], item['updated_at']))
					self.conn.commit()
					logging.debug("Item stored in db: %s" % item['product_id'])

		return item
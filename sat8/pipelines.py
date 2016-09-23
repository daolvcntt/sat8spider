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

from sat8.Products.DbProduct import DbProduct

from time import strftime
from random import randint

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
		self.dbProduct = DbProduct()

	def process_item(self, item, spider):

		if spider.name == 'blog_spider' or spider.name == 'GenkSpider':
			# Check link exits
			query = "SELECT hash_link FROM post_hash_links WHERE hash_link = %s"
			self.cursor.execute(query, (md5(item['link'])))
			result = self.cursor.fetchone()

			# Update craw links
			sql = "REPLACE INTO post_hash_links(hash_link) VALUES(%s)"
			self.cursor.execute(sql, (md5(item['link'])))
			self.conn.commit()

			# Select post
			query = "SELECT id,title FROM posts WHERE link = %s"
			self.cursor.execute(query, (item['link']))
			result = self.cursor.fetchone()

			postId = 0
			if result:
				postId = result['id']

				sql = "UPDATE posts SET avatar = %s, content = %s, static_time = %s WHERE id = %s"
				self.cursor.execute(sql, (item['avatar'], item['content'], str(timestamp()), postId))
				self.conn.commit()

				logging.info("Item already stored in db: %s" % item['link'])
			else:
				# Neu co avatar thi moi insert
				if item['avatar'] != '':
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

					# sql = "UPDATE products SET price = %s, min_price = %s, image = %s, images = %s, updated_at = %s WHERE id = %s"
					# self.cursor.execute(sql, (item['price'], item['min_price'], item['image'], item['images'], item['updated_at'], productId))

					sql = "UPDATE products SET updated_at = %s WHERE id = %s"
					self.cursor.execute(sql, (item['updated_at'], productId))
					self.conn.commit()

					logging.info("Item already stored in db: %s" % item['name'])
				else:
					sql = "INSERT INTO products (category_id, type, source_id, name, price, min_price, hash_name, brand_id, image, images, is_smartphone, is_laptop, is_tablet, is_camera, link, spec, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
					self.cursor.execute(sql, (item['category_id'], item['type'], item['source_id'], item['name'].encode('utf-8'), item['price'], item['min_price'] ,item['hash_name'].encode('utf-8'), item['brand_id'], item['image'].encode('utf-8'), item['images'] , item['is_mobile'], item['is_laptop'], item['is_tablet'], item['is_camera'] ,item['link'], item['spec'], item['created_at'], item['updated_at']))
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
		# Lấy gian hàng Vật Giá
		elif spider.name == "merchant_spider":
			merchant  = item['merchant']
			priceItem = item['price_item']
			product   = item['product']

			merchantId = self.saveMerchant(merchant)
			merchant['id'] = merchantId

			priceItem['source_id'] = merchantId
			self.savePriceItem(priceItem)

			self.saveMerchantRate(merchant)


		elif spider.name == "tinhte_spider":
			post    = item['post']
			comments = item['comments']

			query = "SELECT id,title FROM posts WHERE link = %s"
			self.cursor.execute(query, (post['link']))
			result = self.cursor.fetchone()

			postId = 0
			insertComment = 0

			# Nếu có rồi thì bỏ qua
			if result:
				postId = result['id']
				post = result
				logging.info("Item already stored in db: %s" % post['title'])

				query = "SELECT count(*) as count FROM post_comments WHERE post_id = %s"
				self.cursor.execute(query, (postId))
				result = self.cursor.fetchone()

				# Nếu không có bình luận thì mới thêm bình luận
				if result["count"] == 0:
					insertComment = 1

			else:
				content = post['content'];
				sql = "INSERT INTO posts (title, content, type, is_tinhte, tinhte_category_link, category, teaser, avatar, link, category_id, product_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (post['title'].encode('utf-8'), content, post['post_type'] , post['is_tinhte'], post['tinhte_category_link'] ,post['category'].encode('utf-8') ,post['teaser'].encode('utf-8'), post['avatar'], post['link'], post['category_id'], post['product_id'], post['user_id'], post['created_at'], post['updated_at']))
				self.conn.commit()

				postId = self.cursor.lastrowid

				insertComment = 1

			if insertComment == 1:
				# Insert cau tra loi
				for comment in comments:
					sql = "INSERT INTO post_comments(post_id, user_name, user_avatar, comment, is_crawl, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s)"
					self.cursor.execute(sql, (postId, comment["user"], comment['avatar_hash'], comment['comment'], 1, post['created_at'], post['updated_at']))
					self.conn.commit()

			self.post.insertOrUpdate(postId, {
			    "id" : postId,
				"title" : post['title'],
				"teaser" : post['teaser'],
				"category" : post['category'],
				"content" : post['content']
			})

		return item

	def savePriceHistories(self, item):
		day = strftime("%Y-%m-%d")
		sql = "INSERT INTO price_histories (price_id, price, day) VALUES (%s, %s, %s)"
		self.cursor.execute(sql, (item['id'], item['price'], day))
		self.conn.commit()


	def saveMerchant(self, merchant):
		query = "SELECT id,name FROM sites WHERE name = %s"
		self.cursor.execute(query, (merchant['name']))
		result = self.cursor.fetchone()
		created_at = strftime("%Y-%m-%d %H:%M:%S")
		updated_at  = strftime("%Y-%m-%d %H:%M:%S")

		if result == None:
			sql = "INSERT INTO sites(name, alias, logo, is_craw, created_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s)"
			self.cursor.execute(sql, (merchant['name'], merchant['alias'], merchant['logo_hash'], merchant['is_craw'] ,created_at, updated_at))
			self.conn.commit()

			merchantId = self.cursor.lastrowid

			return merchantId;
		else:
			return result['id']


	def savePriceItem(self, item):
		created_at = strftime("%Y-%m-%d %H:%M:%S")
		updated_at  = strftime("%Y-%m-%d %H:%M:%S")
		crawled_at = updated_at
		item['created_at'] = created_at
		item['updated_at'] = updated_at

		if item['price'] > 0:
			query = "SELECT * FROM product_prices WHERE link = %s"
			self.cursor.execute(query, (item['link'].encode('utf-8')))
			result = self.cursor.fetchone()

			priceId = 0

			if result:
				updateSql = "UPDATE product_prices SET price = %s, source_id = %s, updated_at = %s, crawled_at = %s WHERE link = %s"

				self.cursor.execute(updateSql, (item['price'], item['source_id'], item['updated_at'], crawled_at, item['link'].encode('utf-8')))
				self.conn.commit()
				logging.info("Item already updated in db: %s" % item['link'])

				priceId = result['id']

			else:
				sql = "INSERT INTO product_prices (title, price, source_id, link, created_at, updated_at, crawled_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
				self.cursor.execute(sql, (item['title'].encode('utf-8'), item['price'], item['source_id'], item['link'],  item['created_at'], item['updated_at'], crawled_at))
				self.conn.commit()
				logging.info("Item stored in db: %s" % item['link'])

				priceId = self.cursor.lastrowid

			item["id"] = priceId

			# print item.toJson()


			# Insert to elasticsearch
			item.pop('created_at', None)
			item.pop('updated_at', None)
			item.pop('crawled_at', None)

			self.price.insertOrUpdate(priceId, item)

			# Update price history
			self.savePriceHistories(item)

			return priceId

		return 0


	# Fake dữ liệu đánh giá với các gian hàng VG
	def saveMerchantRate(self, merchant):
		sql = "DELETE FROM merchant_rates WHERE merchant_id = %s AND user_id = %s";
		self.cursor.execute(sql, (merchant['id'], 0))

		# 5 sao
		if merchant['rating_5_count'] > 0:
			sql ="INSERT INTO merchant_rates(merchant_id, user_id, value) VALUES "
			for i in range(0, int(merchant['rating_5_count'])):
				sql += "('"+ str(merchant['id']) +"', '0', '5'),"
			sql = sql[:len(sql)-1]
			self.cursor.execute(sql)
			self.conn.commit()

		# Random sao con lai
		rating_count = float(merchant['rating_count']);
		rating_5_count = float(merchant['rating_5_count']);

		randomStarCount = int(rating_count) - int(rating_5_count)

		if randomStarCount > 0:
			sql = "INSERT INTO merchant_rates(merchant_id, user_id, value) VALUES "
			for i in range(0, randomStarCount):
				sql += "('"+ str(merchant['id']) +"', '0', '"+ str(randint(1,4)) +"'),"

			sql = sql[:len(sql)-1]

			self.cursor.execute(sql)
			self.conn.commit()










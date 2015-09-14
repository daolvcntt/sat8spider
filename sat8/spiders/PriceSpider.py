# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.spiders import Spider
from scrapy.selector import Selector
from sat8.items import ProductPriceItem, ProductItemLoader
from time import gmtime, strftime

class PriceSpider(Spider):
	name = "price_spider"
	allowed_domains = []
	start_urls = []
	price_rule = {}
	# productList = {}

	def __init__(self):
		conn = settings['MYSQL_CONN']
		cursor = conn.cursor()
		# query = "SELECT id, link FROM products"
		query = "SELECT product_id, link, rule, allowed_domains FROM price_rules"
		cursor.execute(query)
		price_rules = cursor.fetchall()
		for pr in price_rules:
			self.allowed_domains.append(pr['allowed_domains'])
			self.start_urls.append(pr['link'])
			self.price_rule[pr['link']] = pr

		# results = cursor.fetchall()
		# for product in results:
		# 	self.start_urls.append(product['link'])
		# 	self.productList[product['link']] = product;

	# def parse(self, response):
		# pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		# pil.add_xpath('price', '//*[@id="price"]//text()')
		# link = response.url
		# pil.add_value('product_id', self.productList[link]['id'])
		# pil.add_value('source', "cellphones.com.vn")
		# pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		# pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		# yield(pil.load_item())

	def parse(self, response):
		link = response.url
		pr = self.price_rule[link]
		pil = ProductItemLoader(item = ProductPriceItem(), response = response)
		pil.add_xpath('price', pr['rule'])
		pil.add_value('product_id', pr['product_id'])
		pil.add_value('source', pr['allowed_domains'])
		pil.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		pil.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		yield(pil.load_item())
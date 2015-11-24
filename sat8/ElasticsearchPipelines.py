from elasticsearch import Elasticsearch
import time
import json

class ElasticsearchPipelines():

	def __init__(self):
		self.es = Elasticsearch()

	def process_item(self, item, spider):



		if spider.name == 'blog_spider':
			post = {
				"link" : item['link']
				"title" : item['title'],
				"category" : item['category'],
				"teaser" : item['teaser'],
				"avatar" : item['avatar'],
				"content" : item['content'],
				"type" : item['post_type'],
				"created_at" : item['created_at'],
				"updated_at" : item['updated_at']
			}

			id = int(time.time())

			self.es.index(index="nht-test", doc_type="posts", id=id, body=post)

		elif spider.name == 'product_spider' :

			id = int(time.time())

			product = {
				"name" : item["name"]
				"price" : item["price"]
				"hash_name" : item["hash_name"]
				"brand" : item["brand"]
				"image" : item["image"]
				"images" : item["images"]
				"spec" : item["spec"]
				"link" : item["link"]
				"created_at" : item["created_at"]
				"updated_at" : item["updated_at"]
			}

			self.es.index(index="nht-test", doc_type="posts", id=id, body=product)


		# print item
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
import re

def filter_price(val):
	m = re.compile(r'\D+')
	val = m.sub('', val)
	return val if val.isdigit() else None

class ProductItem(Item):
	id = Field()
	name = Field()
	price = Field()
	hash_name = Field()
	brand = Field()
	image = Field()
	images = Field()
	image_urls = Field()
	spec = Field()
	link = Field()
	created_at = Field()
	updated_at = Field()
	image_paths = Field()
	typ = Field()

	def toJson(self):
		return {
			"id" : self["id"],
			"name" : self["name"],
			"price" : self["price"],
			"hash_name" : self["hash_name"],
			"brand" : self["brand"],
			"image" : self["image"],
			"images" : self["images"],
			"spec" : self["spec"],
			"link" : self["link"],
			"created_at" : self["created_at"],
			"updated_at" : self["updated_at"]
		}

class ProductPriceItem(Item):
	id = Field()
	name = Field()
	title = Field()
	brand = Field()
	price = Field()
	source = Field()
	link = Field()
	created_at = Field()
	updated_at = Field()

	def toJson(self):
		return {
			"id" : self["id"],
			"title" : self["title"],
			"brand" : self["brand"],
			"price" : int(self["price"]),
			"source" : self["source"],
			"link" : self["link"],
			"created_at" : self["created_at"],
			"updated_at" : self["updated_at"]
		}

class BlogItem(Item):
	id = Field()
	link = Field()
	title = Field()
	teaser = Field()
	content = Field()
	avatar = Field()
	image_urls = Field()
	category_id = Field()
	product_id = Field()
	user_id = Field()
	published_time = Field()
	created_at = Field()
	updated_at = Field()
	image_paths = Field()
	typ = Field()
	category = Field()
	post_type = Field()

	def toJson(self):
		return {
			"id" : self["id"],
			"link" : self["link"],
			"title" : self["title"],
			"teaser" : self["teaser"],
			"content" : self["content"],
			"avatar" : self["avatar"],
			"category_id" : self["category_id"],
			"product_id" : self["product_id"],
			"user_id" : self["user_id"],
			"created_at" : self["created_at"],
			"updated_at" : self["updated_at"],
			"category" : self["category"],
			"post_type" : self["post_type"]
		}

class VideoItem(Item):
	link = Field()
	title = Field()
	description = Field()
	embed = Field()
	thumbnail = Field()
	author = Field()
	category_id = Field()
	product_id = Field()
	user_id = Field()

	def toJson(self):
		return {
			"link" : self["link"],
			"title" : self["title"],
			"description" : self["description"],
			"embed" : self["embed"],
			"thumbnail" : self["embed"],
			"author" : self["author"],
			"category_id" : self["category_id"],
			"product_id" : self["product_id"],
			"user_id" : self["user_id"]
		}

class ProductItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	price_in = MapCompose(remove_tags, filter_price)

class PostItemLoader(ItemLoader):
	default_output_processor = TakeFirst()

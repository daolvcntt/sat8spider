from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags
import re
from time import gmtime, strftime

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
			"id" : self.get("id"),
			"name" : self.get("name", ""),
			"price" : self.get("price", 0),
			"hash_name" : self.get("hash_name", ""),
			"brand" : self.get("brand", ""),
			"image" : self.get("image", ""),
			"images" : self.get("images", ""),
			"spec" : self.get("spec", ""),
			"link" : self.get("link", ""),
			"created_at" : self.get("created_at", strftime("%Y-%m-%d %H:%M:%S")),
			"updated_at" : self.get("updated_at", strftime("%Y-%m-%d %H:%M:%S")),
		}

class ProductPriceItem(Item):
	id = Field()
	name = Field()
	title = Field()
	brand = Field()
	price = Field()
	price_save = Field()
	source = Field()
	link = Field()
	created_at = Field()
	updated_at = Field()
	crawled_at = Field()

	def toJson(self):
		return {
			"id" : self.get("id"),
			"title" : self.get("title", ""),
			"price" : int(self.get("price", 0)),
			"source" : self.get("source", ""),
			"link" : self.get("link", ""),
			"created_at" : self.get("created_at", strftime("%Y-%m-%d %H:%M:%S")),
			"updated_at" : self.get("updated_at", strftime("%Y-%m-%d %H:%M:%S")),
			"crawled_at" : self.get("crawled_at", strftime("%Y-%m-%d %H:%M:%S")),
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
			"id" : self.get("id"),
			"link" : self.get("link", ""),
			"title" : self.get("title", ""),
			"teaser" : self.get("teaser", ""),
			"content" : self.get("content", ""),
			"avatar" : self.get("avatar", ""),
			"category_id" : self.get("category_id", 0),
			"product_id" : self.get("product_id", 0),
			"user_id" : self.get("user_id", 0),
			"created_at" : self.get("created_at", strftime("%Y-%m-%d %H:%M:%S")),
			"updated_at" : self.get("updated_at", strftime("%Y-%m-%d %H:%M:%S")),
			"category" : self.get("category", ""),
			"post_type" : self.get("post_type", "post")
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
			"link" : self.get("link", ""),
			"title" : self.get("title", ""),
			"description" : self.get("description", ""),
			"embed" : self.get("embed", ""),
			"thumbnail" : self.get("embed", ""),
			"author" : self.get("author", ""),
			"category_id" : self.get("category_id", ""),
			"product_id" : self.get("product_id", ""),
			"user_id" : self.get("user_id", "")
		}

class QuestionItem(Item):
	id = Field()
	question = Field()
	product_id = Field()
	content = Field()
	user = Field()
	link = Field()
	created_at = Field()
	updated_at = Field()

class AnswerItem(Item):
	id = Field()
	answer = Field()
	question_id = Field()
	user = Field()
	created_at = Field()
	updated_at = Field()

class ProductItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	price_in = MapCompose(remove_tags, filter_price)
	name_in = MapCompose(unicode.strip)

class ProductPriceItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	price_in = MapCompose(remove_tags, filter_price)
	title_in = MapCompose(unicode.strip)
	name_in = MapCompose(unicode.strip)

class PostItemLoader(ItemLoader):
	default_output_processor = TakeFirst()

class QuestionItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	user_in = MapCompose(unicode.strip)
	question_in = MapCompose(unicode.strip)

class AnswerItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	user_in = MapCompose(unicode.strip)
	answer_in = MapCompose(unicode.strip)

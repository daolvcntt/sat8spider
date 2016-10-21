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
	min_price = Field()
	hash_name = Field()
	brand = Field()
	image = Field()
	images = Field()
	image_urls = Field()
	image_links = Field()
	spec = Field()
	link = Field()
	brand_id = Field()
	source_id = Field()
	created_at = Field()
	updated_at = Field()
	image_paths = Field()
	typ = Field()
	is_laptop = Field()
	is_tablet = Field()
	is_mobile = Field()
	is_camera = Field()
	type = Field()
	category_id = Field()
	announce_date = Field()

	def toJson(self):
		return {
			"id" : self.get("id"),
			"name" : self.get("name", ""),
			"price" : self.get("price", 0),
			"hash_name" : self.get("hash_name", ""),
			"source_id" : self.get("source_id", 0),
			"category_id": self.get("category_id", 0),
			"brand" : self.get("brand", ""),
			"image" : self.get("image", ""),
			"images" : self.get("images", ""),
			"spec" : self.get("spec", ""),
			"link" : self.get("link", "")
		}

class ProductPriceItem(Item):
	id = Field()
	name = Field()
	title = Field()
	brand = Field()
	brand_id = Field()
	price = Field()
	price_save = Field()
	source = Field()
	source_id = Field()
	link = Field()
	is_tablet = Field()
	is_phone = Field()
	is_laptop = Field()
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
			"updated_at" : self.get("updated_at", strftime("%Y-%m-%d %H:%M:%S"))
			# "crawled_at" : self.get("crawled_at", strftime("%Y-%m-%d %H:%M:%S")),
		}

class BlogItem(Item):
	id = Field()
	link = Field()
	title = Field()
	teaser = Field()
	content = Field()
	content_text = Field()
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
	tinhte_category_link = Field()
	is_tinhte = Field()

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
			"category" : self.get("category", "")
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


class RaovatItem(Item):
	id = Field()
	title = Field()
	teaser = Field()
	content = Field()
	link = Field()
	hash_link = Field()
	is_crawl = Field()
	price = Field()
	user_name = Field()
	created_at = Field()
	updated_at = Field()
	image = Field()
	image_urls = Field()
	image_links = Field()
	info = Field()
	phone = Field()
	source = Field()

	def toJson(self):
		return {
			"id" : self.get('id'),
			"title" : self.get('title', ""),
			"teaser" : self.get('teaser', ""),
			"content" : self.get('content', ""),
			"link" : self.get('link', ""),
			'hash_link' : self.get('hash_link', ""),
			"is_crawl" : self.get('is_crawl', ""),
			"price" : self.get('is_price', ""),
			"user_name" : self.get('user_name', ''),
			"image" : self.get('image', ""),
			"info" : self.get('info', "")
		}


class MerchantItem(Item):
	id = Field()
	name = Field()
	logo = Field()
	logo_hash = Field()
	alias = Field()
	star = Field()
	image_links = Field()
	product_link = Field()
	product_name = Field()
	product_price = Field()
	is_craw = Field()
	rating_count = Field()
	rating_5_count = Field()
	percent_rating_5 = Field()

class RealEstateItem(Item):
	id = Field()
	title = Field()
	slug = Field()
	teaser = Field()
	json_tags = Field()
	placement = Field()
	placement_text = Field()
	all_keyword = Field()
	all_keyword_lower = Field()
	all_keyword_lower_no_accent = Field()
	content = Field()
	content_text = Field()
	source = Field()
	source_link = Field()
	image = Field()
	images = Field()
	images_array = Field()
	image_links = Field()
	characters = Field()
	created_at = Field()
	updated_at = Field()


class DpreviewItem(Item):
	id = Field()
	name = Field()
	announce = Field()
	type = Field()

class ProductItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	price_in = MapCompose(remove_tags, filter_price)
	name_in = MapCompose(unicode.strip)
	brand_in = MapCompose(unicode.strip)

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


class RaovatItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	title_in = MapCompose(unicode.strip)
	teaser_in = MapCompose(unicode.strip)
	user_name_in = MapCompose(unicode.strip)
	price_in = MapCompose(remove_tags, filter_price)

class MerchantItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	name_in = MapCompose(unicode.strip)
	alis_in = MapCompose(unicode.strip)
	rating_5_count_in  = MapCompose(remove_tags, filter_price)


class DpreviewItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	name_in = MapCompose(unicode.strip)
	announce_in = MapCompose(unicode.strip)

class RealEstateItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	title_in = MapCompose(unicode.strip)
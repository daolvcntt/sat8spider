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
	name = Field()
	price = Field()
	image = Field()
	spec = Field()
	link = Field()

class BlogItem(Item):
	link = Field()
	title = Field()
	teaser = Field()
	content = Field()
	avatar = Field()
	category_id = Field()
	product_id = Field()
	user_id = Field()
	published_time = Field()
	created_at = Field()
	updated_at = Field()

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

class ProductPriceItem(Item):
	product_id = Field()
	price = Field()
	source = Field()
	created_at = Field()
	updated_at = Field()

class ProductItemLoader(ItemLoader):
	default_output_processor = TakeFirst()
	price_in = MapCompose(remove_tags, filter_price)
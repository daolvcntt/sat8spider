# -*- coding: utf-8 -*-
import sys
import logging
import pymysql.cursors
from time import gmtime, strftime
from scrapy.utils.log import configure_logging

BOT_NAME = 'sat8'

SPIDER_MODULES = ['sat8.spiders']
NEWSPIDER_MODULE = 'sat8.spiders'
ITEM_PIPELINES = {
	'sat8.pipelines.MySQLStorePipeline' : 100,
	'scrapy.pipelines.images.ImagesPipeline' : 101
}
COOKIES_ENABLED = False

# Product price rules
PRODUCT_PRICE_RULES = {
	'cellphones.com.vn' : {
		'Source' : 'cellphones.com.vn',
		'StartUrls' : 'http://cellphones.com.vn/mobile.html',
		'LEAllow' : 'mobile\.html\?p\=[0-9]+',
		'LERestrict' : '//div[@class="pages"]',
		'ProductList' : '//*[@class="product-image"]/@href',
		'Title' : '//*[@id="product_addtocart_form"]//h1/text()',
		'Price' : '//*[@id="price"]'
	},
	'thegioididong.com' : {
		'Source' : 'thegioididong.com',
		'StartUrls' : 'https://www.thegioididong.com/dtdd?trang=20',
		'LEAllow' : '',
		'LERestrict' : '',
		'ProductList' : '//*[@id="lstprods"]/li/a/@href',
		'Title' : '//*[@id="topdetail"]/div/div/h1/text()',
		'Price' : '//*[@id="topdetail"]/section/div/aside[2]/strong'
	}
}

# Image download settings
IMAGES_STORE = '/home/justin/public_html/sat8web/public/uploads'
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110
IMAGES_THUMBS = {
	'small': (50, 50),
	'big': (270, 270),
}
DOWNLOAD_DELAY = 5

# SQL DATABASE SETTING
MYSQL_SERVER = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'search'

# connect to the MySQL server
try:
	MYSQL_CONN = pymysql.connect(host=MYSQL_SERVER,
										port=MYSQL_PORT,
										user=MYSQL_USER,
										password=MYSQL_PASSWORD,
										db=MYSQL_DB,
										charset='utf8',
										cursorclass=pymysql.cursors.DictCursor,
										use_unicode=True)
except pymysql.Error, e:
	logging.error("Error %d: %s" % (e.args[0], e.args[1]))
	sys.exit(1)

# configure_logging(install_root_handler=False)
# logging.basicConfig(
# 	filename='log' + strftime("%Y_%m_%d", gmtime()) + '.txt',
# 	format='%(levelname)s: %(message)s',
# 	level=logging.INFO
# )

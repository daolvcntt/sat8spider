# -*- coding: utf-8 -*-
import sys
import logging
import pymysql.cursors
import env
from time import gmtime, strftime
from scrapy.utils.log import configure_logging


BOT_NAME = 'sat8'

REACTOR_THREADPOOL_MAXSIZE = 20
CONCURRENT_REQUESTS        = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 100
RETRY_ENABLED              = True
DOWNLOAD_TIMEOUT           = 500
COOKIES_ENABLED            = True

USER_AGENT = 'Googlebot/2.1 (+http://www.google.com/bot.html)'

SPIDER_MODULES = ['sat8.spiders']
NEWSPIDER_MODULE = 'sat8.spiders'
ITEM_PIPELINES = {
	'sat8.pipelines.MySQLStorePipeline' : 100,
	# 'scrapy.pipelines.images.ImagesPipeline': 102
	# 'sat8.MyImagesPipeline.MyImagesPipeline' : 102,
	#'sat8.ConverImagePipeline.ConverImagePipeline' : 102,
	# 'sat8.YoutubePipeline.YoutubePipeline' : 101,
	'sat8.DownloadImagePipeline.DownloadImagePipeline' : 101
}


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
		'StartUrls' : 'https://www.thegioididong.com/dtdd?trang=1',
		'LEAllow' : '',
		'LERestrict' : '',
		'ProductList' : '//*[@id="lstprods"]/li/a/@href',
		'Title' : '//*[@id="topdetail"]/div/div/h1/text()',
		'Price' : '//*[@id="topdetail"]/section/div/aside[2]/strong'
	}
}

# Image download settings
IMAGES_STORE = env.IMAGES_STORE
IMAGES_MIN_HEIGHT = 90
IMAGES_MIN_WIDTH = 90
IMAGES_THUMBS = {
	'small': (120, 120),
	'big': (270, 270),
}
DOWNLOAD_DELAY = 0.5

# SQL DATABASE SETTING
MYSQL_SERVER   = env.MYSQL_SERVER
MYSQL_PORT     = env.MYSQL_PORT
MYSQL_USER     = env.MYSQL_USER
MYSQL_PASSWORD = env.MYSQL_PASSWORD
MYSQL_DB       = env.MYSQL_DB

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

# LOG_FILE = env.LOG_FILE
# LOG_LEVEL = 'ERROR'

def default_request_headers():
	return {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,vi;q=0.6,zh-CN;q=0.4,zh;q=0.2,nb;q=0.2,ru;q=0.2,cs;q=0.2',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive'
	}

DEFAULT_REQUEST_HEADERS = default_request_headers()

APP_CONFIG = {
	'default_request_headers' : default_request_headers()
}
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
}

# SQL DATABASE SETTING
MYSQL_SERVER = '127.0.0.1'
MYSQL_PORT = 33060
MYSQL_USER = 'homestead'
MYSQL_PASSWORD = 'secret'
MYSQL_DB = 'nht-starter'

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

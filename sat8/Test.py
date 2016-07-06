from scrapy.conf import settings
import pprint
import json
import datetime
from Functions import echo

conn = settings['MYSQL_CONN']
cursor = conn.cursor()

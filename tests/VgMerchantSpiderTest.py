import sys

import socket
import os

hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

from sat8.Functions import *
from sat8.Helpers.Functions import *
from sat8.pipelines import MySQLStorePipeline

from scrapy.conf import settings

import hashlib
import unittest
import datetime
import time



class VgMerchantSpiderTest(unittest.TestCase):

    def setUp(self):
        self.pipeline = MySQLStorePipeline()

    def testSaveMerchantRate(self):
        merchant = {}
        merchant['id'] = 1
        merchant['rating_5_count'] = 5
        merchant['rating_count'] = 10
        self.pipeline.saveMerchantRate(merchant)


if __name__ == '__main__':
    unittest.main()
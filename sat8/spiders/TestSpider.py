# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from sat8.items import RaovatItem, RaovatItemLoader

from sat8.Classifields.EsRaovat import EsRaovat

from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

# from sat8.Helpers.Google_Bucket import *
from sat8.Helpers.Functions import *

import urllib
import logging
import os
import re
import sys

class TestSpider(CrawlSpider):
    name = "raovat_spider"

    start_urls = []

    def __init__(self, env="production"):
        print env
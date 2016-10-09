# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader, ProductPriceItem, ProductPriceItemLoader, MerchantItem, MerchantItemLoader
from urlparse import urlparse
from time import gmtime, strftime
from scrapy.conf import settings

from sat8.Functions import parseJson4Params
from sat8.Functions import echo

import json,urllib
from urlparse import urljoin

from sat8.Helpers.Functions import *
from sat8.Helpers.Google_Bucket import *

import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

from sat8.env import API_VG_USER, API_VG_PASSWORD

class VgGetProductsByBrandUrlSpider(CrawlSpider):
    name = "vg_get_products_by_brand_url_spider"
    allowed_domains = []
    start_urls = ['http://vatgia.com']
    rules = ()

    env = 'production'

    def __init__(self, env="production"):
        self.env = env;
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

    def parse(self, response):
        conn = self.conn
        cursor = self.cursor

        print '------------------------------', "\n"
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

        sql = "SELECT * FROM vatgia_brand_links"

        if self.env == "dev":
            sql = "SELECT * FROM vatgia_brand_links  LIMIT 5"

        self.cursor.execute(sql)
        links = self.cursor.fetchall()

        image_links = []

        for link in links:
            for i in range(1, link['max_page']+1):
                url = 'http://graph.vatgia.vn/v1/products/fromurl?url=' + link['link'] + '&page=' + str(i)

                response = requests.get(url, auth=HTTPDigestAuth(API_VG_USER, API_VG_PASSWORD))
                json = response.json()

                if 'data' in json:
                    data = json['data']

                    for product in data:
                        product['link'] = 'test';

                        print product['name']

                        if product['main_picture'] != '' or product['main_picture'] != None:
                            image_links.append(product['main_picture'])

                        if len(product['pictures']) > 0:
                            for pic in product['pictures']:
                                image_links.append(pic);

                        item = {
                            "id_vatgia" : product['id'],
                            "name" : product['name'],
                            "link" : product['link'],
                            "hash_name": md5(product['name'].encode('utf-8')),
                            "price": product['price'],
                            "min_price": product['price'],
                            "image": sha1FileName(product['main_picture']),
                            "is_crawl": 1,
                            "created_at" : strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at" : strftime("%Y-%m-%d %H:%M:%S"),
                            "announce_date" : product['date'],
                            "image_links" : image_links
                        }

                        yield item
                else:
                    print 'Khong co data'
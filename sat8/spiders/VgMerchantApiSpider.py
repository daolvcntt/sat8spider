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

class VgMerchantApiSpider(CrawlSpider):
    name = "merchant_spider"
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

        sql = "SELECT id, name, source_id, link FROM products WHERE source_id = 185 ORDER BY updated_at DESC"

        if self.env == "dev":
            # sql += " LIMIT 5"
            sql = "SELECT id, name, source_id, link FROM products WHERE source_id = 185 AND id = 3426 ORDER BY updated_at DESC"

        self.cursor.execute(sql)
        products = self.cursor.fetchall()

        image_links = []



        for product in products:
            url = 'http://graph.vatgia.vn/v1/products/estore/' + str(getVGProductId(product['link']))

            response = requests.get(url, auth=HTTPDigestAuth(API_VG_USER, API_VG_PASSWORD))
            json = response.json()

            if 'data' in json:
                data = json['data']

                # Lặp mảng danh sách gian hàng
                for merchant in data:
                    print merchant['logo']

                    if merchant['logo'] == '' or merchant['logo'] == None:
                        merchant['logo'] = 'http://giaca.org/images/grey.gif'

                    thumbs = downloadImageFromUrl(merchant['logo'])

                    # Upload bucket
                    imageName = sha1FileName(merchant['logo'])

                    google_bucket_upload_object('static.giaca.org', thumbs['full'], 'uploads/full/' + imageName)
                    google_bucket_upload_object('static.giaca.org', thumbs['big'], 'uploads/thumbs/big/' + imageName)
                    google_bucket_upload_object('static.giaca.org', thumbs['small'], 'uploads/thumbs/small/' + imageName)

                    item = {}

                    item['merchant'] = {
                        "name" : merchant['url'].replace('http://www.', ''),
                        "alias": merchant['company'],
                        "logo_hash" : sha1FileName(merchant['logo']),
                        "is_craw": 1,
                        "rating_count": merchant['total_rate'],
                        "rating_5_count": merchant['good_rate'],
                        "created_at" : strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at" : strftime("%Y-%m-%d %H:%M:%S")
                    }

                    item['product'] = product

                    item['price_item'] = {
                        "title": product['name'],
                        "price": merchant['price'],
                        "source_id": product['source_id'],
                        "link": merchant['url_product'],
                        "create_at": strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": strftime("%Y-%m-%d %H:%M:%S"),
                        "crawled_at": strftime("%Y-%m-%d %H:%M:%S")
                    }

                    yield item
            else:
                print response
                print 'ProductID: ' + product['id']
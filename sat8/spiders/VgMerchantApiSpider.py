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
            sql += " LIMIT 5"

        self.cursor.execute(sql)
        products = self.cursor.fetchall()

        image_links = []



        for product in products:
            url = 'http://graph.vatgia.vn/v1/products/estore/' + str(getVGProductId(product['link']))

            response = requests.get(url, auth=HTTPDigestAuth(API_VG_USER, API_VG_PASSWORD))
            data = response.json()['data']

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


    def parse_list_merchant(self, response):
        sel = Selector(response)
        merchants = sel.xpath('//*[@id="estore_bronze_table"]//tr')

        for m in merchants:

            star = m.xpath('.//span[@class="product_rating_star"]//i[@class="star_10"]').extract()
            itemLoader = MerchantItemLoader(item = MerchantItem(), selector = m)
            itemLoader.add_xpath('name', './/div[@class="name"]//a/@href')
            itemLoader.add_xpath('alias', './/div[@class="name"]//a/text()')
            itemLoader.add_xpath('logo', './/td[@class="avatar"]/img/@data-original')
            itemLoader.add_xpath('rating_count', './/td[@class="company"]/div[@class="rating"]/span[2]/text()')
            itemLoader.add_xpath('percent_rating_5', './/td[@class="company"]/div[@class="rating"]/span[1]/text()')

            merchant = itemLoader.load_item()

            if 'rating_count' not in merchant:
                merchant['rating_count'] = 0

            if 'percent_rating_5' not in merchant:
                merchant['percent_rating_5'] = 0

            if merchant['rating_count'] > 0 and merchant['percent_rating_5'] > 0 :
                round5Rating = merchant.get('percent_rating_5', "0.0").replace('%', '')
                round5Rating = round5Rating.replace(',', '.')
                round5Rating = float(round5Rating)
                round5Rating = round(round5Rating)

                roundRatingCount = float(merchant['rating_count'])
                merchant['rating_5_count'] = round((round5Rating*roundRatingCount)/100)


            if 'rating_5_count' not in merchant:
                merchant['rating_5_count'] = 0;

            merchant["name"] = self.getUrlFromLink(response, merchant["name"])
            merchant["star"] = len(star)
            merchant["logo"] = merchant.get("logo", "").replace("small_", "")
            merchant["is_craw"] = 1;


            image_links = []

            image_links.append(merchant["logo"])

            merchant["image_links"] = image_links
            merchant["logo_hash"] = sha1FileName(merchant["logo"])

            linkProduct = m.xpath('.//a[@class="form_button_3"]/@href').extract()
            linkProduct = self.getProductDetailLink(response, linkProduct[0])

            request = scrapy.Request(linkProduct, callback=self.parse_product_detail)
            request.meta['merchant'] = merchant
            request.meta['product'] = response.meta['product']

            yield request


    def parse_product_detail(self, response):
        priceItemLoader = ProductItemLoader(item = ProductItem(), response = response)
        priceItemLoader.add_xpath('name', '//h1[@id="detail_product_name"]/text()')
        priceItemLoader.add_xpath('price', '//div[@id="detail_product_price"]//b[@class="product_price"]/text()')
        priceItemLoader.add_value('link', response.url)

        priceItem = priceItemLoader.load_item()

        item = {
            "merchant" : response.meta['merchant'],
            "product" : response.meta['product'],
            "price_item" : priceItem,
            "image_links" : response.meta['merchant']["image_links"]
        }

        if self.env == 'dev':
            print item
            return

        yield item


    # def start_requests(self):
    #     conn = self.conn
    #     cursor = self.cursor

    #     print '------------------------------', "\n"
    #     self.conn = settings['MYSQL_CONN']
    #     self.cursor = self.conn.cursor()

    #     sql = "SELECT id, name, source_id, link FROM products WHERE source_id = 185 ORDER BY updated_at DESC"

    #     if self.env == "dev":
    #         sql += " LIMIT 5"

    #     self.cursor.execute(sql)
    #     products = self.cursor.fetchall()

    #     image_links = []



    #     for product in products:
    #         url = 'http://graph.vatgia.vn/v1/products/estore/' + str(getVGProductId(product['link']))

    #         response = requests.get(url, auth=HTTPDigestAuth(API_VG_USER, API_VG_PASSWORD))
    #         data = response.json()['data']

    #         # Lặp mảng danh sách gian hàng
    #         for merchant in data:
    #             image_links.append(merchant["logo"])
    #             item = {}
    #             item['merchant'] = {
    #                 "name" : merchant['url'].replace('http://www.', ''),
    #                 "alias": merchant['company'],
    #                 "logo" : sha1FileName(merchant['logo']),
    #                 "is_crawl": 1,
    #                 "rating_count": merchant['total_rate'],
    #                 "rating_5_count": merchant['good_rate'],
    #                 "created_at" : strftime("%Y-%m-%d %H:%M:%S"),
    #                 "updated_at" : strftime("%Y-%m-%d %H:%M:%S")
    #             }

    #             item['product'] = product

    #             item['price_item'] = {
    #                 "title": product['name'],
    #                 "price": merchant['price'],
    #                 "source_id": product['source_id'],
    #                 # "link": merchant['product_detail_url'],
    #                 "link": "",
    #                 "create_at": strftime("%Y-%m-%d %H:%M:%S"),
    #                 "updated_at": strftime("%Y-%m-%d %H:%M:%S"),
    #                 "crawled_at": strftime("%Y-%m-%d %H:%M:%S")
    #             }

    #             # yield(item)





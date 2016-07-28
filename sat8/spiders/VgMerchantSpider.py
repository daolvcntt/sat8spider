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

class VgMerchantSpider(CrawlSpider):
    name = "merchant_spider"
    allowed_domains = []
    start_urls = []
    rules = ()

    env = 'production'

    # Response return html
    RESPONSE_HTML = 0

    # Response return json with value is html, {key: HTML}
    RESPONSE_JSON_HTML = 1

    RESPONSE_JSON = 2

    def __init__(self, env="production"):
        self.env = env;
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

    def parse(self, response):
        sel = Selector(response)
        linksToListMerchant = sel.xpath('//*[@class="product_thumb_view"]//a[@class="picture_link"]/@href')

        for pl in linksToListMerchant:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback=self.parse_list_merchant)
            yield request
            break


    def parse_list_merchant(self, response):
        sel = Selector(response)
        merchants = sel.xpath('//*[@id="estore_bronze_table"]//tr')

        for m in merchants:

            star = m.xpath('.//span[@class="product_rating_star"]//i[@class="star_10"]').extract()
            itemLoader = MerchantItemLoader(item = MerchantItem(), selector = m)
            itemLoader.add_xpath('name', './/div[@class="name"]//a/@href')
            itemLoader.add_xpath('alias', './/div[@class="name"]//a/@title')
            itemLoader.add_xpath('logo', './/td[@class="avatar"]/img/@data-original')

            merchant = itemLoader.load_item()
            merchant["name"] = self.getUrlFromLink(response, merchant["name"])
            merchant["star"] = len(star)

            image_links = []
            # image_links.append(merchant["logo"])

            merchant["image_links"] = image_links
            merchant["logo_hash"] = sha1FileName(merchant["logo"])

            linkProduct = m.xpath('.//a[@class="form_button_3"]/@href').extract()
            linkProduct = self.getProductDetailLink(response, linkProduct[0])

            request = scrapy.Request(linkProduct, callback=self.parse_product_detail)
            request.meta['merchant'] = merchant
            yield request


    def parse_product_detail(self, response):
        priceItemLoader = ProductItemLoader(item = ProductItem(), response = response)
        priceItemLoader.add_xpath('name', '//h1[@id="detail_product_name"]/text()')
        priceItemLoader.add_xpath('price', '//div[@id="detail_product_price"]//b[@class="product_price"]/text()')

        priceItem = priceItemLoader.load_item()

        yield {
            "merchant" : response.meta['merchant'],
            "price_item" : priceItem,
            "image_links" : response.meta['merchant']["image_links"]
        }

    def start_requests(self):
        conn = self.conn
        cursor = self.cursor

        print '------------------------------', "\n"
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

        sql = "SELECT DISTINCT id,keyword,rate_keyword FROM products WHERE rate_keyword != '' OR rate_keyword != NULL ORDER BY updated_at DESC"

        if self.env == "dev":
            sql += " LIMIT 5"

        self.cursor.execute(sql)
        products = self.cursor.fetchall()


        for product in products:
            url = 'http://vatgia.com/home/quicksearch.php?keyword=%s&show=product&verified=1' %product['keyword']
            request = scrapy.Request(url)
            yield request



    def getUrlFromLink(self, response, url):

        url = urlparse(url)

        path = url.path

        url = urljoin(response.url, path)

        indexQueryStr = url.find('&')

        if(indexQueryStr >= 0):
            return url[:indexQueryStr]

        return url

    def getProductDetailLink(self, response, url):
        url = urlparse(url)

        path = url.path

        url = urljoin(response.url, path)

        return url

    # Make request
    def makeRequest(self, url, linkItem):
        headers = settings['APP_CONFIG']['default_request_headers']
        request = scrapy.Request(url, callback = self.parse_detail_content, headers = headers)
        request.meta['link_item'] = linkItem
        request.meta['dont_redirect'] = True

        return request



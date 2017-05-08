# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime
from scrapy.conf import settings

from sat8.Functions import parseJson4Params
from sat8.Functions import echo

import json,urllib
from urlparse import urljoin

from sat8.Helpers.Functions import *
import socket

hostname = socket.gethostname()

class TestTxncMinisoSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = []
    start_urls = []
    rules = ()

    env = 'production'

    # Response return html
    RESPONSE_HTML = 0

    # Response return json with value is html, {key: HTML}
    RESPONSE_JSON_HTML = 1

    RESPONSE_JSON = 2

    def __init__(self, env = 'production'):
        self.env = env
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

    def parse_item(self, response):
        url = response.url;
        yield self.makeRequest(url)

    # Return product to crawl
    def get_product(self, response):
        link = response.url

        url_parts = urlparse(link)
        linkItem  = {
            'image' : '//*[@class="MagicZoom"]/@href',
            'images' : '//*[@class="MagicZoom"]/@href',
            'meta_xpath_name': '//*[@class="title-cate-product"]/text()',
            'meta_xpath_price': '//*[@class="price-info-product"]/text()',
            'site_id' : 2492,
            'brand_id': 63,
            'meta_xpath_spec': '//*[@class="title-cate-product"]/text()',
            'is_laptop': 0,
            'is_mobile': 0,
            'is_tablet': 0,
            'is_camera': 0,
            'type' : 0,
            'category_id': 8
        }

        pil = ProductItemLoader(item = ProductItem(), response = response)

        pil.add_xpath('image', linkItem['image'])
        pil.add_xpath('name', linkItem['meta_xpath_name'])
        pil.add_xpath('price', linkItem['meta_xpath_price'])
        pil.add_value('source_id', linkItem['site_id'])
        pil.add_value('brand_id', linkItem['brand_id'])
        pil.add_xpath('spec', linkItem['meta_xpath_spec'])
        pil.add_value('link', link)
        pil.add_value('is_laptop', linkItem['is_laptop'])
        pil.add_value('is_mobile', linkItem['is_mobile'])
        pil.add_value('is_tablet', linkItem['is_tablet'])
        pil.add_value('is_camera', linkItem['is_camera'])
        pil.add_value('type', linkItem['type'])
        pil.add_value('category_id', linkItem['category_id'])

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath(linkItem['images']);

        dataImage = []
        image_urls = []

        for img in images:
            imgLink = response.urljoin(img.extract())
            image_urls.append(imgLink)

            imgLinkHash = sha1FileName(imgLink)
            dataImage.append(imgLinkHash)

        product = pil.load_item()

        parseUrlImage = urlparse(product['image'])

        # Tạo link ảnh chuẩn http://xxx
        if parseUrlImage.scheme == '':
            if parseUrlImage.netloc != '':
                product['image'] = urljoin('http://' + parseUrlImage.netloc, parseUrlImage.path)
            else:
                product['image'] = urljoin('http://' + url_parts.netloc, parseUrlImage.path)

        image_urls.append(product['image'])

        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        product['name']       = product['name'].strip(' \t\n\r')
        product['name']       = product['name'].strip()
        product['image']      = sha1FileName(product['image'])
        product['images']     = ',' . join(dataImage)
        product['image_links'] = image_urls
        product['hash_name']  = md5(product['name'].encode('utf-8'))
        product['price']      = price
        product['min_price']  = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        if 'spec' not in product:
            product['spec'] = '';

        return product


    # Process crawl product
    def parse_detail_content(self, response):
        urlPart = urlparse(response.url)
        product = self.get_product(response)

        print '-----------3. parse_detail_content--------------';

        if self.env == 'production':
            yield product
        else:
            print product

    def parseJsonDetailContent(self, response):
        yield self.getProductJson(response)

    def start_requests(self):

        # request = scrapy.FormRequest(url=startLink, callback=self.parse_item)

        print '--------1. start_requests -----------';

        links = [
            'http://minisovietnam.vn/do-choi-bang-nhua-040315-pd,34663',
            'http://minisovietnam.vn/do-choi-bang-nhua-040322-pd,34662',
            'http://minisovietnam.vn/but-danh-dau--mau-hong-sang-838453-pd,34657',
            'http://minisovietnam.vn/bang-viet-08270-pd,34652',
            'http://minisovietnam.vn/bang-viet-08256-pd,34650',
            'http://minisovietnam.vn/no-deo-co-nam-194124-pd,57384'
        ]

        for startLink in links:
            headers = settings['APP_CONFIG']['default_request_headers']

            request = scrapy.Request(startLink, callback = self.parse_detail_content, headers = headers)
            request.meta['dont_redirect'] = True

            yield request


    def getUrlFromLink(self, response, url):
        url_parts = urlparse(response.url)

        url = urlparse(url)

        path = url.path

        url = urljoin(response.url, path)

        return url

        # url = url_parts.scheme + '://' + url_parts.netloc + '/' + path

        # return url


    # Make request
    def makeRequest(self, url):

        print '------2. JUMP TO makeRequest-------';

        headers = settings['APP_CONFIG']['default_request_headers']

        request = scrapy.Request(url, callback = self.parse_detail_content, headers = headers)
        request.meta['dont_redirect'] = True

        return request



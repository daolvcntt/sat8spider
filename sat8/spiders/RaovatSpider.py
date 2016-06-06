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

import urllib
import logging


class RaovatSpider(CrawlSpider):
    name = "raovat_spider"

    allowed_domains = ['vatgia.com']

    questionId = 0
    productId = 0;

    def __init__(self):
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()


    def parse_item(self, response):

        sel = Selector(response)
        product_links = sel.xpath('//*[@class="raovat_listing"]/li[@class="info"]//a[@class="tooltip"][1]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback=self.parse_raovat)
            request.meta['productId'] = response.meta['productId']
            yield request


    def parse_raovat(self, response):
        productId = response.meta['productId']
        raovatItemLoader = RaovatItemLoader(item = RaovatItem(), response = response)
        raovatItemLoader.add_xpath('title', '//*[@class="infomation_raovat fr"]/h1//text()')
        raovatItemLoader.add_value('link', response.url)
        raovatItemLoader.add_value('is_crawl', 1)
        raovatItemLoader.add_xpath('user_name', '//*[@class="userPostInfor fl"]/p/b//text()')
        raovatItemLoader.add_xpath('price', '//*[@class="detail_price"]/div/span/text()')
        raovatItemLoader.add_xpath('teaser', '//*[@id="main_description"]//text()')
        raovatItemLoader.add_xpath('content', '//*[@id="main_description"]')
        raovatItemLoader.add_xpath('info', '//*[@class="raovat_list_info"]')
        raovatItemLoader.add_xpath('image', '//*[@class="img-raovat"]//img[1]/@src')
        raovatItemLoader.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        raovatItemLoader.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))

        raovatItem = raovatItemLoader.load_item()
        # raovatItem['link'] = 'http://vatgia.com' + raovatItem['link'];
        raovatItem['hash_link'] = hashlib.md5(raovatItem['link']).hexdigest()

        if 'user_name' not in raovatItem:
            raovatItem['user_name'] = ''

        if 'price' not in raovatItem:
            raovatItem['price'] = 0

        if 'teaser' not in raovatItem:
            raovatItem['teaser'] = ''

        if 'content' not in raovatItem:
            raovatItem['content'] = ''

        raovatItem['teaser'] = raovatItem['teaser'][0:250]

        query = "SELECT id,link FROM classifields WHERE hash_link = %s"
        self.cursor.execute(query, (raovatItem['hash_link']))
        result = self.cursor.fetchone()

        raovatId = 0;
        if result:
            raovatId = result['id']
            sql = "UPDATE classifields SET content = %s, image = %s, info = %s, updated_at = %s WHERE id = %s"
            self.cursor.execute(sql, (raovatItem['content'], raovatItem['image'], raovatItem['info'] , raovatItem['updated_at'] ,raovatId))
            self.conn.commit()
            logging.info("Item already stored in db: %s" % raovatItem['link'])
        else:
            sql = "INSERT INTO classifields (product_id, title, teaser, content, user_name, image, info, is_crawl, price, link, hash_link, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (productId, raovatItem['title'], raovatItem['teaser'], raovatItem['content'], raovatItem['user_name'], raovatItem['image'], raovatItem['info'] , raovatItem['is_crawl'] ,raovatItem['price'], raovatItem['link'], raovatItem['hash_link'] ,raovatItem['created_at'], raovatItem['updated_at']))
            self.conn.commit()
            logging.info("Item stored in db: %s" % raovatItem['link'])
            raovatId = self.cursor.lastrowid

        raovatItem["id"] = raovatId
        # Insert elasticsearch
        esRaovat = EsRaovat()
        esRaovat.insertOrUpdate(raovatId, raovatItem.toJson())

        # yield raovatItem


    def start_requests(self):
        print '------------------------------', "\n"
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT DISTINCT id,keyword,rate_keyword FROM products WHERE rate_keyword != '' OR rate_keyword != NULL ORDER BY updated_at DESC")
        products = self.cursor.fetchall()

        # url = 'http://vatgia.com/raovat/quicksearch.php?keyword=Sony+Xperia+Z3'
        # request = scrapy.Request(url, callback = self.parse_item)
        # request.meta['productId'] = 0
        # yield request

        for product in products:
            url = 'http://vatgia.com/raovat/quicksearch.php?keyword=%s' %product['rate_keyword']
            # self.start_urls.append(url)
            request = scrapy.Request(url, callback = self.parse_item)
            request.meta['productId'] = product['id']
            yield request

        # yield scrapy.Request(response.url, callback=self.parse_item)
        print '------------------------------', "\n\n"

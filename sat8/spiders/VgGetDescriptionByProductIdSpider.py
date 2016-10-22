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
# from sat8.Helpers.Google_Bucket import *

import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

from sat8.env import API_VG_USER, API_VG_PASSWORD

class VgGetDescriptionByProductIdSpider(CrawlSpider):
    name = "vg_get_products_description_technical_spider"
    allowed_domains = []
    start_urls = ['http://vatgia.com']
    rules = ()

    env = 'production'

    pathSaveImage = 'http://static.giaca.org/uploads/products/'

    bucket = 'static.giaca.org'

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

        sql = "SELECT * FROM products WHERE source_id = 185 AND id_vatgia > 0"

        if self.env == "dev":
            sql += " LIMIT 5"

        self.cursor.execute(sql)
        products = self.cursor.fetchall()

        image_links = []

        for pro in products:
            url = 'http://graph.vatgia.vn/v1/products/technical/' + str(pro['id_vatgia'])

            response = requests.get(url, auth=HTTPDigestAuth(API_VG_USER, API_VG_PASSWORD))
            json_data = response.json()

            if 'data' in json_data:
                data = json_data['data']

                product = data[0]

                spect_json = json.dumps(product['technical'])
                tags_json = json.dumps(product['keywords'])

                self.processing_content_image(product['description']);

                # Replace something
                product['description'] = replace_link(product['description'])
                try:
                    product['description'] = replace_image(product['description'], self.pathSaveImage, 'http://vatgia.com')
                except IOError as e:
                    print "Erro description image : " + url

                query = "SELECT product_id FROM product_metas WHERE product_id = %s"
                self.cursor.execute(query, (pro['id']))
                result = self.cursor.fetchone()

                if result:
                    sql = "UPDATE product_metas SET content = %s, spec_json = %s WHERE product_id = %s"
                    self.cursor.execute(sql, (product['description'], spect_json, pro['id']))
                    self.conn.commit();
                else:
                    sql = "INSERT INTO product_metas(content, spec_json, json_tags_vg, product_id) VALUES(%s,%s,%s,%s)"
                    self.cursor.execute(sql, (product['description'], spect_json, tags_json, pro['id']))
                    self.conn.commit();


            else:
                print 'Khong co data'

    def processing_content_image(self, text):
        selector = Selector(text=text)
        images = selector.xpath('//img/@src')

        for image in images:
            imgname = image.extract()
            parse = urlparse(imgname)

            if parse.scheme:
                imgLink = imgname
            else:
                imgLink = 'http://vatgia.com' + imgname

            # imgLink = response.urljoin(image.extract())

            print "Download image:" + imgLink

            imageName = sha1FileName(imgLink)
            pathSaveImage = settings['IMAGES_STORE'] + '/products/' + imageName

            # Download to tmp file
            urllib.urlretrieve(imgLink, pathSaveImage)

            # Upload to bucket
            # google_bucket_upload_object(self.bucket, pathSaveImage, 'uploads/products/' + imageName)

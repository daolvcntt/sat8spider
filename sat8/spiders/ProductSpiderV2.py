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


class ProductSpiderV2(CrawlSpider):
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

    def __init__(self):
        self.conn = settings['MYSQL_CONN']
        self.cursor = self.conn.cursor()

    def parse_item(self, response):
        linkItem = response.meta['link_item']

        url_parts = urlparse(response.url)

        # HTML
        if linkItem['response_type'] == self.RESPONSE_HTML:
            sel = Selector(response)
            product_links = sel.xpath(linkItem['link_item'])

            for pl in product_links:

                url = self.getUrlFromLink(response, pl.extract())

                yield self.makeRequest(url, linkItem)

        # Response là json , có 1 key chứa data html
        elif linkItem['response_type'] == self.RESPONSE_JSON_HTML:
            jsonresponse = json.loads(response.body_as_unicode())

            tempJsonResponse = jsonresponse

            jsonKey = linkItem['json_key']
            jsonKeySplit = jsonKey.split('.')

            for key in jsonKeySplit:
                tempJsonResponse = tempJsonResponse.get(key)

            sel = Selector(text=tempJsonResponse)

            product_links = sel.xpath(linkItem['xpath_link_detail'])

            for pl in product_links:
                url = self.getUrlFromLink(response, pl.extract())
                yield self.makeRequest(url, linkItem)

        # Response là json
        elif linkItem['response_type'] == self.RESPONSE_JSON:
            jsonresponse = json.loads(response.body_as_unicode())

            tempJsonResponse = jsonresponse

            jsonKey = linkItem['json_key']
            jsonKeySplit = jsonKey.split('.')

            for key in jsonKeySplit:
                tempJsonResponse = tempJsonResponse.get(key)

            product_links = tempJsonResponse

            # Loop array json
            for pl in product_links:
                url = pl[linkItem['xpath_link_detail']]
                request = scrapy.Request(url=url, callback=self.parseJsonDetailContent)
                request.meta['linkItem'] = linkItem
                request.meta['site'] = site
                request.meta['item'] = pl
                yield request

    # Get product json
    def getProductJson(self, response):
        linkItem = response.meta['linkItem']
        site     = response.meta['site']
        item     = response.meta['item']

        link = item.get(linkItem['xpath_link_detail'])

        pil = ProductItemLoader(item = ProductItem(), response = response)

        pil.add_value('name', item.get(linkItem['meta_xpath_name']))
        pil.add_value('image', item.get(linkItem['image']))
        pil.add_value('price', item.get(linkItem['meta_xpath_price']))
        pil.add_value('site_id', linkItem['site_id'])
        pil.add_value('brand_id', linkItem['brand_id'])
        pil.add_value('link', link)
        pil.add_value('is_laptop', linkItem['is_laptop'])
        pil.add_value('is_mobile', linkItem['is_mobile'])
        pil.add_value('is_tablet', linkItem['is_tablet'])

        product = pil.load_item()

        # Price
        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        product['name'] = product['name'].strip(' \t\n\r')
        product['name'] = product['name'].strip()

        product['image']      = hashlib.sha1(pil.get_value(product['image'])).hexdigest() + '.jpg'

        product['price']      = price
        product['hash_name']  = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        return product

    # Return product to crawl
    def get_product(self, response):
        link = response.url

        url_parts = urlparse(link)
        linkItem  = response.meta['link_item']

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

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath(linkItem['images']);

        dataImage = []
        image_urls = []

        for img in images:
            imgLink = response.urljoin(img.extract())
            image_urls.append(imgLink)

            imgLinkHash = hashlib.sha1(imgLink).hexdigest() + '.jpg'
            dataImage.append(imgLinkHash)

        product = pil.load_item()

        parseUrlImage = urlparse(product['image'])

        if parseUrlImage.scheme == '':
            product['image'] = urljoin('http://' + parseUrlImage.netloc, parseUrlImage.path)

        image_urls.append(product['image'])

        # echo(image_urls)
        # return
        # Price
        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        product['name']       = product['name'].strip(' \t\n\r')
        product['name']       = product['name'].strip()
        product['image']      = hashlib.sha1(product['image']).hexdigest() + '.jpg'
        product['images']     = ',' . join(dataImage)
        product['image_urls'] = image_urls
        product['hash_name']  = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        return product


    # Get sites for crawler
    def get_avaiable_sites(self):
        conn = self.conn
        cursor = self.cursor

        query = "SELECT sites.* FROM sites WHERE allow_crawl = 1"

        # Nếu env = testing thì thêm điều kiện testing
        if self.env == 'testing':
            query = query + " AND sites.env_testing = 1"

        # Nếu muốn chạy ngay thì chạy
        if self.env == 'quick':
            query = query + " AND sites.env_quick = 1";

        cursor.execute(query)
        sites = cursor.fetchall()

        if not sites:
            errMsg = str("----------------------------------------------------------------------------------------------\n")
            errMsg = errMsg + 'No site allow crawl or testing'
            errMsg = errMsg + "\n----------------------------------------------------------------------------------------------\n";
            raise ValueError(errMsg)

        return sites;


    # Process crawl product
    def parse_detail_content(self, response):
        yield self.get_product(response)

    def parseJsonDetailContent(self, response):
        yield self.getProductJson(response)

    def start_requests(self):
        conn = self.conn
        cursor = self.cursor

        try:

            sites = self.get_avaiable_sites()
            siteIdsList = ''
            for site in sites:
                siteIdsList = siteIdsList + str(site['id']) + ','

            siteIdsList = siteIdsList[:-1];

            queryLink = "SELECT product_xlinks.*, product_xpaths.name as meta_xpath_name, product_xpaths.price as meta_xpath_price, product_xpaths.image, product_xpaths.images, product_xpaths.link_item, product_xpaths.spec as meta_xpath_spec FROM product_xlinks JOIN product_xpaths ON xpath_id = product_xpaths.id WHERE product_xlinks.site_id IN ("+ siteIdsList +") ORDER BY product_xlinks.id DESC"
            cursor.execute(queryLink)
            links = cursor.fetchall()

            for link in links:
                if link["max_page"] > 0:
                    for i in range(1, link["max_page"]+1):

                        startLink = link["url"].replace('[0-9]+', str(i * link['step_page']))
                        cookies  = link['cookies']
                        formdata = link['form_data']
                        headers  = link['header']
                        method   = link['request_method']

                        if formdata != '' and formdata != None:
                            formdata = parseJson4Params(formdata)

                        if headers != '' and formdata != None:
                            headers = parseJson4Params(headers)

                        if cookies != '' and formdata != None:
                            cookies = parseJson4Params(cookies)

                        # Tăng biến phân trang
                        if link['param_page'] in formdata and isinstance(formdata, dict):
                            formdata[link['param_page']] = str(i * link['step_page'])

                        request = scrapy.FormRequest(url=startLink, callback=self.parse_item, formdata=formdata, method=method, headers=headers, cookies=cookies)
                        request.meta['link_item'] = link
                        yield request

        except ValueError as e:
            print e



    def getUrlFromLink(self, response, url):
        url_parts = urlparse(response.url)

        url = urlparse(url)

        path = url.path

        url = urljoin(response.url, path)

        return url

        # url = url_parts.scheme + '://' + url_parts.netloc + '/' + path

        # return url


    # Make request
    def makeRequest(self, url, linkItem):
        request = scrapy.Request(url, callback = self.parse_detail_content)
        request.meta['link_item'] = linkItem
        request.meta['dont_redirect'] = True

        return request



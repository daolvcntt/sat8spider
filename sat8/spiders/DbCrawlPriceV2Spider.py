# -*- coding: utf-8 -*-
# Xpath được lấy tự động từ database
# Mỗi ngày lấy 15000 links
# @author Justin <cong.itsoft@gmail.com>
# @date 2016-04-05
import scrapy
import re
import datetime
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductPriceItemLoader
from urlparse import urlparse
from time import gmtime, strftime
from scrapy.conf import settings

from sat8.Functions import parseJson4Params
from sat8.Functions import echo

import json,urllib
from urlparse import urljoin


class DbCrawlPriceV2Spider(CrawlSpider):
    name = "product_link"
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
        site = response.meta['site']

        url_parts = urlparse(response.url)

        # HTML
        if linkItem['response_type'] == self.RESPONSE_HTML:
            sel = Selector(response)
            product_links = sel.xpath(linkItem['xpath_link_detail'])

            for pl in product_links:

                url = self.getUrlFromLink(response, pl.extract())

                yield self.makeRequest(url, site, linkItem)

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
                yield self.makeRequest(url, site, linkItem)

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

        pil = ProductPriceItemLoader(item = ProductPriceItem(), response = response)

        pil.add_value('title', item.get(linkItem['meta_xpath_name']))
        pil.add_value('price', item.get(linkItem['meta_xpath_price']))
        pil.add_value('source', site['name'])
        pil.add_value('source_id', linkItem['site_id'])
        pil.add_value('brand_id', linkItem['brand_id'])
        pil.add_value('link', link)
        pil.add_value('is_laptop', linkItem['is_laptop'])
        pil.add_value('is_phone', linkItem['is_phone'])
        pil.add_value('is_tablet', linkItem['is_tablet'])

        product = pil.load_item()

        # Price
        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        product['title'] = product['title'].strip(' \t\n\r')
        product['title'] = product['title'].strip()
        product['name']  = product['title']

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['crawled_at'] = strftime("%Y-%m-%d %H:%M:%S")

        return product

    # Return product to crawl
    def get_product(self, response):
        link = response.url

        url_parts = urlparse(link)
        site = response.meta['site']
        linkItem = response.meta['link_item']

        pil = ProductPriceItemLoader(item = ProductPriceItem(), response = response)

        pil.add_xpath('title', linkItem['meta_xpath_name'])
        pil.add_xpath('price', linkItem['meta_xpath_price'])

        pil.add_value('source', site['name'])
        pil.add_value('source_id', linkItem['site_id'])
        pil.add_value('brand_id', linkItem['brand_id'])
        pil.add_value('link', link)
        pil.add_value('is_laptop', linkItem['is_laptop'])
        pil.add_value('is_phone', linkItem['is_phone'])
        pil.add_value('is_tablet', linkItem['is_tablet'])

        product = pil.load_item()

        # Price
        price = pil.get_value(product.get('price', "0").encode('utf-8'))
        price = re.sub('\D', '', price)

        product['title'] = product['title'].strip(' \t\n\r')
        product['title'] = product['title'].strip()
        product['name']  = product['title']

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['crawled_at'] = strftime("%Y-%m-%d %H:%M:%S")

        return product

    # Process crawl product
    def parse_detail_content(self, response):
        yield self.get_product(response)

    def parseJsonDetailContent(self, response):
        yield self.getProductJson(response)


    # Get sites for crawler
    def get_avaiable_sites(self):
        conn = self.conn
        cursor = self.cursor

        # Ngày trong tuần
        weekday = datetime.datetime.today().weekday()

        # Lấy các site sẽ chạy ngày hôm nay

        query = "SELECT sites.* FROM sites JOIN site_cronjob ON sites.id = site_cronjob.site_id WHERE day = %s AND allow_crawl = 1 AND parent_id = 0"

        # Nếu env = testing thì thêm điều kiện testing
        if self.env == 'testing':
            query = query + " AND sites.env_testing = 1"

        # Nếu muốn chạy ngay thì chạy
        if self.env == 'quick':
            query = query + " AND sites.env_quick = 1";

        cursor.execute(query,(weekday))
        sites = cursor.fetchall()

        if not sites:
            errMsg = str("----------------------------------------------------------------------------------------------\n")
            errMsg = errMsg + 'Ngày hôm nay chưa có site nào được đặt cronjob, vui lòng đặt cronjob cho từng site trong Admin'
            errMsg = errMsg + "\n----------------------------------------------------------------------------------------------\n";
            raise ValueError(errMsg)

        return sites;

    def start_requests(self):
        conn = self.conn
        cursor = self.cursor

        try:
            sites = self.get_avaiable_sites()

            crawlLinks = []

            for site in sites:
                queryLink = "SELECT site_links.*, site_metas.xpath_name as meta_xpath_name, site_metas.xpath_price as meta_xpath_price, site_metas.xpath_link_detail FROM site_links JOIN site_metas ON xpath_id = site_metas.id WHERE site_links.site_id = %s ORDER BY site_links.id DESC"
                cursor.execute(queryLink, (site["id"]))
                links = cursor.fetchall()

                for link in links:
                    if link["max_page"] > 0:
                        for i in range(1, link["max_page"]+1):

                            startLink = link["link"].replace('[0-9]+', str(i * link['step_page']))
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
                            if link['param_page'] != '' and link['param_page'] != None and link['param_page'] in formdata and isinstance(formdata, dict):
                                formdata[link['param_page']] = str(i * link['step_page'])

                            request = scrapy.FormRequest(url=startLink, callback=self.parse_item, formdata=formdata, method=method, headers=headers, cookies=cookies)

                            request.meta['site'] = site
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
    def makeRequest(self, url, site, linkItem):
        request = scrapy.Request(url, callback = self.parse_detail_content)
        request.meta['site'] = site
        request.meta['link_item'] = linkItem
        request.meta['dont_redirect'] = True

        return request



# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductPriceItemLoader
from urlparse import urlparse
from time import gmtime, strftime
from scrapy.conf import settings

conn = settings['MYSQL_CONN']
cursor = conn.cursor()

class DbPriceSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = []
    start_urls = []
    rules = ()

    def parse_item(self, response):
        sel = Selector(response)
        site = response.meta['site']

        product_links = sel.xpath(site['xpath_link_detail'])
        for pl in product_links:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback = self.parse_detail_content)
            request.meta['site'] = site
            yield request

    def parse_detail_content(self, response):
        link = response.url
        url_parts = urlparse(link)
        site = response.meta['site']

        pil = ProductPriceItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', site['xpath_name'])
        pil.add_xpath('price', site['xpath_price'])
        pil.add_value('source', site['name'])
        pil.add_value('link', link)

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


        yield(product)


    def start_requests(self):
        query = "SELECT * FROM sites JOIN site_metas ON sites.id = site_metas.site_id"
        cursor.execute(query)
        sites = cursor.fetchall()

        for site in sites:
            queryLink = "SELECT * FROM site_links WHERE site_id = %s"
            cursor.execute(queryLink, (site["id"]))
            links = cursor.fetchall()

            for link in links:
                if link["max_page"] > 0:
                    for i in range(1, link["max_page"]):
                        startLink = link["link"].replace('[0-9]+', str(i))

                        request = scrapy.Request(startLink, callback = self.parse_item)
                        request.meta['site'] = site
                        yield request
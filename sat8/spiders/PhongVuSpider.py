# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductPriceItem, ProductItemLoader
from urlparse import urlparse
from time import gmtime, strftime

class PhongVuSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ["phongvu.vn"]
    start_urls = ['http://phongvu.vn/may-tinh/may-tinh-xach-tay-laptop-1670c.html',]
    rules = (
        Rule (LinkExtractor(allow=('http://phongvu.vn/may-tinh/may-tinh-xach-tay-laptop-1670/cpage\-[0-9]+\.html')), callback='parse_item', follow= True),
    )

    images = [];

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="picsp"]/a[1]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@class="chitietsp"]/h1/text()')
        pil.add_xpath('price', '//*[@class="giasp"]/text()')
        pil.add_xpath('brand', '//*[@class="breadcrumb"]/ul/li/a[3]/text()')
        pil.add_value('source', url_parts.netloc)
        pil.add_value('link', link)

        product = pil.load_item()

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        yield(product)

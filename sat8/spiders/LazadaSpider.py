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

class LazadaSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ["www.lazada.vn"]
    start_urls = [
        'http://www.lazada.vn/laptop/?page=2',
    ]
    rules = (
        Rule (LinkExtractor(allow=('http://www.lazada.vn/laptop/\?page=[0-9]+')), callback='parse_item', follow= True),
    )

    images = [];

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.css('.product-card.new_.outofstock a').xpath('@href');

        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@id="prod_title"]/text()')
        pil.add_xpath('price', '//*[@id="special_price_box"]/text()')
        pil.add_value('source', url_parts.netloc)
        pil.add_value('link', link)
        pil.add_xpath('brand', '//*[@class="prod_header_brand_action"]/a/span/text()')

        product = pil.load_item()

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)
        product['title'] = product['title'].strip(' \t\n\r')
        product['title'] = product['title'].strip()
        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        print product

        return


        yield(product)

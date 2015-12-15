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

class AnKhangSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ["www.ankhang.vn"]
    start_urls = [
        'http://www.ankhang.vn/may-tinh-xach-tay_dm167.html',
    ]
    rules = (
        Rule (LinkExtractor(allow=('may-tinh-xach-tay_dm167.html\?page=[0-9]+')), callback='parse_item', follow= True),
    )

    images = [];

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="p_container"]//a[@class="p_name"]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@id="overview"]/h1/text()')
        pil.add_xpath('price', '//*[@id="price_detail"]/div[@class="img_price_full"]/text()')
        pil.add_value('source', url_parts.netloc)
        pil.add_value('link', link)

        product = pil.load_item()

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        product['price']      = price
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['brand']      = (pil.get_value(product['title'])).split(" ")[0]

        yield(product)

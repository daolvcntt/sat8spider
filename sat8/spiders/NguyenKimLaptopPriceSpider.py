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

class NguyenKimLaptopPriceSpider(CrawlSpider):
    name = "product_link"
    allowed_domains = ["www.nguyenkim.com"]
    start_urls = ['http://www.nguyenkim.com/may-tinh-xach-tay/',]
    rules = (
        Rule (LinkExtractor(allow=('http://www.nguyenkim.com/index.php?dispatch=categories.load&category_id=527&next_page=[0-9]+&columns=4&get_more=y&features_hash=&items_per_page=20&sort_by=popularity&sort_order=desc')), callback='parse_item', follow= True),
    )

    images = [];

    def parse(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="ty-grid-list__image"]/a[1]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        link = response.url
        url_parts = urlparse(link)

        pil = ProductItemLoader(item = ProductPriceItem(), response = response)
        pil.add_xpath('title', '//*[@class="block_product-title"]/text()')
        pil.add_css('price', '.actual-price .price-num')
        pil.add_xpath('brand', '//*[@id="breadcrumbs_320"]/div/a[4]/text()')
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

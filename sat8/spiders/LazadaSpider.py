# -*- coding: utf-8 -*-
# Chua xong
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from AbstractPriceSpider import AbstractPriceSpider
from scrapy.selector import Selector

class LazadaSpider(AbstractPriceSpider):
    name = "product_link"
    allowed_domains = ["www.lazada.vn"]
    start_urls = [
        'http://www.lazada.vn/laptop/?page=2',
    ]
    rules = (
        Rule (LinkExtractor(allow=('http://www.lazada.vn/laptop/\?page=[0-9]+')), callback='parse_item', follow= True),
    )

    configs = {
        'product_links' : '//*[@class="cm-gallery-item cm-item-gallery"]/a/@href',
        'source' : 'banhangtructuyen.vn',
        'title' : '//*[@id="prod_title"]/text()',
        'price' : '//*[@id="special_price_box"]/text()'
    }

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.css('.product-card.new_.outofstock a').xpath('@href');

        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

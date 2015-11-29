# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader

from time import gmtime, strftime

class TgddLaptopSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = ["thegioididong.com"]
    start_urls = ['https://www.thegioididong.com/laptop?trang=1','https://www.thegioididong.com/may-tinh-bang?trang=1']
    rules = (
        Rule (LinkExtractor(allow=('laptop\?trang\=[0-9]+')), callback='parse_item', follow= True),
        Rule (LinkExtractor(allow=('may-tinh-bang\?trang\=[0-9]+')), callback='parse_item', follow= True),
    )

    images = [];

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@id="lstprods"]/li/a[1]/@href');

        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', '//*[@class="rowtop"]/h1//text()')
        pil.add_xpath('image', '//*[@class="boxright"]/aside[1]/img/@src')
        pil.add_xpath('spec', '//*[@class="parameter"]')
        # pil.add_xpath('images', '//*[@class="owl-item"]/div/a/img/@src')
        pil.add_xpath('price', '//*[@class="price_sale"]/strong[1]/text()');
        pil.add_xpath('brand', '//*[@class="breadcrumb"]/li[@class="brand"]/a/text()');

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath('//*[@id="characteristics"]/div/a/img/@data-src');

        dataImage = []
        image_urls = []

        for img in images:
            imgLink = response.urljoin(img.extract())
            image_urls.append(imgLink)

            imgLinkHash = hashlib.sha1(imgLink).hexdigest() + '.jpg'
            dataImage.append(imgLinkHash)

        product = pil.load_item()

        image_urls.append(pil.get_value(product['image']))

        # Price
        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        product['price']      = price
        product['link']       = response.url
        product['image_urls'] = image_urls
        product['image']      = hashlib.sha1(pil.get_value(product['image'])).hexdigest() + '.jpg'
        product['images']     = ',' . join(dataImage)
        product['hash_name']  = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['brand']      = pil.get_value(product['brand'])
        product['typ']        = 'product'
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        yield(product)

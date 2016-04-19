# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader

from time import gmtime, strftime

class ProductSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = ["cellphones.com.vn"]
    start_urls = ['http://cellphones.com.vn/mobile.html',]
    rules = (
        Rule (LinkExtractor(allow=('mobile\.html\?p\=[0-9]+'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item', follow= True),
    )

    images = [];

    def parse_item(self, response):
    	sel = Selector(response)
        product_links = sel.xpath('//*[@class="product-image"]/@href');
        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', '//*[@class="product-big-right"]/div[@class="product-name"]/h1/text()')
        pil.add_xpath('image', '//*[@id="image"]/@src')
        pil.add_css('spec', '.content-thongso > ul')
        pil.add_xpath('images', '//*[@class="more-views"]/ul[1]/li/a/@href')
        pil.add_xpath('price', '//*[@id="price"]//text()');

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath('//*[@class="more-views"]/ul[1]/li/a/@href');

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
        if 'price' not in product:
            product['price'] = '0'

        price = pil.get_value(product['price'].encode('utf-8'))
        price = re.sub('\D', '', price)

        product['price']      = price
        product['link']       = response.url
        product['image_urls'] = image_urls
        product['image']      = hashlib.sha1(pil.get_value(product['image'])).hexdigest() + '.jpg'
        product['images']     = ',' . join(dataImage)
        product['hash_name']  = hashlib.md5(pil.get_value(product['name']).encode('utf-8')).hexdigest()
        product['brand']      = (pil.get_value(product['name'])).split(" ")[0]
        product['typ']        = 'product'
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        yield(product)

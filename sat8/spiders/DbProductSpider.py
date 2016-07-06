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
    allowed_domains = []
    start_urls = []



    images = [];

    configs = [

        {
            "url" : "http://cellphones.com.vn/mobile.html?p=[0-9]+",
            "max_page" : 1,
            "is_mobile" : 1,
            "is_tablet" : 0,
            "is_laptop" : 0,

            "xpath_name" : '//*[@class="product-big-right"]/div[@class="product-name"]/h1/text()',
            "xpath_price" : '//*[@id="price"]//text()',
            "xpath_image" : '//*[@id="image"]/@src',
            "xpath_images" : '//*[@class="more-views"]/ul[1]/li/a/@href',
            "xpath_spec" : '//*[@class="content-thongso"]//ul[1]',
            "xpath_url_detail" : '//*[@class="product-image"]/@href'
        },
        {
            "url" : "http://cellphones.com.vn/tablet.html?p=[0-9]+",
            "max_page" : 1,
            "is_mobile" : 0,
            "is_tablet" : 1,
            "is_laptop" : 0,

            "xpath_name" : '//*[@class="product-big-right"]/div[@class="product-name"]/h1/text()',
            "xpath_price" : '//*[@id="price"]//text()',
            "xpath_image" : '//*[@id="image"]/@src',
            "xpath_images" : '//*[@class="more-views"]/ul[1]/li/a/@href',
            "xpath_spec" : '//*[@class="content-thongso"]//ul[1]',
            "xpath_url_detail" : '//*[@class="product-image"]/@href'
        }

    ]

    def parse_item(self, response):
        link = response.meta['link']

        sel = Selector(response)
        product_links = sel.xpath(link['xpath_url_detail']);
        for pl in product_links:
            url = response.urljoin(pl.extract());
            request = scrapy.Request(url, callback = self.parse_detail_content)
            request.meta['link'] = link;
            yield request

    def parse_detail_content(self, response):
        config = response.meta['link']

        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', config['xpath_name'])
        pil.add_xpath('image', config['xpath_image'])
        pil.add_xpath('spec', config['xpath_spec'])
        pil.add_xpath('price', config['xpath_price']);

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath(config['xpath_images']);

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
        product['is_laptop']  = config['is_laptop']
        product['is_tablet']  = config['is_tablet']
        product['is_mobile']  = config['is_mobile']
        product['created_at'] = strftime("%Y-%m-%d %H:%M:%S")
        product['updated_at'] = strftime("%Y-%m-%d %H:%M:%S")

        yield(product)


    def start_requests(self):
        configs = self.configs

        for config in configs:
            if(config['max_page'] > 0):
                for i in range(1, config['max_page']+1):
                    startLink = config["url"].replace('[0-9]+', str(i))

                    request = scrapy.Request(startLink, callback = self.parse_item)
                    request.meta['link'] = config
                    yield request
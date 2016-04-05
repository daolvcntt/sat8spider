# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from sat8.items import ProductItem, ProductItemLoader

from time import gmtime, strftime

import json,urllib

class FptProductSpider(CrawlSpider):
    name = "product_spider"
    allowed_domains = ["fptshop.com.vn"]
    start_urls = [
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=0&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=18&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=36&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=54&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=72&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=90&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
        'http://fptshop.com.vn/Ajax/FilterProduct/ViewMore?page=108&typeView=Hot&url=http://fptshop.com.vn/may-tinh-xach-tay?sl=ban-chay-nhat',
    ]
    rules = (

    )

    images = [];

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())

        sel = Selector(text=jsonresponse["content"])

        product_links = sel.xpath('//*[contains(@class, "fshop-lplap-item") and contains(@class, "col-xs-6")]//a[1]/@href');

        for pl in product_links:
            url = response.urljoin(pl.extract());
            yield scrapy.Request(url, callback = self.parse_detail_content)

    def parse_detail_content(self, response):
        pil = ProductItemLoader(item = ProductItem(), response = response)
        pil.add_xpath('name', '//*[@class="detail-top-left"]//h1[@class="detail-name"]//text()')
        pil.add_xpath('image', '//*[@class="detail-main-image left"]//img[@id="default_image"]/@src')
        pil.add_xpath('spec', '//*[@class="detail-main-specification"]')
        # pil.add_xpath('images', '//*[@class="owl-item"]/div/a/img/@src')
        pil.add_xpath('price', '//*[@class="detail-current-price"]/strong[1]//text()');
        pil.add_xpath('brand', '//*[@class="breadcrumb"]/li[3]/a/text()');

        # Ảnh chi tiết sản phẩm
        sel = Selector(response)
        images = sel.xpath('//*[@class="detail-thumbnail clearfix"]/a/img/@data-original');

        dataImage = []
        image_urls = []

        for img in images:
            imgLink = response.urljoin(img.extract())
            imgLink = imgLink.replace('Thumbs', 'Originals')

            # imgLink = 'http://fptshop.com.vn' + imgLink
            image_urls.append(imgLink)

            imgLinkHash = hashlib.sha1(imgLink).hexdigest() + '.jpg'
            dataImage.append(imgLinkHash)

        product = pil.load_item()

        product['image'] = 'http://fptshop.com.vn' + product['image']

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

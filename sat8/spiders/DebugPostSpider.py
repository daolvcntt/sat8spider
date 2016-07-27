# -*- coding: utf-8 -*-
import scrapy
import hashlib
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from sat8.items import BlogItem, PostItemLoader
from time import gmtime, strftime
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse

from PIL import Image

import urllib

from sat8.Helpers.Google_Bucket import *
from sat8.Helpers.Functions import *

from sat8.Functions import getImageFromContent
from sat8.Functions import makeGzFile

class DebugPostSpider(CrawlSpider):
    name = "blog_spider"
    allowed_domains = []
    start_urls = [
        'http://sohoa.vnexpress.net/danh-gia/dien-thoai/sony-xperia-z5-nhieu-cai-tien-nhung-thieu-diem-nhan-3309336.html'
    ]

    bucket = 'static.giaca.org'

    pathSaveImage = 'http://static.giaca.org/uploads/posts/'

    config_urls = [
        # {
        #     "url" : "http://news.zing.vn/cong-nghe/dien-thoai/trang[0-9]+.html",
        #     "max_page" : 10
        # }
    ]

    configs = {
        "links" : '//*[@class="list_news"]//h2[@class="title_news"]/a[1]/@href',
        'title' : '//*[@class="title_news"]/h1//text()',
        'teaser' : '//*[@class="short_intro txt_666"]//text()',
        'avatar' : '//*[@class="width_common space_bottom_20"]//img[1 or 2 or 3 or 4]/@src',
        'content' : '//*[@class="content_danhgia_chitiet"][1]',
        'category_value' : 'Đánh giá',
        'category_id' : 2,
        'type' : 'review'
    }

    def __init__(self, env="production"):
        self.env = env

    def parse(self, response):
        il = PostItemLoader(item = BlogItem(), response=response)
        il.add_value('link', response.url)
        il.add_xpath('title', self.configs['title'])
        il.add_xpath('teaser', self.configs['teaser'])
        il.add_xpath('avatar', self.configs['avatar'])

        il.add_value('category_id', 1)

        if 'category' in self.configs:
            il.add_xpath('category', self.configs['category']);
        else:
            if 'category_value' in self.configs:
                il.add_value('category', self.configs['category_value'].decode('utf-8'))

            if 'category_id' in self.configs:
                il.replace_value('category_id', self.configs['category_id'])

        il.add_xpath('content', self.configs['content'])

        il.add_value('product_id', 0)
        il.add_value('user_id', 1)

        il.add_value('created_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('updated_at', strftime("%Y-%m-%d %H:%M:%S"))
        il.add_value('post_type', self.configs['type'])

        item = il.load_item()



        item['typ'] = 'blog'

        if 'avatar' in item:
            avatar = item['avatar']
            item['avatar'] = hashlib.sha1(avatar).hexdigest() + '.jpg'

            self.processing_avatar_image(avatar)
        else:
            item['avatar'] = ''

        if 'content' in item:
            self.processing_content_image(response)

            # Replace something
            item['content'] = replace_link(item['content'])
            item['content'] = replace_image(item['content'], self.pathSaveImage)


        if self.env == 'dev':
            print item
            return

        yield item


    def processing_avatar_image(self, avatar):
        imageName = hashlib.sha1(avatar).hexdigest() + '.jpg'
        # Download image to host
        pathSaveImage = settings['IMAGES_STORE'] + '/full/' + imageName
        pathSaveImageSmall = settings['IMAGES_STORE'] + '/thumbs/small/' + imageName
        pathSaveImageBig   = settings['IMAGES_STORE'] + '/thumbs/big/' + imageName
        urllib.urlretrieve(avatar, pathSaveImage)

        # Resize image
        im = Image.open(pathSaveImage).convert('RGB')

        imageThumbs = settings['IMAGES_THUMBS']

        im.thumbnail(imageThumbs["small"])
        im.save(pathSaveImageSmall, 'JPEG')

        im = Image.open(pathSaveImage).convert('RGB')
        im.thumbnail(imageThumbs["big"])
        im.save(pathSaveImageBig, 'JPEG')

        # Make gz file
        makeGzFile(pathSaveImage)
        makeGzFile(pathSaveImageBig)
        makeGzFile(pathSaveImageSmall)

        # Upload to google bucket
        bucket = self.bucket
        google_bucket_upload_object(bucket, pathSaveImage, 'uploads/full/' + imageName)
        google_bucket_upload_object(bucket, pathSaveImageBig, 'uploads/thumbs/big/' + imageName)
        google_bucket_upload_object(bucket, pathSaveImageSmall, 'uploads/thumbs/small/' + imageName)

        google_bucket_upload_object(bucket, pathSaveImage + '.gz', 'uploads/full/' + imageName + '.gz')
        google_bucket_upload_object(bucket, pathSaveImageBig + '.gz', 'uploads/thumbs/big/' + imageName + '.gz')
        google_bucket_upload_object(bucket, pathSaveImageSmall + '.gz', 'uploads/thumbs/small/' + imageName + '.gz')

    def processing_content_image(self, response):
        selector = Selector(response)
        images = selector.xpath(self.configs['content'] + '//img/@src')

        for image in images:

            imgLink = response.urljoin(image.extract())

            print imgLink

            imageName = hashlib.sha1(imgLink.encode('utf-8')).hexdigest() + '.jpg'
            pathSaveImage = settings['IMAGES_STORE'] + '/posts/' + imageName

            # Download to tmp file
            urllib.urlretrieve(imgLink, pathSaveImage)

            # Upload to bucket
            google_bucket_upload_object(self.bucket, pathSaveImage, 'uploads/posts/' + imageName)

    # def parse_start_url(self, response):
    #     print '------------------------------', "\n"
    #     print response.url
    #     yield scrapy.Request(response.url, callback=self.parse_item)
    #     print '------------------------------', "\n\n"
    #

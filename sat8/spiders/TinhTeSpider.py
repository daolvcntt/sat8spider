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

class TinhTeSpider(CrawlSpider):
    name = "tinhte_spider"
    allowed_domains = []
    start_urls = []

    bucket = 'static.giaca.org'

    pathSaveImage = 'http://static.giaca.org/uploads/posts/'

    config_urls = [
        {
            "url" : "https://tinhte.vn/forums/ios-tin-tuc-danh-gia.118/page-[0-9]+",
            "max_page" : 2
        },
        # {
        #     "url" : "https://tinhte.vn/forums/android-tin-tuc-danh-gia.151/page-[0-9]+",
        #     "max_page" : 5
        # },
        # {
        #     "url" : "https://tinhte.vn/forums/wp-tin-tuc-danh-gia.11/page-[0-9]+",
        #     "max_page" : 5
        # },
        # {
        #     "url" : "https://tinhte.vn/forums/bb-tin-tuc-danh-gia.99/page-[0-9]+",
        #     "max_page": 5
        # },
        # {
        #     "url" : "https://tinhte.vn/forums/win-tin-tuc-danh-gia.23/page-[0-9]+",
        #     "max_page": 5
        # },
        # {
        #     "url" : "https://tinhte.vn/forums/mac-tin-tuc-danh-gia.196/page-[0-9]+",
        #     "max_page": 5
        # },
        # {
        #     "url": "https://tinhte.vn/forums/may-tinh-linux.79/page-[0-9]+",
        #     "max_page": 5
        # },
        # {
        #     "url": "https://tinhte.vn/forums/may-tinh-chrome-os.402/page-[0-9]+",
        #     "max_page": 5
        # },
        # {
        #     "url": "https://tinhte.vn/forums/tin-tuc.71/page-[0-9]+",
        #     "max_page": 5
        # },
        # {
        #     "url": "https://tinhte.vn/forums/danh-gia.660/page-[0-9]+",
        #     "max_page": 5
        # }
    ]

    configs = {
        "links" : '//*[@class="discussionListItems"]//a[@class="PreviewTooltip"]/@href',
        'title' : '//*[@class="titleBar"]/h1//text()',
        'teaser' : '//*[@class="titleBar"]/h1//text()',
        'avatar' : '//*[@class="messageInfo primaryContent"]//img[1]/@src',
        'content' : '//*[@class="messageInfo primaryContent"]/div[@class="messageContent"]/article',
        'category_value' : 'Tinh tế',
        'category_id' : 8,
        'type' : 'post'
    }

    def __init__(self, env="production"):
        self.env = env
        # Add start_urls
        config_urls = self.config_urls
        for url in config_urls:
            if url["max_page"] > 0:
                for i in range(1, url["max_page"]):
                    self.start_urls.append(url["url"].replace('[0-9]+', str(i)))
            else:
                self.start_urls.append(url["url"])

    def parse(self, response):
        sel = Selector(response)

        blog_links = sel.xpath(self.configs['links'])

        for href in blog_links:
            url = response.urljoin(href.extract());
            request = scrapy.Request(url, callback = self.parse_detail_content)
            request.meta['tinhte_category_link'] = response.url
            yield request


    def parse_detail_content(self, response):

        sel = Selector(response)

        il = PostItemLoader(item = BlogItem(), response=response)
        il.add_value('link', response.url)
        il.add_value('link', response.url)
        il.add_xpath('title', self.configs['title'])
        il.add_xpath('teaser', self.configs['teaser'])
        il.add_xpath('avatar', self.configs['avatar'])
        il.add_value('tinhte_category_link', response.meta['tinhte_category_link'])
        il.add_value('is_tinhte', 1)

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

            if avatar == 'styles/default/xenforo/clear.png':
                avatar = 'https://tinhte.vn/styles/default/xenforo/clear.png'

            self.processing_avatar_image(avatar)

            item['avatar'] = sha1FileName(avatar)
        else:
            item['avatar'] = ''

        if 'content' in item:
            self.processing_content_image(response)

            # Replace something
            item['content'] = replace_link(item['content'])
            item['content'] = replace_image(item['content'], self.pathSaveImage)

        # Bình luận của thành viên
        commentNodes = sel.xpath('//*[contains(@class, "sectionMain message")]')
        comments = []
        image_links = []

        for commentNode in commentNodes:
            # print commentNode
            avatar  = commentNode.xpath('.//div[@class="messageUserInfo"]//a[contains(@class, "avatar")]/img/@src').extract()
            user    = commentNode.xpath('.//div[@class="messageUserInfo"]//a[@class="username"]/text()').extract()
            comment = commentNode.xpath('.//div[@class="messageInfo primaryContent"]').extract()

            user    = user[0]
            avatar  = getUrlWithoutParams(avatar[0])
            comment = comment[0]

            comment = comment.replace("styles/default/xenforo/clear.png", "https://tinhte.vn/styles/default/xenforo/clear.png")

            self.process_comment(comment, response)

            comment = replace_image(comment, self.pathSaveImage)

            a = {
                "avatar" : avatar,
                "avatar_hash" : sha1FileName(getUrlWithoutParams(avatar)),
                "user": user,
                "comment" : comment
            }

            comments.append(a)

            image_links.append(a['avatar'])


        yield {
            "post" : item,
            "comments": comments,
            "image_links": image_links
        }


    def processing_avatar_image(self, avatar):
        imageName = sha1FileName(avatar)
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

            imageName = sha1FileName(imgLink)
            pathSaveImage = settings['IMAGES_STORE'] + '/posts/' + imageName

            # Download to tmp file
            urllib.urlretrieve(imgLink, pathSaveImage)

            # Upload to bucket
            google_bucket_upload_object(self.bucket, pathSaveImage, 'uploads/posts/' + imageName)


    def process_comment(self, comment, response):
        selector = Selector(text=comment)
        images = selector.xpath('//img/@src')

        for image in images:

            imgLink = response.urljoin(image.extract())
            # imgLink = imgLink[0]

            print imgLink

            imageName = sha1FileName(imgLink)
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

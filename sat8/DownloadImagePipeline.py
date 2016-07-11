# -*- coding: utf-8 -*-

import hashlib
import urllib
from scrapy.selector import Selector
from scrapy.conf import settings

from sat8.Helpers.Functions import *
from sat8.Helpers.Google_Bucket import *

class DownloadImagePipeline(object):

    def process_item(self, item, spider):

        if 'image_links' in item:
            for image_url in item['image_links']:

                ext = getExtension(image_url)
                imageName = hashlib.sha1(image_url).hexdigest() + '.' + ext

                # Download to local
                thumbs = downloadImageFromUrl(image_url)

                # Upload bucket
                google_bucket_upload_object('static.giaca.org', thumbs['full'], 'uploads/full/' + imageName)
                google_bucket_upload_object('static.giaca.org', thumbs['big'], 'uploads/thumbs/big/' + imageName)
                google_bucket_upload_object('static.giaca.org', thumbs['small'], 'uploads/thumbs/small/' + imageName)

            return item
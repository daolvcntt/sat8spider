# -*- coding: utf-8 -*-

import hashlib
import urllib
from scrapy.selector import Selector
from scrapy.conf import settings

from sat8.Helpers.Functions import *
# from sat8.Helpers.Google_Bucket import *

from sat8.Functions import makeGzFile

class DownloadImagePipeline(object):

    def process_item(self, item, spider):

        if 'image_links' in item:
            for image_url in item['image_links']:

                # ext = getExtension(image_url)

                # try:
                #     imageName = hashlib.sha1(image_url).hexdigest() + '.' + ext
                # except UnicodeEncodeError, e:
                #     imageName = hashlib.sha1(image_url.encode('utf-8')).hexdigest() + '.' + ext

                imageName = sha1FileName(image_url)

                # Download to local
                try:
                    thumbs = downloadImageFromUrl(image_url)

                    # Make gz file
                    makeGzFile(thumbs['full'])
                    makeGzFile(thumbs['big'])
                    makeGzFile(thumbs['small'])

                    # Upload bucket
                    # google_bucket_upload_object('static.giaca.org', thumbs['full'], 'uploads/full/' + imageName)
                    # google_bucket_upload_object('static.giaca.org', thumbs['big'], 'uploads/thumbs/big/' + imageName)
                    # google_bucket_upload_object('static.giaca.org', thumbs['small'], 'uploads/thumbs/small/' + imageName)
                except IOError as e:
                    print image_url
                    # raise e


            return item
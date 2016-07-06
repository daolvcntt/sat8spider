import unittest
import sys
import scrapy

import socket
hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider/sat8/Helpers")
else:
    sys.path.insert(0, "/var/www/html/sat8spider/sat8/Helpers")

from Functions import *
from Google_Bucket import *

class GoogleBucketTest(unittest.TestCase):

    def test_upload_object(self):
        bucket = 'static.giaca.org'
        filename = '/var/www/html/sat8spider/90.jpg'
        response = google_bucket_upload_object(bucket, filename, 'Girls/90.jpg')
        self.assertEqual("Girls/90.jpg", response["name"])

        # filename = 'http://p.vatgia.vn/raovat_pictures/1/gxq1347940471.jpg'
        # response = google_bucket_upload_object(bucket, filename)
        # self.assertEqual("gxq1347940471.jpg", response["name"])

if __name__ == '__main__':
    unittest.main()
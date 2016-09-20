import sys

import socket
import os

hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

from sat8.Functions import *
from sat8.Helpers.Functions import *

from scrapy.conf import settings

import hashlib
import unittest
import datetime
import time


class FunctionTest(unittest.TestCase):

    def test_parseJson4Params(self):
        string = "name:cong\nage:20"
        a = parseJson4Params(string);
        rs = {"name": "cong", "age": "20"}
        self.assertEqual(a, rs)

    def test_get_file_name(self):
        expected = 'girl.jpg'
        actual = get_file_name('http://shit.com/girl.jpg')
        self.assertEqual(expected, actual)

    def test_get_mime_type(self):
        path = 'http://static.giaca.org/Girls/90.jpg'
        expected = 'image/jpeg'
        actual = get_mime_type(path)
        self.assertEqual(expected, actual)

    # def test_file_get_contents(self):
        # path = 'http://static.giaca.org/Girls/90.jpg'
        # fo = open(path)
        # content = fo.read()

        # expected = content

        # actual = file_get_contents(path)

        # self.assertEqual(expected, actual)

    def test_replace_link(self):
        expected = '<span>shit</span>'
        actual = replace_link('<a href="http://google.com"><span>shit</span></a>')
        self.assertEqual(expected, actual)

    def test_replace_image(self):
        imgLink = 'http://google.com/sexy.jpg'
        content = '<p><img src="'+ imgLink +'" /></p>'

        expected = '<p><img src="http://static.giaca.org/uploads/full/' + sha1FileName(imgLink) + '" /></p>'
        actual = replace_image(content, 'http://static.giaca.org/uploads/full/')

        self.assertEqual(expected, actual)

    def test_getExtension(self):
        expected = 'jpeg';
        actual = getExtension('http://google.com/sexy.jpg');

        self.assertEqual(expected, actual);

    def test_downloadImageFromUrl(self):
        imgLink = 'http://cellphones.com.vn/media/catalog/product/cache/1/image/180x350/9df78eab33525d08d6e5fb8d27136e95/s/7/s7-edge-gold_1.png';
        ext = getExtension(imgLink);
        imageName = hashlib.sha1(imgLink).hexdigest() + '.' + ext;

        pathSaveImage = settings['IMAGES_STORE'] + '/full/' + imageName
        pathSaveImageSmall = settings['IMAGES_STORE'] + '/thumbs/small/' + imageName
        pathSaveImageBig   = settings['IMAGES_STORE'] + '/thumbs/big/' + imageName

        expected = {
            "full" : pathSaveImage,
            "big" : pathSaveImageBig,
            "small" : pathSaveImageSmall
        }

        actual = downloadImageFromUrl(imgLink, 1)

        self.assertEqual(expected, actual)
        self.assertEqual(os.path.isfile(pathSaveImage), True)
        self.assertEqual(os.path.isfile(pathSaveImageSmall), True)
        self.assertEqual(os.path.isfile(pathSaveImageBig), True)

    def test_sha1(self):
        string = 'luongvancong'
        expected = hashlib.sha1(string.encode('utf-8')).hexdigest()
        actual = sha1(string)

        self.assertEqual(expected, actual)

    def test_sha1FileName(self):
        fileName = 'sexy.jpg'
        expected = sha1(fileName) + '.' + getExtension(fileName)
        actual = sha1FileName(fileName)

        self.assertEqual(expected, actual)

    def test_getUrlWithoutParams(self):
        url = 'http://abc.com/1.jpg?121212'
        expected = 'http://abc.com/1.jpg'
        actual = getUrlWithoutParams(url)

        self.assertEqual(expected, actual)

    def test_getVGProductId(self):
        url = 'http://vatgia.com/438/2415665/apple-iphone-3g-s-3gs-8gb-black-b%E1%BA%A3n-qu%E1%BB%91c-t%E1%BA%BF-2012.html';
        expected = 2415665
        actual = getVGProductId(url)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
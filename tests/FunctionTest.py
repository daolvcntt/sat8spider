import sys

import socket
hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

from sat8.Functions import *
from sat8.Helpers.Functions import *

import hashlib
import unittest


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

        expected = '<p><img src="http://static.giaca.org/uploads/full/' + hashlib.sha1(imgLink).hexdigest() + '.jpg" /></p>'
        actual = replace_image(content, 'http://static.giaca.org/uploads/full/')

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
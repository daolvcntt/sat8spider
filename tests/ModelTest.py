import socket
import sys

hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

import unittest
from sat8.Databases.Model import Model

class Post(Model):
    table = 'tests'
    primaryKey = 'id'

class ModelTest(unittest.TestCase):

    def setUp(self):
        self.post = Post()

    def test_01_insert(self):
        self.post.truncate()
        expected = 1
        actual = self.post.insert({"name" : "Cong", "age" : 20})
        self.assertEquals(expected, actual)

    def test_02_getById(self):
        expected = dict
        actual = self.post.getById(1)

        self.assertIsInstance(actual, expected)

    def test_03_all(self):
        expected = list
        actual = self.post.all()
        self.assertIsInstance(actual, expected)

    def test_04_delete(self):
        expected = 1
        actual = self.post.delete(1)
        self.assertEquals(expected, actual)


if __name__ == '__main__':
    unittest.main()
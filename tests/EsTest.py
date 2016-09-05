import socket
import sys
from time import gmtime, strftime

hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

import unittest
from sat8.Elasticsearch.ES import ES

created_at = strftime("%Y-%m-%d 00:00:00")
created_at_str = str(created_at)

class EsTest(unittest.TestCase):

    def setUp(self):
        self.es = ES()
        self.es.setIndex('nht-test')

    def test_get(self):
        self.assertEquals('null', self.es.get('posts', 9999999999999999));

    def test_insertOrUpdate(self):
        document = {"title" : "shit"}
        self.es.setDocType('unitests')
        self.assertEquals(document, self.es.insertOrUpdate(202, document))



if __name__ == '__main__':
    unittest.main()
import socket
import sys
from time import gmtime, strftime

hostname = socket.gethostname()

if hostname == 'justin-HP-ProBook-450-G0':
    sys.path.insert(0, "/home/justin/public_html/sat8spider")
else:
    sys.path.insert(0, "/var/www/html/sat8spider")

import unittest
from sat8.Databases.DB import DB

created_at = strftime("%Y-%m-%d 00:00:00")
created_at_str = str(created_at)

class DbTest(unittest.TestCase):

    def setUp(self):
        self.db = DB()

        self.dataInsert = {
            "age" : 20,
            "name" : 'Cong',
            "created_at" : created_at
        }

        self.dataUpdate = {
            "name" : "Cong_Edit",
            "age" : 27
        }

    def test_01_getInsertQuery(self):
        data = self.dataInsert
        expected = "INSERT INTO persons(created_at,age,name) VALUES('"+ created_at_str +"','20','Cong')"
        actual = self.db.getInsertQuery('persons', data)

        self.assertEquals(expected, actual)


    def test_02_insert(self):
        self.db.truncate('tests')
        data = self.dataInsert
        expected = 1
        actual = self.db.insert('tests', data)

        self.assertEquals(expected, actual)

    def test_03_first(self):
        actual = self.db.first('tests', 'id', 1)

        self.assertIn('id', actual)
        self.assertIn('name', actual)
        self.assertIn('age', actual)
        self.assertEquals(1, actual['id'])
        self.assertIsInstance(actual, dict)

    def test_04_all(self):
        actual = self.db.all('tests')
        expected = list
        self.assertIsInstance(actual, expected)

    def test_05_getQueryUpdate(self):
        expected = "UPDATE tests SET age='27', name='Cong_Edit' WHERE id='1'"
        actual = self.db.getUpdateQuery('tests', self.dataUpdate, {"id" : 1})
        self.assertEquals(expected, actual)

    def test_06_update(self):
        expected = 1
        actual = self.db.update('tests', self.dataUpdate, {"id" : 1})

        self.assertEquals(expected, actual)

    def test_07_getDeleteQuery(self):
        expected = "DELETE FROM tests WHERE id='1'"
        actual = self.db.getDeleteQuery('tests', {"id" : 1})
        self.assertEquals(expected, actual)

    def test_08_selectRawFetchOne(self):
        expected = 1;
        actual = self.db.selectRawFetchOne("SELECT * FROM tests WHERE id = 1")
        self.assertEquals(expected, actual['id'])

    def test_09_selectRawFetchAll(self):
        expected = list
        actual = self.db.selectRawFetchAll("SELECT * FROM tests WHERE id > 0")
        self.assertIsInstance(actual, expected)

    def test_10_delete(self):
        expected = 1
        actual = self.db.delete('tests', {"id" : 1})
        self.assertEquals(expected, actual)


if __name__ == '__main__':
    unittest.main()
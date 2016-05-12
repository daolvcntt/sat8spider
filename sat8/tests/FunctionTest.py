import sys

sys.path.insert(0, "/home/justin/public_html/sat8spider")

from sat8.Functions import parseJson4Params

import unittest


class FunctionTest(unittest.TestCase):

    def test_parseJson4Params(self):
        string = "name:cong\nage:20"
        a = parseJson4Params(string);
        rs = {"name": "cong", "age": "20"}
        self.assertEqual(a, rs)

if __name__ == '__main__':
    unittest.main()
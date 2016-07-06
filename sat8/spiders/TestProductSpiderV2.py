# -*- coding: utf-8 -*-

from ProductSpiderV2 import ProductSpiderV2

class TestProductSpiderV2(ProductSpiderV2):

    env = 'testing'

    def parse_detail_content(self, response):
        print self.get_product(response)

    def parseJsonDetailContent(self, response):
        print self.getProductJson(response)

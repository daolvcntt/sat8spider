# -*- coding: utf-8 -*-

from ProductSpiderV2 import ProductSpiderV2

class QuickRunProductSpiderV2(ProductSpiderV2):

    env = 'quick'

    def parse_detail_content(self, response):
        yield self.get_product(response)

    def parseJsonDetailContent(self, response):
        yield self.getProductJson(response)

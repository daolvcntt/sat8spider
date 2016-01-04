from sat8.Elasticsearch.ES import ES

class ProductPriceES(ES):

	doc_type = 'prices'

	index = 'nht-test'

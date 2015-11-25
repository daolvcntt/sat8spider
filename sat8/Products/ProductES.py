from sat8.Elasticsearch.ES import ES

class ProductES(ES):

	doc_type = 'products'

	index = 'nht-test'

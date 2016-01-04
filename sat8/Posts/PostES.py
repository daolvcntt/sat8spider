from sat8.Elasticsearch.ES import ES

class PostES(ES):

	doc_type = 'posts'

	index = 'nht-test'

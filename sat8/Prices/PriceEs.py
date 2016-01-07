from sat8.Elasticsearch.ES import ES

class PriceES(ES):

    doc_type = 'prices'

    index = 'nht-test'

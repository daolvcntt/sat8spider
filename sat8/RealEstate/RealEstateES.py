from sat8.Elasticsearch.ES import ES

class RealEstateES(ES):

    doc_type = 'real_estate'

    index = 'nht-test'

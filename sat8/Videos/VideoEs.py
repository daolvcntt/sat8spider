from sat8.Elasticsearch.ES import ES

class VideoEs(ES):

    doc_type = 'videos'

    index = 'nht-test'

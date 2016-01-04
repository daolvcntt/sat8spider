from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'], timeout=20)

from elasticsearch_dsl import Mapping, String, Nested, Integer

# name your type
m = Mapping('prices')

# add fields
m.field('price', Integer())
m.save('nht-test')

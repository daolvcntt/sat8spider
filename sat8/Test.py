import sys
import os

path = os.path.dirname(os.path.realpath(__file__ + '../..'))
sys.path.append(path)

from Helpers import Functions

from Posts.PostES import PostES
from Products.DbProduct import DbProduct


# print sys.path

# Test class db

p = PostES()
print p.count('posts')


# print es.get('posts', 5)


# for i in post:
# 	print post[i]

# # print es.count('posts')

# print es.insertOrUpdate(1, post)
# print es.get('posts', 1)['title']

# print es.update(2, post)
# print es.get('posts', 2)


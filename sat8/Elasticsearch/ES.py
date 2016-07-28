# coding: utf-8
# Phải có dòng trên nếu muốn comment = tiếng việt
#
from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError
from elasticsearch import TransportError
import json

class ES():

	def __init__(self):
		self.es = Elasticsearch()

	def setIndex(self, index):
		self.index = index

	def getIndex(self):
		return self.index

	def setDocType(self, doc_type):
		self.doc_type = doc_type

	def getDocType(self):
		return self.doc_type

	# Thêm tài liệu
	# Chưa có thì thêm mới, có rồi thì update
	# @params id
	# @params doucument
	#
	# @return document
	def insertOrUpdate(self, id, document):
		index = self.getIndex()
		doc_type = self.getDocType()

		exist = self.get(doc_type, id)

		if exist != 'null':
			result = self.update(id, document)
		else:
			result = self.es.index(index=index, doc_type=doc_type, id=id, body=document)

		return document

	# Cập nhật tài liệu
	def update(self, id, document):
		index = self.getIndex()
		doc_type = self.getDocType()
		return self.es.update(index=index, doc_type=doc_type, id=id, body={"doc" : document})

	# Lấy tài liệu
	def get(self, doc_type, id):
		index = self.getIndex()
		try:
			document = self.es.get(index = index, doc_type = doc_type, id = id)
			return document['_source']
		except NotFoundError, e:
			return 'null'
		except TransportError, e:
			return 'null'

	# Delete tài liệu
	def delete(self, doc_type, id):
		index = self.getIndex()
		return self.es.delete(index, doc_type = doc_type, id = id)

	def count(self, doc_type):
		index = self.getIndex()
		count = self.es.count(index, doc_type)
		return count['count']




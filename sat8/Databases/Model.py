import sat8.settings
from sat8.Databases.DB import DB

class Model():

	table = ''
	primaryKey = ''

	attributes = {}

	def __init__(self, attributes = {}):
		self.db = DB()

	def fill(self, attributes):
		self.attributes = attributes
		return self

	def getAttributes(self):
		return self.attributes

	def setTable(self, table):
		self.table = table

	def getTable(self):
		return self.table

	def setPrimaryKey(self, key):
		self.primaryKey = key

	def getPrimaryKey(self):
		return self.primaryKey

	def getById(self, id, fields = '*'):
		return self.db.first(self.getTable(), self.getPrimaryKey(), id, fields)

	def delete(self, id):
		return self.db.delete(self.getTable(), {self.getPrimaryKey() : id});

	def insert(self, data):
		return self.db.insert(self.getTable(), data)

	def update(self, data, where):
		return self.db.update(self.getTable(), data, where)

	def truncate(self):
		return self.db.truncate(self.getTable())

	def all(self):
		return self.db.all(self.getTable())

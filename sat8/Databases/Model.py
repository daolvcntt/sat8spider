import sat8.settings
from sat8.Databases.DB import DB

class Model(DB):

	table = ''
	primaryKey = ''

	def setTable(self, table):
		self.table = table

	def getTable(self):
		return self.table

	def setPrimaryKey(self, key):
		self.primaryKey = key

	def getPrimaryKey(self):
		return self.primaryKey

	def getById(self, id, fields = '*'):
		query = "SELECT %s" %fields +  " FROM " + self.getTable() + " WHERE "  + self.getPrimaryKey() +  "=%d" %id
		self.cursor.execute(query)
		return self.cursor.fetchone()

	def delete(self, id):
		query = "DELETE FROM " + self.getTable() + " WHERE " + self.getPrimaryKey() + "=%d" %id
		self.cursor.execute(query)
		self.conn.commit()
		return self.cursor.rowcount

	def insert(self, data):
		return DB.insert(self, self.getTable(), data)

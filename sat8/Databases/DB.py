from sat8 import settings

class DB():

	def __init__(self):
		self.conn = settings.MYSQL_CONN
		self.cursor = self.conn.cursor()

	def getInsertQuery(self, table, data):
		queryStr = "INSERT INTO %s" %table + "("
		queryValue = "VALUES(";

		for i in data:
			queryStr += i + ","
			queryValue += "'" + str(data[i]) + "'" + ","


		queryValue = queryValue[:-1] + ")"
		queryStr = queryStr[:-1] + ") "

		queryStr = queryStr + queryValue

		return queryStr

	def insert(self, table, data):
		queryStr = self.getInsertQuery(table, data)
		self.cursor.execute(queryStr, (data))
		self.conn.commit()

		return self.cursor.lastrowid

	def getUpdateQuery(self, table, data, where):
		queryStr = "UPDATE " + str(table)

		setStr = " SET "
		whereStr = " WHERE "

		# Set conditions
		temp = ""
		for i in data:
			temp += str(i) + "=" + "'" + str(data[i]) + "', "

		setStr += temp[:-2]

		# Where conditions
		temp = ""
		for j in where:
			temp += str(j) + "=" + "'" + str(where[j]) + "' AND "

		whereStr += temp[:-5]

		queryStr = queryStr + setStr + whereStr

		return queryStr

	def update(self, table, data, where):
		queryStr = self.getUpdateQuery(table, data, where)
		self.cursor.execute(queryStr)
		self.conn.commit()

		return self.cursor.rowcount


	def truncate(self, table):
		queryStr = "TRUNCATE TABLE " + table
		self.cursor.execute(queryStr)
		self.conn.commit()

		return self.cursor.rowcount

	def first(self, table, primaryKey, value, fields = '*'):
		queryStr = "SELECT "+ str(fields) +" FROM " + table + " WHERE " + primaryKey + "=" + str(value)
		self.cursor.execute(queryStr)
		return self.cursor.fetchone()

	def all(self, table, fields = '*'):
		queryStr = "SELECT "+ str(fields) +" FROM " + table
		self.cursor.execute(queryStr)
		return self.cursor.fetchall()

	def getDeleteQuery(self, table, where):
		queryStr = "DELETE FROM " + str(table)
		whereStr = " WHERE "
		# Where conditions
		temp = ""
		for j in where:
			temp += str(j) + "=" + "'" + str(where[j]) + "' AND "

		whereStr += temp[:-5]

		queryStr += whereStr

		return queryStr

	def delete(self, table, where):
		queryStr = self.getDeleteQuery(table, where)
		self.cursor.execute(queryStr)
		self.conn.commit()

		return self.cursor.rowcount



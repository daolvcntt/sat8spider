from sat8 import settings

class DB():

	def __init__(self):
		self.conn = settings.MYSQL_CONN
		self.cursor = self.conn.cursor()

	def insert(self, table, data):
		queryStr = "INSERT INTO %s" %table + "("
		queryValue = "VALUES(";

		params = []
		for i in data:
			queryStr += i + ","
			queryValue += "'" + data[i] + "',"
			# queryValue += "%s,"


		params = params[:-1]
		queryValue = queryValue[:-1] + ")"
		queryStr = queryStr[:-1] + ") "

		queryStr = queryStr + queryValue

		self.cursor.execute(queryStr, (data))
		self.conn.commit()

		return self.cursor.lastrowid

	def update(self, table, data, where):

		return 'shit'

	def raw(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchall()


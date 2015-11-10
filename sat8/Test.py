import settings

# print settings.MYSQL_SERVER
# print settings.MYSQL_DB

class Connection:

	def conn(self):

		print settings.MYSQL_DB

a = Connection()
a.conn()
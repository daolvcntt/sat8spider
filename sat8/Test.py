# SQL DATABASE SETTING
MYSQL_SERVER = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'search'

# connect to the MySQL server
try:
	MYSQL_CONN = pymysql.connect(host=MYSQL_SERVER,
										port=MYSQL_PORT,
										user=MYSQL_USER,
										password=MYSQL_PASSWORD,
										db=MYSQL_DB,
										charset='utf8',
										cursorclass=pymysql.cursors.DictCursor,
										use_unicode=True)
except pymysql.Error, e:
	logging.error("Error %d: %s" % (e.args[0], e.args[1]))
	sys.exit(1)

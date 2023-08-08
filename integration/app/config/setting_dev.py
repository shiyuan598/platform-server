# coding=utf8
# MySQL配置
MYSQL_HOST = '172.16.12.84'
MYSQL_PORT = '3307'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'integration'
# dialect+driver://username:password@host:port/database
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=MYSQL_USER,password=MYSQL_PASSWD,host=MYSQL_HOST,port=MYSQL_PORT,db=MYSQL_DB)
# 短信通知
SMS_ENABLE = False
# 项目配置
DEBUG = False
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True  #开启慢查询
FLASKY_DB_QUERY_TIMEOUT = 0.05  #数据库查询时间的门限值
SQLALCHEMY_ECHO = False
JSON_AS_ASCII = False
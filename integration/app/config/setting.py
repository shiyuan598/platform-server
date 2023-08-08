# coding=utf8
# MySQL配置
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3307'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'
MYSQL_DB = 'integration'
# dialect+driver://username:password@host:port/database
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=MYSQL_USER,password=MYSQL_PASSWD,host=MYSQL_HOST,port=MYSQL_PORT,db=MYSQL_DB)
# artifactory配置
ARTIFACTS = {
    "url": "https://artifactory.zhito.com/artifactory",
    "username": "wangshiyuan",
    "api_key": "AKCp8nzqQaRKVZGfYHimkQh9FK3FHq2mkaaRtgJZhjaeYL71aUXU3RTJbFBjNTT9CqNoMTdru"
}
# confluence配置
CONFLUENCE = {
    "url": "https://confluence.zhito.com:8090",
    "username": "wangshiyuan",
    "password": "zhito26@#",
    "space": "ITD",
    "parent_page_id": 56111727,
    "parent_page_id_app": 56114852,
    "parent_page_id_api": 56114855
}
# gitlab配置
GITLAB = {
    "url": "https://gitlab.zhito.com",
    "token": "7c5ohyqs1pzL6873cxjd"
}
# jenkins配置
JENKINS = {
    "jenkins_server_url": "https://jenkins.zhito.com",
    "user_id": "wangshiyuan",
    "api_token": "11bdffee022bd22472efdf2ebd99354522"
}
# Redis配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6378
# 短信通知
SMS_ENABLE = False
# 项目配置
DEBUG = False
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True  #开启慢查询
FLASKY_DB_QUERY_TIMEOUT = 0.5  #数据库查询时间的门限值
SQLALCHEMY_ECHO = False
JSON_AS_ASCII = False
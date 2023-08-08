1.修改配置
config/setting.py 中数据库的配置
gun.conf 中IP端口配置

2.拷贝文件到服务器
sudo scp -r build/ zhito@172.16.18.223:/home/zhito/integration/server

3.启动命令
nohup gunicorn -c gunicorn.conf app:app &


启动Redis：
redis-server --daemonize yes --port 6378  #后台运行, 指定端口

Redis配置文件位于/etc/redis/redis.conf

客户端连接：
redis-cli -h 127.0.0.1 -p 6378
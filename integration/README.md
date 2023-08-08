#### 说明
软件集成平台后端服务
##### 开发
1.虚拟环境
创建
```bash
python3.10 -m venv venv_dir

```
激活
```bash
source venv_dir/bin/activate

```
2.安装依赖
```bash
pip3 install -r requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple
```
设置镜像源：--index https://pypi.tuna.tsinghua.edu.cn/simple
安装短信SDK：
pip3 install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python tencentcloud-sdk-python-sms

参考：腾讯云短信服务SDK[地址(https://cloud.tencent.com/document/product/382)]
腾讯云账户管理[地址(https://console.cloud.tencent.com/smsv2)]
腾讯云密钥管理[地址(https://console.cloud.tencent.com/cam/capi)]


导出requirements: 
```
python3.10 -m pip freeze > requirements.txt


3.启动
开发环境
```bash
python3.10 app.py
```
生产环境使用gunicorn
```bash
nohup gunicorn -c gunicorn.conf app:app > log_info.log 0<&1 2>&1 &
```

3.迁移
3.1安装
```
pip3 install flask-migrate --index https://pypi.tuna.tsinghua.edu.cn/simple
```
3.2初始化Migrate
from flask_migrate import Migrate
...
# 数据迁移
migrate = Migrate(app, db)

3.3初始化数据库
```bash
flask db init 
```
或 python3.10 -m flask db init

3.4在项目根目录中执行以下命令创建迁移脚本
```bash
python3.10 -m flask db migrate -m "add num field to Project table" 
```

3.5在项目根目录中执行以下命令将迁移脚本应用到数据库中
```bash
python3.10 -m flask db upgrade
```

注意数据库中
alembic_version的版本号，可以根据需要设置最后的版本以便能执行更新

字符错误时执行以下内容：
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

##### 文档
1.python-gitlab: https://python-gitlab.readthedocs.io/en/stable/gl_objects/branches.html
2.python-jenkins: https://python-jenkins.readthedocs.io/en/latest/api.html#jenkins.Jenkins.get_queue_item
3.confluence: https://docs.atlassian.com/ConfluenceServer/rest/7.8.1/#api/content-createContent

1.artifactory api key
user - set me up - configure [password] - resolve
2.jenkins api token
user - 设置 - api token
3.gitlab token
user - preferences - access tokens

##### rest url
https://jira.zhito.com:8080/rest/api/2/issue/GSL3P-2986
https://confluence.zhito.com:8090/rest/api/space/JSZSZX
https://gitlab.zhito.com/api/v4/projects
https://artifactory.zhito.com/artifactory/api/repositories
https://jenkins.zhito.com/api/

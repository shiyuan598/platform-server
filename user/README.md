# 用户管理后端

### 启动
```
node app.js
```
注：node v14.20.0


### 构建
```
ncc build app.js -m -o dist
```
需要@vercel/ncc 包
```
npm install -g @vercel/ncc
```

### 数据库迁移
使用knex.js，适用小型项目，无需ORM
安装：npm i knex mysql2
1.创建配置文件knexfile.js
2.创建迁移文件 --knexfile指定配置文件
```
npx knex migrate:make add_sex_to_user
```
3.手动编辑迁移文件中的up/down函数
4.执行迁移 执行所有未执行的迁移
```
npx knex migrate:latest
```
5.回滚迁移 回滚最后一次的迁移，可多次执行，参数：--all --to
```
npx knex migrate:rollback
```


### 文档
mysql2:
https://www.npmjs.com/package/mysql2

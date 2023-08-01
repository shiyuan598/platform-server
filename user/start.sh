#!/bin/bash
# 设置环境变量为 production
export NODE_ENV=production

# 执行数据库迁移
npx knex migrate:latest

# 启动应用程序
nohup node weread.js &

# 生成pid文件
echo $! > pid.txt
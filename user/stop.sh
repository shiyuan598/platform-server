#!/bin/bash

# 从 pid.txt 文件中读取之前保存的进程 PID
pid=$(cat pid.txt)

# 检查是否存在该进程，如果存在则结束进程
if ps -p $pid > /dev/null; then
    echo "Stopping the process with PID $pid"
    kill $pid
else
    echo "Process with PID $pid not found."
fi

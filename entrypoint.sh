#!/bin/bash

# 把所有环境变量写入 /etc/environment，让 cron 任务可以读取
printenv | sed 's/^\(.*\)$/export \1/g' > /etc/environment

# 启动 cron 进程
cron -f

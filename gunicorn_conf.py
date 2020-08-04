#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pathlib

cpu_count = os.cpu_count()

# 进程名
proc_name = 'task_service'
# 守护模式
daemon = True
# 项目根路径
chdir = str(pathlib.Path.cwd())
# ip 端口配置
bind = '0.0.0.0:30001'
# workers 数
workers = cpu_count
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
timeout = 30
keepalive = 2

raw_env = [
    'WATCH_URL=redis://192.168.2.106:6379/2',
]

# 日志配置
log_path = pathlib.Path('log/')
log_path.mkdir(exist_ok=True)
loglevel = 'error'
errorlog = str(log_path.joinpath('error.log'))
accesslog = str(log_path.joinpath('access.log'))
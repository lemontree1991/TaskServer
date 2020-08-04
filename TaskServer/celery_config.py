#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class Config:
    # 常规设置

    # 时间和日期设置
    timezone = 'Asia/Shanghai'

    # 任务设置
    task_annotations = {'*': {'rate_limit': '10/s'}}
    result_backend = 'redis://127.0.0.1:6379/4'
    result_extended = True  # 扩展的任务结果属性写入后端
    task_acks_late = True

    # broker 配置
    broker_url = 'redis://127.0.0.1:6379/5'

    # worker 配置
    imports = ['TaskServer.core.tasks']
    worker_concurrency = os.cpu_count()  # worker并发数，默认cpu核数
    worker_max_tasks_per_child = 10
    worker_max_memory_per_child = 12 * 1024  # 12M

    # event 配置
    task_send_sent_event = True
    worker_send_task_events = True

    # 日志配置
    worker_redirect_stdouts_level = 'ERROR'
    worker_task_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s"
    worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"

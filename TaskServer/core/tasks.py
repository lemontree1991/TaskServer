#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path
import time
from functools import lru_cache

import celery
import redis
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from modellibrary import ProcessPlus
from modellibrary.src.main.python.core.algorithm.process import StatusCode

from TaskServer import celery_app, states
from TaskServer.config import settings
from TaskServer.enums import CommandCode

logger = get_task_logger(__name__)


# @lru_cache(maxsize=128)
def fib(n: int):
    assert n > 0
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


@celery_app.task(
    bind=True,
    name='fib_task',
)
def fib_task(self, num):
    task_id = self.request.id
    data = {
        'progress': 0,
        'data': []
    }
    if num < 1:
        msg = f'{task_id} num必须为大于0的整数,输入为{num}'
        logger.error(msg)
        data['error_msg'] = msg
        self.update_state(state=states.FAILURE, meta=data)
        raise Ignore()

    count = num + 1
    for i in range(1, count):
        data['progress'] = i / num * 100
        data['data'].append(fib(i))

        self.update_state(state=states.PROGRESS, meta=data)

    return data['data']


class BaseTask(celery.Task):
    paused = False
    watcher = None

    def run(self, *args, **kwargs):
        raise NotImplementedError('Tasks must define the run method.')

    def register_subscribe(self):
        conn = redis.from_url(url=settings.WATCH_URL)
        # conn = redis.Redis(host='127.0.0.1', port=6379, db=2, password='')
        self.watcher = conn.pubsub()
        self.watcher.psubscribe([self.request.id])

    def monitor(self, arithmetic):
        response = self.watcher.get_message()

        if response:
            channel = response['channel']
            msg = response["data"]
            if msg != 1:
                logger.debug(f'接受到订阅信息:{channel} {msg}')
                msg = json.loads(response["data"].decode(encoding='utf8'))
                command = msg['command']
                params = msg['params']
                if CommandCode(command) == CommandCode.STOP:
                    logger.info(f'{self.request.id}: 接受到*终止*信息')
                    arithmetic.process.status = StatusCode.STOP
                    self.update_state(state=StatusCode.STOP)
                    raise Ignore()
                elif CommandCode(command) == CommandCode.PAUSE:
                    logger.info(f'{self.request.id}: 接受到*暂停*信息')
                    arithmetic.process.status = StatusCode.PAUSE
                    self.update_state(state=StatusCode.PAUSE)
                elif CommandCode(command) == CommandCode.RESUME:
                    arithmetic.process.status = StatusCode.PROGRESS
                    logger.info(f'{self.request.id}: 接受到*恢复*信息')
                    self.update_state(state=StatusCode.PROGRESS)
                else:
                    raise ValueError(f'无效的命令:{command}')

    def update_progress(self, state, data):
        self.update_state(state=state, meta=data)


@celery_app.task(base=BaseTask, bind=True, name='simulate-task')
def simulate(self, *, end_time, interval, data):
    task_id = self.request.id
    logger.info(f'{task_id} 接受到参数: end_time={end_time}')
    self.register_subscribe()

    path = Path(__file__).resolve(strict=True).parent.joinpath('schema_data.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
        data['sys_config']['simulate']['terminal'] = end_time

    process_plus = ProcessPlus(config_path=path, data=data)
    process_plus.arithmetic.solve(self.monitor, self.update_progress)
    process_plus.arithmetic.save_result()

    result = {
        'current': process_plus.arithmetic.get_current_result(),
        'result': process_plus.arithmetic.result
    }
    return result

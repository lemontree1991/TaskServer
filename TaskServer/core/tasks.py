#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from functools import lru_cache


from celery.exceptions import Ignore
from celery.utils.log import get_task_logger

from TaskServer import celery_app, states

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

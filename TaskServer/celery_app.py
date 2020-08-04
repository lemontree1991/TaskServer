#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from celery import Celery
from celery.utils.log import get_task_logger

from TaskServer import states
from TaskServer.celery_config import Config

logger = get_task_logger(__name__)

celery_app = Celery('TaskServer')
# celery_app.config_from_object(celeryconfig)
celery_app.config_from_object(Config)


@celery_app.task(bind=True, name='test_task')
def test_task(self, sleep_time: int = 1):
    task_id = self.request.id
    data = {
        'progress': 0,
        'data': []
    }

    for i in range(1, 101):
        data['data'].append(i)
        data['progress'] = i
        self.update_state(state=states.PROGRESS, meta=data)
        logger.info(f'{task_id} progress is {i}')
        time.sleep(sleep_time)

    return data['data']

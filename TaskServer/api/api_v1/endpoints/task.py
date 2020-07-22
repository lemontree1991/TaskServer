#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import time
from typing import Optional
import json

import redis
from fastapi import APIRouter, Body
from celery.result import AsyncResult
from starlette.websockets import WebSocket

from TaskServer import celery_app, states
from TaskServer.config import settings
from TaskServer.core.client import monitor
from TaskServer.schemas.task import ControlTask
from TaskServer.utils.id_generator import id_generator

router = APIRouter()


@router.post('/create', summary='创建任务')
def create_task(
        end_time: int = Body(1, embed=True),
        interval: int = Body(15, embed=True),
        data: dict = Body({}, embed=True)

):
    response = {
        'errcode': 200,
        'msg': '成功',
        'result': None
    }
    active_tasks = monitor.active_tasks()
    count = 0
    for worker_name, tasks in active_tasks.items():
        count += len(tasks)
    if count >= settings.MAX_TASKS:
        response['errcode'] = 400
        response['msg'] = f'当前任务数为{count},最大任务数为{settings.MAX_TASKS},不可新建任务'
        return response

    result = celery_app.send_task(
        task_id=str(id_generator.gen_id()),
        name='simulate-task',
        kwargs={
            'end_time': end_time,
            'interval': interval,
            'data': data
        }
    )

    task_id = result.task_id
    response['result'] = {'task_id': task_id}

    return response


@router.get('/progress/{task_id}', summary='获取任务实时状态')
def get_task_progress(task_id: str):
    response = {
        'errcode': 200,
        'msg': '成功',
        'result': None
    }

    result = celery_app.AsyncResult(task_id)

    if result.status in [states.PROGRESS, states.PAUSE]:
        response['result'] = {
            'state': result.status,
            'progress': result.result['progress'] * 100,
            'result': result.result['result']
        }
    elif result.status == states.FAILURE:
        response['result'] = {
            'state': result.status,
            'traceback': result.traceback
        }
    elif result.status == states.SUCCESS:
        response['result'] = {
            'state': result.status,
            'progress': 100,
            'result': result.result['current']
        }
    else:
        response['result'] = {
            'state': result.status,
        }

    return response


@router.get('/result/{task_id}', summary='获取任务结果')
def get_task_result(task_id: str):
    response = {
        'errcode': 200,
        'msg': '成功',
        'result': None
    }

    result = celery_app.AsyncResult(task_id)
    if result.status != states.SUCCESS:
        response['errcode'] = 400
        response['msg'] = f'当前任务数在非成功状态'
        return response
    response['result'] = result.result['result']
    return response


@router.post('/control', summary='任务控制')
def control_task(command: ControlTask):
    response = {
        'errcode': 200,
        'msg': '成功',
        'result': None
    }
    data = json.dumps(command.dict())
    with redis.from_url(url=settings.WATCH_URL) as conn:
        conn.publish(channel=command.task_id, message=data)

    return response

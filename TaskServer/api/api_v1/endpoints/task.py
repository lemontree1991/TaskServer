#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter
from celery.result import AsyncResult

from TaskServer import celery_app

router = APIRouter()


@router.post('/create', summary='创建任务')
def create_task():
    result = celery_app.send_task('test_task')

    task_id = result.task_id
    return {'task_id': task_id}


@router.get('/{task_id}', summary='获取任务详情')
def retrieve_task(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return result.result


@router.post('/pause/{task_id}', summary='暂停任务')
def pause_task(task_id):
    pass


@router.post('/resume/{task_id}', summary='恢复任务')
def resume_task(task_id):
    pass

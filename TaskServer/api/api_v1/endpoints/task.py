#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

router = APIRouter()


@router.post('/create', summary='创建任务')
def create_task():
    pass


@router.get('/{task_id}', summary='获取任务详情')
def retrieve_task(task_id: str):
    pass


@router.post('/pause/{task_id}', summary='暂停任务')
def pause_task(task_id):
    pass


@router.post('/resume/{task_id}', summary='恢复任务')
def resume_task(task_id):
    pass

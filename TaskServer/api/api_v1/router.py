#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter
from .endpoints import login, task, monitor

api_router = APIRouter()
api_router.include_router(login.router, tags=['登录'])
api_router.include_router(task.router, prefix='/tasks', tags=['任务管理'])
api_router.include_router(monitor.router, prefix='/monitor', tags=['celery管理'])

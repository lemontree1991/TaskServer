#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from TaskServer.core.client import monitor

router = APIRouter()


@router.get('/workers', summary='worker信息')
def workers():
    result = monitor.worker_stats()
    return result


@router.get('/tasks', summary='task信息')
def tasks():
    result = monitor.registered_tasks()
    return result


@router.get('/active_tasks', summary='active_tasks信息')
def active_tasks():
    result = monitor.active_tasks()
    return result

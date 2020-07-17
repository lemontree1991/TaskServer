#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

router = APIRouter()


@router.get('/workers', summary='worker信息')
def workers():
    pass


@router.get('/tasks', summary='task信息')
def tasks():
    pass


@router.get('/active_tasks', summary='active_tasks信息')
def active_tasks():
    pass

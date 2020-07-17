#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

router = APIRouter()


@router.post("/login/access-token", summary='用户登录')
async def login_access_token():
    token = {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE"
                        "1OTU2NjE5MTksInN1YiI6IjEifQ.3ZRURrefyFftMP192blnmP8s7K3EcJCMQWmaE6rwoH0",
        "token_type": "bearer"
    }
    return token

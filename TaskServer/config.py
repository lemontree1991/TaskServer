#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "TaskServer"
    PROJECT_DESC: str = "A Celery Task Server"
    PROJECT_VERSION: str = "0.0.1"
    DOCS_URL: str = '/'
    API_V1_STR: str = '/api/v1'

    # 服务配置
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True

    # 安全配置
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS = ['*']

    # 任务配置
    MAX_TASKS: int = os.cpu_count()
    WATCH_URL: str = 'redis://127.0.0.1:6379/2'

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()

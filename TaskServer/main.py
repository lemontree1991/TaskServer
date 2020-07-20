#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from TaskServer.api.api_v1.router import api_router
from TaskServer.config import settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESC,
    version=settings.PROJECT_VERSION,
    docs_url=settings.DOCS_URL
)

# 处理跨域
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],

    )

app.include_router(
    api_router, prefix=settings.API_V1_STR
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        debug=settings.DEBUG,
        reload=settings.RELOAD
    )

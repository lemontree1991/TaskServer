#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn

from TaskServer import AppFactory
from TaskServer.api.api_v1.router import api_router

env_path = '../local.env'
factory = AppFactory(env_file=env_path)
settings = factory.settings
app = factory.create_app()
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

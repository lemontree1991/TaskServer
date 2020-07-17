#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from TaskServer.config import Settings


class AppFactory:
    def __init__(self, env_file=None):
        if env_file:
            self.settings = Settings(_env_file=env_file)
        else:
            self.settings = Settings()

    def create_app(self):
        app = FastAPI(
            debug=self.settings.DEBUG,
            title=self.settings.PROJECT_NAME,
            description=self.settings.PROJECT_DESC,
            version=self.settings.PROJECT_VERSION,
            docs_url=self.settings.DOCS_URL
        )
        self._cors_handler(app)
        return app

    def _cors_handler(self, app: FastAPI) -> None:
        """处理跨域"""
        if self.settings.BACKEND_CORS_ORIGINS:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],

            )

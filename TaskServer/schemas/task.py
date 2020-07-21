#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic.main import BaseModel

from TaskServer.enums import CommandCode


class ControlTask(BaseModel):
    task_id: str
    command: CommandCode
    params: dict = {}

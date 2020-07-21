#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class CommandCode(str, Enum):
    STOP = 'stop',
    PAUSE = 'pause'
    RESUME = 'resume'


# print(CommandCode.PAUSE.value)
# print(CommandCode('stop'))

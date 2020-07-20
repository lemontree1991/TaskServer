#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from TaskServer import celery_app


class Monitor:
    def __init__(self):
        self._app = celery_app
        self._control = self._app.control
        self._inspect = self._control.inspect()

    def worker_stats(self):
        return self._inspect.stats()

    def worker_statuses(self):
        """
        get worker statuses
        :return:
        """
        response = self._inspect.ping()
        if not response:
            return []
        workers = {}
        for k, v in response.iteritems():
            for k_inner, v_inner in v.iteritems():
                if k_inner == 'ok' and v_inner == 'pong':
                    workers[k] = 'Active'
                else:
                    workers[k] = 'Passive'
                break
        return workers

    def enable_events(self):
        self._control.enable_events()

    def disable_events(self):
        self._control.disable_events()

    def active_tasks(self):
        response = self._inspect.active()
        if not response:
            return {}
        for worker in response.keys():
            for tasks in response[worker]:
                tasks['time_start'] = datetime.datetime.fromtimestamp(tasks['time_start']).strftime(
                    '%Y-%m-%d %H:%M:%S.%f')
        return response

    def registered_tasks(self):
        response = self._inspect.registered()

        return response


monitor = Monitor()

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
from utils import json_wrapper
from arpylibs.basehandler.handler_result import deco_deal_error
from modules.job.job_manage import JobManage
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor


class FetchResultHandler(tornado.web.RequestHandler):
    """
    """
    executor = ThreadPoolExecutor(10)

    @run_on_executor
    @deco_deal_error
    def get(self, job_id):
        """
        """
        res = JobManage.fetch_result(job_id)

        self.write(json_wrapper.dumps(res))

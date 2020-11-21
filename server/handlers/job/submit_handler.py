#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
from utils import json_wrapper
from arpylibs.basehandler.handler_result import deco_deal_error
from modules.job.job_manage import JobManage


class SubmitHandler(tornado.web.RequestHandler):
    """
    """
    @deco_deal_error
    def post(self):
        """
        """

        json_body = json_wrapper.loads(self.request.body)

        res = JobManage.add_jobs(json_body)
        self.write(json_wrapper.dumps(res))

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
from utils import json_wrapper
from arpylibs.basehandler.handler_result import deco_deal_error
from modules.job.job_manage import JobManage


class FetchAggsHandler(tornado.web.RequestHandler):
    """
    """
    @deco_deal_error
    def get(self, job_id):
        """
        """
        res = JobManage.fetch_aggs(job_id)

        self.write(json_wrapper.dumps(res))

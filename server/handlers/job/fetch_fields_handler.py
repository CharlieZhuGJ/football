#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web
from utils import json_wrapper
from arpylibs.basehandler.handler_result import deco_deal_error
from modules.job.job_manage import JobManage


class FetchFieldsHandler(tornado.web.RequestHandler):
    """
    """
    @deco_deal_error
    def get(self, job_id):
        """
        """
        args = self.request.query_arguments
        field_name = args["field_name"][0] if "field_name" in args else None
        field_type = args["field_type"][0] if "field_type" in args else None
        type_list = args["type_list"] if "type_list" in args else []
        res = JobManage.fetch_fields(job_id, type_list, field_name, field_type)

        self.write(json_wrapper.dumps(res))

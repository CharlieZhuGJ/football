#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
服务路由
"""
from handlers.job.submit_handler import SubmitHandler
from handlers.job.fetch_handler import FetchResultHandler


ROUTER = [
    (r'/v1/search/fetch/(.*)', FetchResultHandler),
    (r'/v1/search/submit', SubmitHandler)
]

#!/usr/bin/env python
# -*- coding:utf-8 -*-
from arpylibs.basehandler.base_handler import BaseHandler
import time
import json
import urllib
from utils.global_info import LOGSTASH_HTTP_URL, MANAGER_USER_URL, log
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import socket
socket.setdefaulttimeout(30)


class LogType:
    ACCESS = "访问日志"
    MANAGE = "管理日志"
    OPERATE = "操作日志"


class LoggerHandler(BaseHandler):
    """docstring for LoggerHandler"""
    executor = ThreadPoolExecutor(2)

    def initialize(self):
        """
        """
        self._log_type = ""
        self._log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._log_level = "信息"
        self._ip = ""
        self._action = ""
        self._object_name = ""
        self._object_type = ""
        self._status = ""
        self._user = ""
        self._failure_reason = ""
        self._log_info = ""
        # self._token = ""

    def set_detail_info(self, log_type, action, log_level="信息", object_type="", object_name=""):
        """
        """
        self._log_type = log_type
        self._action = action
        self._log_level = log_level
        self._object_name = object_name
        self._object_type = object_type

    def _get_user_name(self):
        """
        """
        try:
            user_id = self.request.headers["User"]
            result = urllib.urlopen(MANAGER_USER_URL + user_id)
            self._user = json.loads(result.read())["loginName"]
            # self._user = UserManage().get(user_id)["displayName"]
        except Exception as e:
            self._user = "未知用户"

    def _get_ip(self):
        """X-Real-Ip
        """
        self._ip = self.request.headers["X-Real-Ip"]

    def _build_log_info(self):
        """
        """
        info_list = [self._action, self._object_type,
                     self._object_name, self._status, self._failure_reason]

        log_info_list = []

        for ch in info_list:
            if ch:
                if isinstance(ch, unicode):
                    ch = ch.encode("utf8")

                log_info_list.append(ch)

        self._log_info = " ".join(log_info_list)

    def _parse_args_to_log(self):
        """
        """
        self._get_user_name()
        self._get_ip()
        self._build_log_info()

        log_dict = {
            "时间": self._log_time,
            "用户": self._user,
            "IP地址": self._ip,
            "级别": self._log_level,
            "动作": self._action,
            "结果": self._status,
            "日志类型": self._log_type,
            "日志描述": self._log_info,
            "handler": self.__module__,
            "失败原因": self._failure_reason
        }

        if self._log_type == LogType.MANAGE or self._log_type == LogType.OPERATE:
            log_dict["对象类型"] = self._object_type
            log_dict["对象名称"] = self._object_name

        return log_dict

    @run_on_executor
    def on_finish(self):
        """
        """
        self.logger()
        print "输出审计日志到logstash"

    def logger(self):
        """
        """
        try:
            log_info = self._parse_args_to_log()
            urllib.urlopen(LOGSTASH_HTTP_URL, json.dumps(log_info))
        except Exception as e:
            print "logger error"

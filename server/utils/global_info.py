#!/usr/bin/env python
# encoding=utf-8
import yaml
import os
import inspect

CONFIG = {}


def current_path():
    """
    获取当前脚本的上一级目录
    """
    this_file = inspect.getfile(inspect.currentframe())
    return os.path.dirname(os.path.dirname(this_file))


def load_config():
    """
    """
    c_file = os.path.join(current_path(), "config.yml")
    with open(c_file) as f:
        global CONFIG
        CONFIG = yaml.load(f.read())
        print(CONFIG)


load_config()

# 数据库信息
DB_HOST = CONFIG['mysql']['host']
DB_PORT = CONFIG['mysql']['port']
DB_LOCAL_USER = "root"
DB_LOCAL_PASSWD = "123456"
DB_REMOTE_USER = "root"
DB_REMOTE_PASSWD = "123456"
DB_NAME = "Football"

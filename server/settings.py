#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

BASE_DIR = os.path.dirname(__file__)
LIBS_DIR = os.path.join(BASE_DIR, 'libs')

sys.path.append(BASE_DIR)
sys.path.append(LIBS_DIR)


MAX_BODY_SIZE = 1024 * 1024 * 1024


SETTINGS = {
    # debug 配置
    'debug': False,
    'autoreload': False,
    'debug_host': '127.0.0.1',

    #template 配置
    'template_path': os.path.join(BASE_DIR, 'templates'),

    #cookie 配置
    'cookie_secret': '*#9!pp18-0l8h2bmb(*3cv2vv1q4fh^begv*x*zgf-f2&@qw%-',
}

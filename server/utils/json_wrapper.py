# coding:utf-8
'''
封装json的loads函数，自动将unicode进行utf-8编码，解决中文被loads后不是utf-8编码的问题
'''
import json


def recur_covert_to_utf(data):
    """
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, unicode):
                data[key] = value.encode("utf-8")
            elif isinstance(value, dict):
                data[key] = recur_covert_to_utf(value)
    return data


def loads(data):
    """
    """
    data = json.loads(data)
    return recur_covert_to_utf(data)


def dumps(data):
    """
    """
    return json.dumps(data)

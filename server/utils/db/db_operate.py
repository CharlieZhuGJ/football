# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
数据库操作类
"""

from utils.db import db_connector
from contextlib import contextmanager
from utils import global_info


@contextmanager
def safe_cursor(conn):
    """
    从连接出获取游标，执行完sql后，自动关闭游标
    conn = ConnectorManager.get_db_conn()
    with safe_cursor(conn) as cursor:
        user_id = "id1"
        cursor.execute("select * from t_user where f_user_id = %s", user_id)
    """
    cursor = None
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except:
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


class DBOperate(object):
    """
    AnyRobot数据库操作类
    """
    connector = None

    def __init__(self):
        """
        初始化函数
        """
        pass

    def init_connector(self):
        """
        初始化数据库连接池
        """
        info = db_connector.DBInfo()
        info.host = global_info.DB_HOST
        info.port = global_info.DB_PORT
        info.user = global_info.DB_LOCAL_USER
        info.passwd = global_info.DB_LOCAL_PASSWD
        info.dbname = global_info.DB_NAME
        info.read_timeout = 60
        info.write_timeout = 60
        DBOperate.connector = db_connector.Connector(info)

    def get_operate(self):
        """
        获取 AnyRobot数据库操作句柄
        """
        try:
            if not DBOperate.connector:
                self.init_connector()

            return DBOperate.connector.get_db_operate_obj()
        except Exception:
            raise Exception("数据库异常")

    @property
    def operate(self):
        """
        sharemgnt数据库操作属性
        """

        return self.get_operate()

    def get_conn(self):
        """
        """
        if not DBOperate.connector:
            self.init_connector()

        return DBOperate.connector.get_db_operate_obj()

    def get_cursor(self):
        """
        """
        return self.get_conn().cursor()

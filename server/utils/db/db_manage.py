# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
本脚本用于初始化eofs的数据库表
"""
import os
import re
import json
import copy
import MySQLdb
from db import db_info
from utils import json_wrapper
from utils import global_info
from utils.db .db_operate import DBOperate


data_dict = {}


class DBManager(DBOperate):
    """
    AnyRobot数据库管理类
    """

    def save_db_data(self):
        """
        """
        try:
            for name in db_info.table_names:
                try:
                    select_sql = "SELECT * FROM %s" % name
                    # cursor.execute(select_sql)
                    data_dict[name] =  self.operate.fetch_all_result(select_sql)
                except Exception as e:
                    pass

        except Exception as e:
            print("save_db_data error: %s" % str(e))
            # sys.exit(1)

    def update_all_db_table(self):
        """更新所有表结构
        """
        try:
            # 删除原来存在的表，重新创建
            for name in data_dict.keys():
                try:
                    delete_sql = "DROP TABLE %s" % name
                    self.operate.delete(delete_sql)
                    self.operate.update(db_info.table_list[db_info.table_names.index(name)])
                except Exception as e:
                    pass

        except Exception as e:
            print("update_all_db_table error: %s" % str(e))
            # sys.exit(1)

    def update_db_data(self):
        """
        更新数据库数据
        """
        try:
            for key, values in data_dict.items():
                try:
                    for value in values:
                        self.operate.insert(key, value)
                except Exception as e:
                    print(str(e))

        except Exception as e:
            print("update_db_fields error: %s" % str(e))
            # sys.exit(1)

    def update_db(self):
        """
        """
        self.save_db_data()
        self.update_all_db_table()
        self.update_db_data()


    def init_anyrobot_db(self):
        """
        初始化AnyRobot 数据库
        """
        self.update_db()


def init_mysql_db():
    """
    开始创建数据表，填充初始化数据
    """
    conn = None
    cur = None
    try:
        conn = MySQLdb.connect(host=global_info.DB_HOST,
                               user=global_info.DB_LOCAL_USER,
                               passwd=global_info.DB_LOCAL_PASSWD,
                               port=global_info.DB_PORT)

        cur = conn.cursor()

        # 创建数据库
        cur.execute("CREATE DATABASE if not exists %s CHARACTER SET utf8 COLLATE utf8_bin;"
                    % global_info.DB_NAME)
        cur.execute("USE %s;" % global_info.DB_NAME)

        grant_sql = "grant all privileges on *.* to '{0}'@'%' identified by '{1}'".format(global_info.DB_REMOTE_USER,
                                                                                          global_info.DB_REMOTE_PASSWD)
        cur.execute(grant_sql)
        cur.execute("flush privileges")

        # 设置去掉ONLY_FULL_GROUP_BY，重新设置值
        sql = "set @@global.sql_mode ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';"
        cur.execute(sql)

        # 去除已存的数据库的设置去掉ONLY_FULL_GROUP_BY
        sql = "set sql_mode ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';"
        cur.execute(sql)

        # 创建数据表
        for sql in db_info.table_list:
            cur.execute(sql)
        conn.commit()
    except Exception as ex:
        raise ex
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    try:
        print("success")
        init_mysql_db()
        print("success")
        print("success")
    except:
        import traceback
        import sys
        traceback.print_exc()
        sys.exit(1)

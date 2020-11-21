# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
python 模块数据库公共连接类
提供两种操作方式
1.使用数据库连接池管理模块 DBUtils,返回数据库连接对象,可由调用者自已使用 mysql acid
2.使用数据库连接池管理模块 DBUtils,返回封装类 DBOperate 对象,可调用常用数据库操作接口
"""

from warnings import filterwarnings
import MySQLdb
filterwarnings('ignore', category=MySQLdb.Warning)

from MySQLdb.cursors import DictCursor
from dbutils.persistent_db import PersistentDB

class DBInfo:
    """
    功能：构造数据库连接属性
    说明：host 连接的数据库IP地址 -- "127.0.0.1"
          port 连接的数据库端口   -- "3307"
          user 访问数据库的用户名 -- "root"
          passwd 访问数据库的密码 -- "eisoo.com"
          dbname 访问的数据库名称 -- "ENMC"
          read_timeout mysql连接读超时设置，单位：秒 -- 60
          write_timeout mysql连接写超时设置，单位：秒 -- 60
    """
    def __init__(self):
        self.host = ''
        self.port = 0
        self.user = ''
        self.passwd = ''
        self.dbname = ''
        self.read_timeout = 0
        self.write_timeout = 0


class Connector:
    """
    功能：MySQL 连接管理器，供各python模块使用
    说明：封装公共方法, 增、删、改、查，及事务处理
    """
    pool = None

    def __init__(self, dbinfo):
        """
        init
        """
        self.host = dbinfo.host
        self.port = dbinfo.port
        self.user = dbinfo.user
        self.pwd = dbinfo.passwd
        self.dbname = dbinfo.dbname
        self.read_timeout = dbinfo.read_timeout
        self.write_timeout = dbinfo.write_timeout

    def escape(self, value):
        """
        转义非法字符
        """
        return MySQLdb.escape_string(value)

    def get_pool(self):
        """
        功能：基于 PersistentDB 模块,管理连接池
        说明：creator     指 python 所使用的 mysql 数据库模块
              ping=4      指当查询时使用,检查连接
              maxusage=0  指不限制一个连接使用次数
              setsession  指定编码方式
              cursorclass 指定为字典方式
        """
        self.pool = PersistentDB(creator=MySQLdb,
                                 host=self.host,
                                 port=self.port,
                                 user=self.user,
                                 passwd=self.pwd,
                                 db=self.dbname,
                                 ping=4,
                                 maxusage=0,
                                 setsession=["set names utf8;"],
                                 read_timeout=self.read_timeout,
                                 write_timeout=self.write_timeout,
                                 cursorclass=DictCursor)
        return self.pool

    def get_db_conn(self):
        """
        功能：使用 PersistentDB 管理连接池,连接均为专用连接
        说明：使用方法如下,注意关闭游标,及连接
              dbInfo = DBInfo();             //构造数据库连接基本信息
              conn_inst = Connector(dbInfo)  //构造数据库连接类实例
              conn = conn_inst.get_db_conn() //调用数据库连接的接口
              cursor = conn.cursor()         //调用当前游标
              cursor.execute(sql)            //调用execute(sql),执行 sql
              conn.commit()                  //事务性提交
              cursor.close()                 //关闭游标
              conn.close()                   //关闭连接
        """
        try:
            if self.pool is None:
                self.pool = self.get_pool()
            return self.pool.connection()
        except MySQLdb.OperationalError as ex:
            raise ex

    def get_db_operate_obj(self):
        """
        功能：使用 PersistentDB 管理连接池,连接均为专用连接
        说明：使用此连接,可调用已封装函数,进行数据库操作,也可以自己实现,使用 mysql 事务机制
              增 insert, insert_many
              删 delete
              改 update
              查 one,all
              使用方法参见备函数说明
        """
        try:
            if self.pool is None:
                self.pool = self.get_pool()
            return DBOperate(self.pool.connection())
        except MySQLdb.OperationalError as ex:
            raise ex


class DBOperate(object):
    """
    DB操作类，用于执行SQL语句
    """
    def __init__(self, conn):
        """
        Init
        """
        self.conn = conn
        self.cursor = None

    def __del__(self):
        """
        Del
        """
        self.conn.close()

    def get_columns(self, columns):
        """
        将列名列表转换为字符串
        param columns : 由表中的列名组成的列表
        例如：
            get_columns(["id", "name"])
            => (`id`, `name`)
        """
        stmt = ["`%s`" % c for c in columns]
        return " (%s) " % (", ".join(stmt))

    def insert(self, table, columns):
        """
        插入一条数据,建议使用字典方式构造,可读性强
        若列表方式,只适用于对表中所有字段进行插入
        Args:
            table: string，要插入的表名
            columns: dict or list，要插入值的列名以及值
                     如果是字典，键为列名
                     如果是列表，元素为值
        Return:
            最后一个插入语句的自增ID，如果没有则为0
        Raise:
            TypeError: 参数类型错误时丢出异常
        Example:
            insert("test_table", {"id": 1, "name": "test"})
            => INSERT INTO `test_table` (`id`, `name`) VALUES ("1", "test")
            insert("test_table", [1, "test"])
            => INSERT INTO `test_table` VALUES ("1", "test")
        """
        if not isinstance(table, str):
            raise TypeError("table only use string type")

        sql = ["INSERT INTO `{0}` ".format(table)]

        if isinstance(columns, dict):
            sql.append(self.get_columns(columns.keys()))
            values = columns.values()
        elif isinstance(columns, list):
            values = columns
        else:
            raise TypeError("columns only use list or dict type")

        sql.append(" VALUES (%s) " % (", ".join(["%s"] * len(values))))

        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute("".join(sql), values)
            self.conn.commit()
            last_id = self.cursor.lastrowid
            return last_id
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.cursor.close()

    def insert_many(self, table, columns, values):
        """
        插入多条数据,建议使用字典方式构造,可读性强
        若列表方式,只适用于对表中所有字段进行插入
        Args:
            table: 字符串，要插入的表名
            columns: 列表，要插入值的列，不需要参数使用空列表
            values: 列表元组嵌套，要插入的值
        Return:
            插入行数
        Raise:
            TypeError: 参数类型错误时丢出异常
        Example:
            insert_many("test_table", ["id", "name"], [(1, "name1"), (2, "name2")])
            => INSERT INTO `test_table` (`id`, `name`) VALUES ("1", "name1"), ("2", "name2")
            insert_many("test_table", [], [(1, "name1"), (2, "name2")])
            => INSERT INTO `test_table` VALUES ("1", "name1"), ("2", "name2")
        """
        if not isinstance(table, str):
            raise TypeError("table only use string type")

        if not isinstance(columns, list) or not isinstance(values, list):
            raise TypeError("columns or values only use list type")

        if not isinstance(values[0], tuple):
            raise TypeError("values value only use tuple type")

        sql = ["INSERT INTO `{0}`".format(table)]
        if columns:
            sql.append(self.get_columns(columns))

        sql.append(" VALUES (%s) " % (", ".join(["%s"] * len(values[0]))))

        try:
            self.cursor = self.conn.cursor()
            row_affected = self.cursor.executemany("".join(sql), values)
            self.conn.commit()
            return row_affected
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.cursor.close()

    def update(self, sql, *args):
        '''
        功能：执行一条更新的sql
        说明：本操作返回受影响行数与最后插入行的自增ID,
              当格式化参数为数值型时,依然使用 %s(MySQLdb 格式化的一个问题),如下所示：
        举例：
            db_obj = Connector(dbinfo)
            conn = db_obj.get_db_operate_obj()
            sql = "UPDATE `test_table` SET `name` = %s
            WHERE `id` = %s"
            调用 conn.update(sql, name, 1000)
        '''
        try:
            self.cursor = self.conn.cursor()
            affect_row = self.cursor.execute(sql, args)
            last_id = self.cursor.lastrowid
            self.conn.commit()
            return (affect_row, last_id)
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.cursor.close()

    def delete(self, sql, *args):
        '''
        功能：执行一条删除的sql
        说明：本操作返回受影响行数与最后插入行的自增ID
              当格式化参数为数值型时,依然使用 %s(MySQLdb 格式化的一个问题),如下所示：
        举例：
            db_obj = Connector(dbinfo)
            conn = db_obj.get_db_operate_obj()
            sql = "Delete `test_table` SET `name` = %s
            WHERE `id` = %s"
            调用 conn.delete(sql, name, 1001)
        '''
        try:
            self.cursor = self.conn.cursor()
            affect_row = self.cursor.execute(sql, args)
            last_id = self.cursor.lastrowid
            self.conn.commit()
            return (affect_row, last_id)
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.cursor.close()

    def fetch_all_result(self, sql, *args):
        '''
        功能：执行一条查询语句，并返回所有结果
        举例：
            db_obj = Connector(dbinfo)
            conn = db_obj.get_db_operate_obj()
            sql = "SELECT `name` FROM `table`"
            result = conn.fetch_all_result(sql)
        '''
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            self.conn.commit()
            return result
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.cursor.close()

    def fetch_one_result(self, sql, *args):
        '''
        功能：执行一条查询语句，并返回一条记录
        举例：
            db_obj = Connector(dbinfo)
            conn = db_obj.get_db_operate_obj()
            sql = "SELECT `name` FROM `table`
                WHERE `id` = %s"
            result = conn.fetch_one_result(sql, id)
        '''
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, args)
            result = self.cursor.fetchone()
            self.conn.commit()
            return result
        except Exception as ex:
            self.conn.rollback()
            raise ex
        finally:
            self.cursor.close()

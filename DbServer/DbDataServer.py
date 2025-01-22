import sqlite3
from OutPut.outPut import op

class DbDataServer:
    @staticmethod
    def openDb(dbPath):
        """
        打开数据库
        :param dbPath: 数据库路径
        :return: 连接对象和游标对象
        """
        try:
            conn = sqlite3.connect(dbPath)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            op(f'[-]: 打开数据库出现错误, 错误信息: {e}')
            return None, None

    @staticmethod
    def closeDb(conn, cursor):
        """
        关闭数据库
        :param conn: 连接对象
        :param cursor: 游标对象
        :return:
        """
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            op(f'[-]: 关闭数据库出现错误, 错误信息: {e}')

    @staticmethod
    def createTable(cursor, tableName, tableStructure):
        """
        创建表
        :param cursor: 游标对象
        :param tableName: 表名
        :param tableStructure: 表结构
        :return: bool
        """
        try:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {tableName} {tableStructure}')
            return True
        except Exception as e:
            op(f'[-]: 创建表出现错误, 错误信息: {e}')
            return False

    @staticmethod
    def dropTable(cursor, tableName):
        """
        删除表
        :param cursor: 游标对象
        :param tableName: 表名
        :return: bool
        """
        try:
            cursor.execute(f'DROP TABLE IF EXISTS {tableName}')
            return True
        except Exception as e:
            op(f'[-]: 删除表出现错误, 错误信息: {e}')
            return False

    @staticmethod
    def searchTable(cursor, tableName):
        """
        查询表是否存在
        :param cursor: 游标对象
        :param tableName: 表名
        :return: bool
        """
        try:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (tableName,)
            )
            return cursor.fetchone() is not None
        except Exception as e:
            op(f'[-]: 查询表是否存在出现错误, 错误信息: {e}')
            return False

    @staticmethod
    def clearTable(cursor, tableName):
        """
        清空表数据
        :param cursor: 游标对象
        :param tableName: 表名
        :return: bool
        """
        try:
            cursor.execute(f'DELETE FROM {tableName}')
            return True
        except Exception as e:
            op(f'[-]: 清空表数据出现错误, 错误信息: {e}')
            return False

    @staticmethod
    def insertData(cursor, tableName, data):
        """
        插入数据
        :param cursor: 游标对象
        :param tableName: 表名
        :param data: 数据字典
        :return: bool
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = tuple(data.values())
            cursor.execute(
                f'INSERT INTO {tableName} ({columns}) VALUES ({placeholders})',
                values
            )
            return True
        except Exception as e:
            op(f'[-]: 插入数据出现错误, 错误信息: {e}')
            return False

    @staticmethod
    def updateData(cursor, tableName, data, condition):
        """
        更新数据
        :param cursor: 游标对象
        :param tableName: 表名
        :param data: 更新的数据字典
        :param condition: 条件字典
        :return: bool
        """
        try:
            set_clause = ', '.join([f'{k}=?' for k in data.keys()])
            where_clause = ' AND '.join([f'{k}=?' for k in condition.keys()])
            values = tuple(list(data.values()) + list(condition.values()))
            cursor.execute(
                f'UPDATE {tableName} SET {set_clause} WHERE {where_clause}',
                values
            )
            return True
        except Exception as e:
            op(f'[-]: 更新数据出现错误, 错误信息: {e}')
            return False 
import DbServer.DbDomServer as Dds
import Config.ConfigServer as Cs
from OutPut.outPut import op


class DbUserServer:
    def __init__(self):
        pass

    def addAdmin(self, wxId, roomId):
        """
        增加管理员
        :param wxId: 微信ID
        :param roomId: 群聊ID
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnUserDbPath())
        try:
            if not self.searchAdmin(wxId, roomId):
                cursor.execute(f'INSERT INTO Admin VALUES ({wxId}, {roomId})')
                conn.commit()
                Dds.closeDb(conn, cursor)
                return True
            return False
        except Exception as e:
            op(f'[-]: 增加管理员出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def delAdmin(self, wxId, roomId):
        """
        删除管理员
        :param wxId: 微信ID
        :param roomId: 群聊ID
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnUserDbPath())
        try:
            cursor.execute('DELETE FROM Admin WHERE wxId=? AND roomId=?', (wxId, roomId))
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 删除管理员出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def searchAdmin(self, wxId, roomId):
        """
        查询管理员
        :param wxId: 微信ID
        :param roomId: 群聊ID
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnUserDbPath())
        try:
            cursor.execute('SELECT wxId FROM Admin WHERE wxId=? AND roomId=?', (wxId, roomId))
            result = cursor.fetchone()
            Dds.closeDb(conn, cursor)
            if result:
                return True
            else:
                return False
        except Exception as e:
            op(f'[-]: 查询管理员出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def addFeature(self, name, description):
        """
        添加用户功能
        :param name: 功能名字
        :param description: 功能解释
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnUserDbPath())
        try:
            if not self.searchFeature(name):
                cursor.execute(f"INSERT INTO Feature VALUES ({name},{description})")
                conn.commit()
                Dds.closeDb(conn, cursor)
                return True
            return False
        except Exception as e:
            op(f'[-]: 增加用户功能出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def delFeature(self, name):
        conn, cursor = Dds.openDb(Cs.returnUserDbPath())
        try:
            cursor.execute(f'DELETE FROM Feature WHERE name={name}')
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 删除用户功能出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def searchFeature(self, name=None):
        conn, cursor = Dds.openDb(Cs.returnUserDbPath())
        try:
            if name == None:
                sql = f'SELECT name,description FROM Feature'
            else:
                sql = f'SELECT name,description FROM Feature where name={name}'
            cursor.execute(sql)
            result = cursor.fetchone()
            Dds.closeDb(conn, cursor)
            if result:
                return True
            else:
                return False
        except Exception as e:
            op(f'[-]: 查询用户功能出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

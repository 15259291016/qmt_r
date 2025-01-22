import DbServer.DbDomServer as Dds
import Config.ConfigServer as Cs
from OutPut.outPut import op


class DbRoomServer:
    def __init__(self):
        """
        初始化数据库表
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            # 创建退群监控表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monitorRoom (
                    roomId TEXT PRIMARY KEY,
                    roomName TEXT
                )
            ''')
            # 创建群成员记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS roomMembers (
                    roomId TEXT,
                    memberId TEXT,
                    memberName TEXT,
                    updateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (roomId, memberId)
                )
            ''')
            conn.commit()
        except Exception as e:
            op(f'[-]: 创建数据库表出现错误, 错误信息: {e}')
        finally:
            Dds.closeDb(conn, cursor)

    def addWhiteRoom(self, roomId, roomName):
        """
        新增白名单群聊
        :param roomName:
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            if not self.searchWhiteRoom(roomId):
                cursor.execute('INSERT INTO whiteRoom VALUES (?, ?)', (roomId, roomName))
                conn.commit()
                Dds.closeDb(conn, cursor)
                return True
            return False
        except Exception as e:
            op(f'[-]: 新增白名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def delWhiteRoom(self, roomId):
        """
        删除白名单群聊
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('DELETE FROM whiteRoom WHERE roomId=?', (roomId,))
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 删除白名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def searchWhiteRoom(self, roomId):
        """
        查询白名单群聊
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('SELECT roomName FROM whiteRoom WHERE roomId=?', (roomId,))
            result = cursor.fetchone()
            Dds.closeDb(conn, cursor)
            if result:
                return True
            return False
        except Exception as e:
            op(f'[-]: 查询白名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def showWhiteRoom(self, ):
        """
        查看所有白名单群聊
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        dataDict = dict()
        try:
            cursor.execute('SELECT roomId, roomName FROM whiteRoom')
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            if result:
                for res in result:
                    dataDict[res[0]] = res[1]
            return dataDict
        except Exception as e:
            op(f'[-]: 查看所有白名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return dataDict

    def addBlackRoom(self, roomId, roomName):
        """
        新增黑名单群聊
        :param roomName:
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            if not self.searchBlackRoom(roomId):
                cursor.execute('INSERT INTO blackRoom VALUES (?, ?)', (roomId, roomName))
                conn.commit()
                Dds.closeDb(conn, cursor)
                return True
            return False
        except Exception as e:
            op(f'[-]: 新增黑名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def delBlackRoom(self, roomId):
        """
        删除黑名单群聊
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('DELETE FROM blackRoom WHERE roomId=?', (roomId,))
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 删除黑名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def searchBlackRoom(self, roomId):
        """
        查询黑名单群聊
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('SELECT roomName FROM blackRoom WHERE roomId=?', (roomId,))
            result = cursor.fetchone()
            Dds.closeDb(conn, cursor)
            if result:
                return result
            else:
                return False
        except Exception as e:
            op(f'[-]: 查询黑名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def showBlackRoom(self, ):
        """
        查看所有黑名单群聊
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        dataDict = dict()
        try:
            cursor.execute('SELECT roomId, roomName FROM blackRoom')
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            if result:
                for res in result:
                    dataDict[res[0]] = res[1]
            return dataDict
        except Exception as e:
            op(f'[-]: 查看所有黑名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return dataDict

    def addPushRoom(self, roomId, roomName):
        """
        新增推送群聊
        :param roomName:
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            if not self.searchPushRoom(roomId):
                cursor.execute('INSERT INTO pushRoom VALUES (?, ?)', (roomId, roomName))
                conn.commit()
                Dds.closeDb(conn, cursor)
                return True
            return False
        except Exception as e:
            op(f'[-]: 新增推送群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def delPushRoom(self, roomId):
        """
        删除推送群聊
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('DELETE FROM pushRoom WHERE roomId=?', (roomId,))
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 删除推送群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def searchPushRoom(self, roomId):
        """
        查询推送群聊
        :param roomId:
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('SELECT roomName FROM pushRoom WHERE roomId=?', (roomId,))
            result = cursor.fetchone()
            Dds.closeDb(conn, cursor)
            if result:
                return result
            else:
                return False
        except Exception as e:
            op(f'[-]: 查询推送群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def showPushRoom(self, ):
        """
        查看所有推送群聊
        :return:
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        dataDict = dict()
        try:
            cursor.execute('SELECT roomId, roomName FROM pushRoom')
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            if result:
                for res in result:
                    dataDict[res[0]] = res[1]
            return dataDict
        except Exception as e:
            op(f'[-]: 查看所有黑名单群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return dataDict

    def addMonitorRoom(self, roomId, roomName):
        """
        添加退群监控群聊
        :param roomName: 群聊名称
        :param roomId: 群聊ID
        :return: bool
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            if not self.searchMonitorRoom(roomId):
                cursor.execute('INSERT INTO monitorRoom VALUES (?, ?)', (roomId, roomName))
                conn.commit()
                Dds.closeDb(conn, cursor)
                return True
            return False
        except Exception as e:
            op(f'[-]: 添加退群监控群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def delMonitorRoom(self, roomId):
        """
        删除退群监控群聊
        :param roomId: 群聊ID
        :return: bool
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('DELETE FROM monitorRoom WHERE roomId=?', (roomId,))
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 删除退群监控群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def searchMonitorRoom(self, roomId):
        """
        查询退群监控群聊
        :param roomId: 群聊ID
        :return: tuple or False
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('SELECT roomName FROM monitorRoom WHERE roomId=?', (roomId,))
            result = cursor.fetchone()
            Dds.closeDb(conn, cursor)
            if result:
                return result
            return False
        except Exception as e:
            op(f'[-]: 查询退群监控群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def showMonitorRoom(self):
        """
        查看所有退群监控群聊
        :return: dict
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        dataDict = dict()
        try:
            cursor.execute('SELECT roomId, roomName FROM monitorRoom')
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            if result:
                for res in result:
                    dataDict[res[0]] = res[1]
            return dataDict
        except Exception as e:
            op(f'[-]: 查看所有退群监控群聊出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return dataDict

    def saveRoomMembers(self, roomId, members):
        """
        保存群成员列表
        :param roomId: 群ID
        :param members: 成员列表 [(memberId, memberName), ...]
        :return: bool
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            # 先删除该群的旧记录
            cursor.execute('DELETE FROM roomMembers WHERE roomId=?', (roomId,))
            # 插入新记录
            cursor.executemany(
                'INSERT INTO roomMembers (roomId, memberId, memberName) VALUES (?, ?, ?)',
                [(roomId, m[0], m[1]) for m in members]
            )
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 保存群成员列表出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def getRoomMembers(self, roomId):
        """
        获取群成员列表
        :param roomId: 群ID
        :return: list or None
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute('SELECT memberId FROM roomMembers WHERE roomId=?', (roomId,))
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            if result:
                return [r[0] for r in result]
            return None
        except Exception as e:
            op(f'[-]: 获取群成员列表出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return None

    def addLeftMemberRecord(self, roomId, memberId, memberName):
        """
        添加退群记录
        :param roomId: 群ID
        :param memberId: 成员ID
        :param memberName: 成员名称
        :return: bool
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute(
                'INSERT INTO leftMembers (roomId, memberId, memberName) VALUES (?, ?, ?)',
                (roomId, memberId, memberName)
            )
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 添加退群记录出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

    def getLeftMemberRecords(self, roomId):
        """
        获取群的退群记录
        :param roomId: 群ID
        :return: list or None
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            cursor.execute(
                'SELECT memberId, memberName, leftTime FROM leftMembers WHERE roomId=? ORDER BY leftTime DESC',
                (roomId,)
            )
            result = cursor.fetchall()
            Dds.closeDb(conn, cursor)
            if result:
                return [
                    {
                        'member_id': record[0],
                        'member_name': record[1],
                        'left_time': record[2]
                    }
                    for record in result
                ]
            return None
        except Exception as e:
            op(f'[-]: 获取退群记录出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return None

    def clearLeftMemberRecords(self, roomId=None):
        """
        清除退群记录
        :param roomId: 群ID，如果不指定则清除所有记录
        :return: bool
        """
        conn, cursor = Dds.openDb(Cs.returnRoomDbPath())
        try:
            if roomId:
                cursor.execute('DELETE FROM leftMembers WHERE roomId=?', (roomId,))
            else:
                cursor.execute('DELETE FROM leftMembers')
            conn.commit()
            Dds.closeDb(conn, cursor)
            return True
        except Exception as e:
            op(f'[-]: 清除退群记录出现错误, 错误信息: {e}')
            Dds.closeDb(conn, cursor)
            return False

import DbServer.DbDomServer as Dds
import Config.ConfigServer as Cs
from OutPut.outPut import op


class DbInitServer:
    def __init__(self):
        self.userDb = Cs.returnUserDbPath()
        self.pointDb = Cs.returnPointDbPath()
        self.roomDb = Cs.returnRoomDbPath()
        self.ghDb = Cs.returnGhDbPath()
        self.roomMsgDb = Cs.returnRoomMsgDbPath()



    def initDb(self, ):
        # 初始化用户数据库
        userConn, userCursor = Dds.openDb(self.userDb)

        # 启用外键支持（如果是 SQLite）
        userCursor.execute("PRAGMA foreign_keys = ON")
        # 用户表（明确主键）
        Dds.createTable(userCursor, 'User', 'wxId varchar(255) PRIMARY KEY, wxName varchar(255)')
        # 管理员表
        Dds.createTable(userCursor, 'Admin', 'wxId varchar(255), roomId varchar(255)')

        # 功能表
        Dds.createTable(userCursor, 'Feature',
                        'name varchar(255) PRIMARY KEY, description TEXT')

        # 用户功能关联表（修正 featureId 类型）
        Dds.createTable(userCursor, 'UserFeature', '''
            wxId varchar(255),
            featureId INTEGER,
            enabled BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (wxId) REFERENCES User(wxId),
            FOREIGN KEY (featureId) REFERENCES Feature(id)
        ''')

        Dds.closeDb(userConn, userCursor)

        # 初始化积分数据库 积分数据表 签到表
        pointConn, pointCursor = Dds.openDb(self.pointDb)
        Dds.createTable(pointCursor, 'Point', 'wxId varchar(255), roomId varchar(255), poInt int(32)')
        Dds.createTable(pointCursor, 'Sign', 'wxId varchar(255), roomId varchar(255)')
        Dds.closeDb(pointConn, pointCursor)

        # 初始化群聊数据库 黑名单群聊数据表 白名单群聊数据表 推送群聊数据表 所有群聊数据表
        roomConn, roomCursor = Dds.openDb(self.roomDb)
        Dds.createTable(roomCursor, 'whiteRoom', 'roomId varchar(255), roomName varchar(255)')
        Dds.createTable(roomCursor, 'blackRoom', 'roomId varchar(255), roomName varchar(255)')
        Dds.createTable(roomCursor, 'pushRoom', 'roomId varchar(255), roomName varchar(255)')
        Dds.createTable(roomCursor, 'Room', 'roomId varchar(255), roomName varchar(255)')
        Dds.createTable(roomCursor, 'leftMembers', '''
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roomId TEXT,
            memberId TEXT,
            memberName TEXT,
            leftTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ''')
        Dds.closeDb(roomConn, roomCursor)

        # 初始化公众号数据库 白名单公众号 黑名单公众号
        ghConn, ghCursor = Dds.openDb(self.ghDb)
        Dds.createTable(ghCursor, 'whiteGh', 'ghId varchar(255), ghName varchar(255)')
        Dds.createTable(ghCursor, 'blackGh', 'ghId varchar(255), ghName varchar(255)')
        Dds.closeDb(ghConn, ghCursor)

        # 初始化群聊消息数据库
        roomMsgConn, roomMsgCursor = Dds.openDb(self.roomMsgDb)
        Dds.closeDb(roomMsgConn, roomMsgCursor)


        op(f'[+]: 数据库初始化成功！！！')


if __name__ == '__main__':
    Dis = DbInitServer()
    Dis.initDb()

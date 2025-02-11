from BotServer.MsgHandleServer.FriendMsgHandle import FriendMsgHandle
from BotServer.MsgHandleServer.RoomMsgHandle import RoomMsgHandle
from PushServer.PushMainServer import PushMainServer
from DbServer.DbInitServer import DbInitServer
import FileCache.FileCacheServer as Fcs
from threading import Thread
from OutPut.outPut import op
from cprint import cprint
from queue import Empty
from wcferry import Wcf
import re


class MainServer:
    def __init__(self):
        self.wcf = Wcf()
        self.Dis = DbInitServer()
        # 开启全局接收
        self.wcf.enable_receiving_msg()
        self.Rmh = RoomMsgHandle(self.wcf)
        self.Fmh = FriendMsgHandle(self.wcf)
        self.Pms = PushMainServer(self.wcf)
        # 初始化服务以及配置
        Thread(target=self.initConfig, name='初始化服务以及配置').start()

    def isLogin(self, ):
        """
        判断是否登录
        :return:
        """
        ret = self.wcf.is_login()
        if ret:
            userInfo = self.wcf.get_user_info()
            # 用户信息打印
            cprint.info(f"""
            \t========== NGCBot V2.2 ==========
            \t微信名：{userInfo.get('name')}
            \t微信ID：{userInfo.get('wxid')}
            \t手机号：{userInfo.get('mobile')}
            \t========== NGCBot V2.2 ==========       
            """.replace(' ', ''))

    def processMsg(self, ):
        # 判断是否登录
        self.isLogin()
        # self.wcf.query_sql('', '')
        while self.wcf.is_receiving_msg():
            try:
                msg = self.wcf.get_msg()
                # 调试专用
                # op(f'[*]: 接收到消息: {msg}')
                op(f'[*]: 接收到消息\n[*]: 群聊ID: {msg.roomid}\n[*]: 发送人ID: {msg.sender}\n[*]: 发送内容: {msg.content}\n--------------------')
                # 群聊消息处理
                # if '@chatroom' in msg.roomid and msg.roomid in ['57471680941@chatroom', '57240198127@chatroom',
                #                                                 '38886199012@chatroom',
                #                                                 "48302252369@chatroom", "34494414197@chatroom"]:
                # 承诺不打游戏，前端交流群，gp交流群，赚钱大业,跑步干饭小分队
                if '@chatroom' in msg.roomid:
                    Thread(target=self.Rmh.mainHandle, args=(msg,)).start()
                # 好友消息处理
<<<<<<< HEAD
                # if '@chatroom' not in msg.roomid and 'gh_' not in msg.sender and msg.roomid in ["wxid_ep8bhx9d5j7l21","wxid_cl7ri553olno22"]:
=======
                # if '@chatroom' not in msg.roomid and 'gh_' not in msg.sender:
                # if '@chatroom' not in msg.roomid and 'gh_' not in msg.sender and msg.roomid in ["wxid_cl7ri553olno22"]:
>>>>>>> e087e014910e90fe51c437b9f2755d67175880e0
                #     Thread(target=self.Fmh.mainHandle, args=(msg,)).start()
                # else:
                #     pass
            except Empty:
                continue

    def initConfig(self, ):
        """
        初始化数据库 缓存文件夹 开启定时推送服务
        :return:
        """
        self.Dis.initDb()
        Fcs.initCacheFolder()
        Thread(target=self.Pms.run, name='定时推送服务').start()


if __name__ == '__main__':
    Ms = MainServer()
    Ms.processMsg()

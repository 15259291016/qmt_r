from BotServer.BotFunction.InterfaceFunction import *
from BotServer.BotFunction.JudgeFuncion import *
from DbServer.DbMainServer import DbMainServer
import Config.ConfigServer as Cs
import json


class AdministratorFunction:
    def __init__(self, wcf):
        """
        超管功能
        :param wcf:
        """
        self.wcf = wcf
        self.Dms = DbMainServer()
        configData = Cs.returnConfigData()
        self.addAdminKeyWords = configData['adminFunctionWord']['addAdminWord']
        self.delAdminKeyWords = configData['adminFunctionWord']['delAdminWord']

    def mainHandle(self, message):
        content = message.content.strip()
        roomId = message.roomid
        sender = message.sender
        roomId = message.roomid
        msgType = message.type
        atUserLists, noAtMsg = getAtData(self.wcf, message)
        if msgType == 1:
            # 添加管理员
            if judgeEqualListWord(noAtMsg, self.addAdminKeyWords):
                if atUserLists:
                    for atUser in atUserLists:
                        if self.Dms.addAdmin(atUser, roomId):
                            self.wcf.send_text(
                                f'@{self.wcf.get_alias_in_chatroom(sender, roomId)}\n管理员 [{self.wcf.get_alias_in_chatroom(atUser, roomId)}] 添加成功',
                                receiver=roomId, aters=sender)
                        else:
                            self.wcf.send_text(
                                f'@{self.wcf.get_alias_in_chatroom(sender, roomId)}\n群成员 [{self.wcf.get_alias_in_chatroom(atUser, roomId)}] 已是管理员',
                                receiver=roomId, aters=sender)
            # 删除管理员
            elif judgeEqualListWord(noAtMsg, self.delAdminKeyWords):
                if atUserLists:
                    for atUser in atUserLists:
                        if self.Dms.delAdmin(atUser, roomId):
                            self.wcf.send_text(
                                f'@{self.wcf.get_alias_in_chatroom(sender, roomId)}\n管理员 [{self.wcf.get_alias_in_chatroom(atUser, roomId)}] 删除成功',
                                receiver=roomId, aters=sender)
                        else:
                            self.wcf.send_text(
                                f'@{self.wcf.get_alias_in_chatroom(sender, roomId)}\n群成员 [{self.wcf.get_alias_in_chatroom(atUser, roomId)}] 已不是管理员',
                                receiver=roomId, aters=sender)

        if "上班" in content:
            url = "http://127.0.0.1:8000/上班"
            payload = json.dumps({
                "code": content.split(" ")[-1]
            })
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': '127.0.0.1:8000',
                'Connection': 'keep-alive'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            path_str = (response.text.strip('"'))
            # 替换双反斜杠为单反斜杠
            path_str = path_str.replace("\\\\", "\\")
            self.wcf.send_file(path=path_str, receiver=roomId)
        if "下班" in content:
            url = "http://127.0.0.1:8000/下班"
            payload = json.dumps({
                "code": content.split(" ")[-1]
            })
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': '127.0.0.1:8000',
                'Connection': 'keep-alive'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            path_str = (response.text.strip('"'))
            # 替换双反斜杠为单反斜杠
            path_str = path_str.replace("\\\\", "\\")
            if os.path.exists(path_str):
                self.wcf.send_file(path=path_str, receiver=roomId)
            else:
                self.wcf.send_file(path=response.text, receiver=roomId)
        if "验证码" in content:
            url = "http://127.0.0.1:8000/验证码"
            payload = json.dumps({
                "code": content.split(" ")[-1]
            })
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': '127.0.0.1:8000',
                'Connection': 'keep-alive'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            self.wcf.send_text(response.text, receiver=message.roomid)
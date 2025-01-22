from BotServer.BotFunction.InterfaceFunction import *
from ApiServer.ApiMainServer import ApiMainServer
from BotServer.BotFunction.JudgeFuncion import *
import Config.ConfigServer as Cs
from DbServer.DbMainServer import DbMainServer


class HappyFunction:
    def __init__(self, wcf):
        """
        娱乐功能
        :param wcf:
        """
        self.wcf = wcf
        self.Ams = ApiMainServer()
        self.Dms = DbMainServer()
        configData = Cs.returnConfigData()
        self.picKeyWords = configData['functionKeyWord']['picWord']
        self.videoKeyWords = configData['functionKeyWord']['videoWord']
        self.fishKeyWords = configData['functionKeyWord']['fishWord']
        self.kfcKeyWords = configData['functionKeyWord']['kfcWord']
        self.dogKeyWords = configData['functionKeyWord']['dogWord']
        self.shortPlayWords = configData['functionKeyWord']['shortPlayWords']
        self.morningPageKeyWords = configData['functionKeyWord']['morningPageWord']
        self.eveningPageKeyWords = configData['functionKeyWord']['eveningPageWord']
        self.helpKeyWords = configData['functionKeyWord']['helpMenu']
        self.emoHelpKeyWords = configData['emoConfig']['emoHelp']
        self.emoKeyWords = configData['emoConfig']['emoKeyWord']
        self.emoOneKeyWordsData = configData['emoConfig']['onePicEmo']
        self.emoTwoKeyWordsData = configData['emoConfig']['twoPicEwo']
        self.emoRandomKeyWords = configData['emoConfig']['emoRandomKeyWord']
        self.taLuoWords = configData['functionKeyWord']['taLuoWords']
        # 自定义回复关键词字典
        self.customKeyWords = configData['customKeyWord']
        self.monitorWords = configData['functionKeyWord']['monitorWords']
        self.monitorControlWords = configData['functionKeyWord']['monitorControlWords']
        # 使用 get 方法获取配置，如果不存在则使用默认值
        adminConfig = configData.get('adminFunctionWord', {})
        # 添加监控群聊关键词
        self.addMonitorRoomKeyWords = adminConfig.get('addMonitorRoomWord', ["开启退群监控", "添加退群监控"])
        # 删除监控群聊关键词  
        self.delMonitorRoomKeyWords = adminConfig.get('delMonitorRoomWord', ["关闭退群监控", "删除退群监控"])
        # 查看监控群聊关键词
        self.showMonitorRoomKeyWords = adminConfig.get('showMonitorRoomWord', ["查看监控群聊", "显示监控群聊"])
        # 查看退群记录关键词
        self.showLeftRecordKeyWords = adminConfig.get('showLeftRecordWord', ["谁退群了", "显示退群记录"])
        # 清空退群记录关键词
        self.clearLeftRecordKeyWords = adminConfig.get('clearLeftRecordWord', ["清空退群记录", "删除退群记录"])


    def mainHandle(self, message):
        content = message.content.strip()
        sender = message.sender
        roomId = message.roomid
        msgType = message.type
        atUserLists, noAtMsg = getAtData(self.wcf, message)
        senderName = self.wcf.get_alias_in_chatroom(sender, roomId)
        avatarPathList = []

        def jkqlkz():
            """监控群聊控制"""
            # 添加监控群聊
            if judgeEqualListWord(content, self.addMonitorRoomKeyWords):
                if self.Dms.addMonitorRoom(roomId, getIdName(self.wcf, roomId)):
                    self.wcf.send_text(f'@{senderName} 添加退群监控成功!', receiver=roomId, aters=sender)
                    # 保存当前群成员列表
                    members = self.wcf.get_chatroom_members(roomId)
                    if members:
                        member_info = []
                        for member_id, member_name in members.items():
                            member_info.append((member_id, member_name))
                        self.wcf.save_members(roomId, member_info)
                else:
                    self.wcf.send_text(f'@{senderName} 此群已在监控列表中!', receiver=roomId, aters=sender)

        def scjkql():
            """删除监控群聊"""
            if judgeEqualListWord(content, self.delMonitorRoomKeyWords):
                if self.Dms.delMonitorRoom(roomId):
                    self.wcf.send_text(f'@{senderName} 删除退群监控成功!', receiver=roomId, aters=sender)
                else:
                    self.wcf.send_text(f'@{senderName} 此群未开启监控!', receiver=roomId, aters=sender)

        def ckjkql():
            """查看监控群聊"""
            monitorRoomData = self.Dms.showMonitorRoom()
            if monitorRoomData:
                msg = '===== 监控群聊列表 =====\n'
                for m_roomId, roomName in monitorRoomData.items():
                    msg += f'群聊ID: {m_roomId}\n群聊名称: {roomName}\n---------------\n'
            else:
                msg = '暂无监控群聊'
            self.wcf.send_text(msg, receiver=roomId)

        def cktqjl():
            """查看退群记录"""
            if judgeEqualListWord(content, self.showLeftRecordKeyWords):
                records = self.Dms.getLeftMemberRecords(roomId)
                if records:
                    msg = '===== 退群记录 =====\n'
                    for record in records:
                        msg += f'成员ID: {record["member_id"]}\n'
                        msg += f'成员昵称: {record["member_name"]}\n'
                        msg += f'退群时间: {record["left_time"]}\n'
                        msg += '---------------\n'
                else:
                    msg = '暂无退群记录'
                self.wcf.send_text(msg, receiver=roomId)

        def qktqjl():
            """清空退群记录"""
            if judgeEqualListWord(content, self.clearLeftRecordKeyWords):
                if self.Dms.clearLeftMemberRecords(roomId):
                    self.wcf.send_text(f'@{senderName} 清空退群记录成功!', receiver=roomId, aters=sender)
                else:
                    self.wcf.send_text(f'@{senderName} 清空退群记录失败!', receiver=roomId, aters=sender)

        def mntp():
            if judgeEqualListWord(content, self.picKeyWords):
                picPath = self.Ams.getGirlPic()
                if not picPath:
                    self.wcf.send_text(
                        f'@{senderName} 美女图片接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_image(picPath, receiver=roomId)

        def mnsp():
            if judgeEqualListWord(content, self.videoKeyWords):
                videoPath = self.Ams.getGirlVideo()
                if not videoPath:
                    self.wcf.send_text(
                        f'@{senderName} 美女视频接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_file(videoPath, receiver=roomId)

        def myrj():
            if judgeEqualListWord(content, self.fishKeyWords):
                fishPath = self.Ams.getFish()
                if not fishPath:
                    self.wcf.send_text(
                        f'@{senderName} 摸鱼日历接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_file(fishPath, receiver=roomId)

        def fkxqs():
            # 疯狂星期四
            if judgeEqualListWord(content, self.kfcKeyWords):
                kfcText = self.Ams.getKfc()
                if not kfcText:
                    self.wcf.send_text(
                        f'@{senderName} KFC疯狂星期四接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_text(
                    f'@{senderName} {kfcText}',
                    receiver=roomId, aters=sender)

        def tgrj():
            # 舔狗日记
            if judgeEqualListWord(content, self.dogKeyWords):
                dogText = self.Ams.getDog()
                if not dogText:
                    self.wcf.send_text(
                        f'@{senderName} 舔狗日记接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_text(
                    f'@{senderName} {dogText}',
                    receiver=roomId, aters=sender)

        def zaobao():
            # 早报
            if judgeEqualListWord(content, self.morningPageKeyWords):
                morningPage = self.Ams.getMorningNews()
                if not morningPage:
                    self.wcf.send_text(
                        f'@{senderName} 早报接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_text(morningPage, receiver=roomId)

        def wanbao():
            # 晚报
            if judgeEqualListWord(content, self.eveningPageKeyWords):
                eveningPage = self.Ams.getEveningNews()
                if not eveningPage:
                    self.wcf.send_text(
                        f'@{senderName} 晚报接口出现错误, 请联系超管查看控制台输出日志 ~~~',
                        receiver=roomId, aters=sender)
                    return
                self.wcf.send_text(eveningPage, receiver=roomId)

        def djss():
            # 短剧搜索
            if judgeSplitAllEqualWord(content, self.shortPlayWords):
                playName = content.split(' ')[-1]
                content = self.Ams.getShortPlay(playName)
                if content:
                    self.wcf.send_text(f'@{senderName}\n{content}', receiver=roomId, aters=sender)

        def dyspjx():
            # 抖音视频解析
            if judgeInWord(content, '复制打开抖音'):
                videoPath = self.Ams.getVideoAnalysis(content)
                if videoPath:
                    self.wcf.send_file(path=videoPath, receiver=roomId)

        def tlp():
                if judgeEqualListWord(content, self.taLuoWords):
                    content, picPath = self.Ams.getTaLuo()
                    if content and picPath:
                        self.wcf.send_image(path=picPath, receiver=roomId)
                        self.wcf.send_text(f'@{senderName}\n\n{content}', receiver=roomId, aters=sender)
                    else:
                        self.wcf.send_text(f'@{senderName}\n塔罗牌占卜接口出现错误, 请联系超管查看控制台输出 ~~~', receiver=roomId, aters=sender)

        def sjbq():
            # 随机表情
            if judgeEqualListWord(content, self.emoRandomKeyWords):
                avatarPathList.append(getUserPicUrl(self.wcf, sender))
                emoPath, sizeBool = self.Ams.getEmoticon(avatarPathList)
                if not emoPath:
                    return
                if sizeBool:
                    self.wcf.send_emotion(path=emoPath, receiver=roomId)
                else:
                    self.wcf.send_image(path=emoPath, receiver=roomId)

        def bqbgn():
            # 表情包功能 不@制作表情
            if not atUserLists and judgeSplitAllEqualWord(content, self.emoKeyWords):
                avatarPathList.append(getUserPicUrl(self.wcf, sender))
                emoMeme = self.emoOneKeyWordsData.get(content.split(' ')[-1])
                emoPath, sizeBool = self.Ams.getEmoticon(avatarPathList, emoMeme)
                if not emoPath:
                    return
                if sizeBool:
                    self.wcf.send_emotion(path=emoPath, receiver=roomId)
                else:
                    self.wcf.send_image(path=emoPath, receiver=roomId)

        def zzdfbq():
            # 表情包功能 @制作对方表情
            if atUserLists and judgeSplitAllEqualWord(noAtMsg, self.emoKeyWords):
                for atUser in atUserLists:  # 获取@的用户头像
                    avatarPathList.append(getUserPicUrl(self.wcf, atUser))
                    break
                emoMeme = self.emoOneKeyWordsData.get(noAtMsg.split(' ')[-1])
                emoPath, sizeBool = self.Ams.getEmoticon(avatarPathList, emoMeme)
                if not emoPath:
                    return
                if sizeBool:
                    self.wcf.send_emotion(path=emoPath, receiver=roomId)
                else:
                    self.wcf.send_image(path=emoPath, receiver=roomId)

        def srbq():
            # 表情包功能 @对方制作双人表情
            if atUserLists and judgeEqualListWord(noAtMsg, self.emoTwoKeyWordsData.keys()):
                avatarPathList.append(getUserPicUrl(self.wcf, sender))
                avatarPathList.append(getUserPicUrl(self.wcf, atUserLists[0]))
                emoMeme = self.emoTwoKeyWordsData.get(noAtMsg.split(' ')[-1])
                emoPath, sizeBool = self.Ams.getEmoticon(avatarPathList, emoMeme)
                if not emoPath:
                    return
                if sizeBool:
                    self.wcf.send_emotion(path=emoPath, receiver=roomId)
                else:
                    self.wcf.send_image(path=emoPath, receiver=roomId)

        def zdyhf():
            # 自定义回复
            if judgeEqualListWord(content, self.customKeyWords.keys()):
                for keyWord in self.customKeyWords.keys():
                    if judgeEqualWord(content, keyWord):
                        replyMsgLists = self.customKeyWords.get(keyWord)
                        for replyMsg in replyMsgLists:
                            self.wcf.send_text(replyMsg, receiver=roomId)

        def bqcd():
            # 表情菜单
            if judgeEqualListWord(content, self.emoHelpKeyWords):
                msg = '【单人表情】使用方法: \n表情 表情选项\n@某人 表情选项\n单人表情选项如下: \n'
                for oneEmoKey in self.emoOneKeyWordsData.keys():
                    msg += oneEmoKey + '\n'
                msg += '【双人表情】使用方法: \n表情选项@某人 \n双人表情选项如下\n'
                for twoEmoKey in self.emoTwoKeyWordsData.keys():
                    msg += twoEmoKey + '\n'
                self.wcf.send_text(f'@{senderName}\n{msg}', receiver=roomId, aters=sender)
        def help():
            # 帮助菜单
            if judgeEqualListWord(content, self.helpKeyWords):
                helpMsg = '[爱心]=== N助手菜单 ===[爱心]\n'
                helpMsg += '【一、积分功能】\n1.1、Ai画图(@机器人 画一张xxxx)\n1.2、Ai对话(@机器人即可)\n1.3、IP溯源(溯源 ip)\n1.4、IP威胁查询(ip查询 ip)\n1.5、CMD5查询(md5查询 xxx)\n1.6、签到(签到)\n1.7、积分查询(积分查询)\n\n'
                helpMsg += '【二、娱乐功能】\n2.1、美女图片(图片)\n2.2、美女视频(视频)\n2.3、摸鱼日历(摸鱼日历)\n2.4、舔狗日记(舔我)\n2.5、早报(早报)\n2.6、晚报(晚报)\n2.6、表情列表(表情列表)\n2.7、随机表情(随机表情, 有几率报错)\n'
                helpMsg += '[爱心]=== N助手菜单 ===[爱心]\n'
                self.wcf.send_text(f'@{senderName}\n{helpMsg}', receiver=roomId, aters=sender)

        TASK = [
            {"keyword": self.picKeyWords, "description": "美女图片", "func": mntp},
            {"keyword": self.videoKeyWords, "description": "美女视频", "func": mnsp},
            {"keyword": self.fishKeyWords, "description": "摸鱼日历", "func": myrj},
            {"keyword": self.kfcKeyWords, "description": "疯狂星期四", "func": fkxqs},
            {"keyword": self.dogKeyWords, "description": "舔狗日记", "func": tgrj},
            {"keyword": self.morningPageKeyWords, "description": "早报", "func": zaobao},
            {"keyword": self.eveningPageKeyWords, "description": "晚报", "func": wanbao},
            {"keyword": self.shortPlayWords, "description": "短剧搜索", "func": djss},
            {"keyword": ['复制打开抖音'], "description": "短剧搜索", "func": dyspjx},
            {"keyword": self.taLuoWords, "description": "塔罗牌占卜", "func": tlp},
            {"keyword": self.emoRandomKeyWords, "description": "随机表情", "func": sjbq},
            {"keyword": self.emoKeyWords, "description": "表情包功能", "func": bqbgn},
            {"keyword": self.emoKeyWords, "description": "表情包功能@对方", "func": zzdfbq},
            {"keyword": self.emoTwoKeyWordsData, "description": "双人表情", "func": srbq},
            {"keyword": self.customKeyWords, "description": "自定义回复", "func": zdyhf},
            {"keyword": self.emoHelpKeyWords, "description": "表情菜单", "func": bqcd},
            {"keyword": self.helpKeyWords, "description": "帮助菜单", "func": help},
            {"keyword": self.addMonitorRoomKeyWords, "description": "添加监控群聊", "func": jkqlkz},
            {"keyword": self.delMonitorRoomKeyWords, "description": "删除监控群聊", "func": scjkql},
            {"keyword": self.showMonitorRoomKeyWords, "description": "查看监控群聊", "func": ckjkql},
            {"keyword": self.showLeftRecordKeyWords, "description": "查看退群记录", "func": cktqjl},
            {"keyword": self.clearLeftRecordKeyWords, "description": "清空退群记录", "func": qktqjl},
        ]

        if msgType == 1:
            for task in TASK:
                if content in task['keyword']:
                    task['func']()
        elif msgType == 49:
            objectId, objectNonceId = getWechatVideoData(content)
            if objectId and objectNonceId:
                msg = self.Ams.getWechatVideo(objectId, objectNonceId)
                if msg:
                    self.wcf.send_text(f'@{senderName}\n{msg}', receiver=roomId, aters=sender)
        elif msgType == 10000 and "退出了群聊" in content:
            # 获取上一次保存的群成员列表
            last_members = self.wcf.get_last_members(roomId)
            if last_members:
                # 获取当前群成员列表
                current_members = self.wcf.get_chatroom_members(roomId)
                if current_members:
                    # 找出退群的成员
                    for member_id in last_members:
                        if member_id not in current_members:
                            # 添加退群记录
                            member_name = self.wcf.get_alias_in_chatroom(member_id, roomId) or member_id
                            self.Dms.addLeftMemberRecord(roomId, member_id, member_name)
                            # 发送退群通知
                            self.wcf.send_text(
                                f'检测到成员退群:\n成员ID: {member_id}\n成员昵称: {member_name}',
                                receiver=roomId
                            )
                    # 更新群成员列表
                    member_info = []
                    for member_id, member_name in current_members.items():
                        member_info.append((member_id, member_name))
                    self.wcf.save_members(roomId, member_info)












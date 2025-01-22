def save_members(self, room_id, members):
    """
    保存群成员列表
    :param room_id: 群ID
    :param members: 成员列表
    """
    member_info = []
    for member in members:
        name = self.get_alias_in_chatroom(member, room_id) or member
        member_info.append((member, name))
    return self.DbRoom.saveRoomMembers(room_id, member_info)

def get_last_members(self, room_id):
    """
    获取上次保存的群成员列表
    :param room_id: 群ID
    :return: 成员列表或None
    """
    return self.DbRoom.getRoomMembers(room_id) 
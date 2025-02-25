import os
import sys
import yaml

def resource_path(relative_path):
    """
    获取资源的实际路径，适用于开发和打包后的环境。
    :param relative_path: 相对于项目根目录的相对路径。
    :return: 资源的实际路径。
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # 如果不是通过 PyInstaller 打包运行，则使用正常的路径
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def returnConfigPath():
    """
    返回配置文件夹路径
    :return:
    """
    config_relative_path = 'Config'  # 假设 Config 文件夹在项目的根目录下
    configPath = resource_path(config_relative_path)
    return configPath

def returnConfigData():
    """
    返回配置文件数据（YAML格式）
    :return:
    """
    try:
        current_path = returnConfigPath()
        with open(os.path.join(current_path, 'Config.yaml'), mode='r', encoding='UTF-8') as file:
            configData = yaml.safe_load(file)
        return configData
    except FileNotFoundError:
        print(f"Error: Config.yaml not found at {os.path.join(current_path, 'Config.yaml')}")
        return None
    except Exception as e:
        print(f"Error reading Config.yaml: {e}")
        return None

def returnFingerConfigData():
    """
    返回指纹配置文件数据
    :return:
    """
    current_path = returnConfigPath()
    try:
        with open(os.path.join(current_path, 'Finger.yaml'), mode='r', encoding='UTF-8') as file:
            configData = yaml.safe_load(file)
        return configData
    except FileNotFoundError:
        print(f"Error: Finger.yaml not found at {os.path.join(current_path, 'Finger.yaml')}")
        return None
    except Exception as e:
        print(f"Error reading Finger.yaml: {e}")
        return None

def returnFeishuConfigData():
    """
    返回飞书配置文件数据
    :return:
    """
    current_path = returnConfigPath()
    try:
        with open(os.path.join(current_path, 'Feishu.yaml'), mode='r', encoding='UTF-8') as file:
            configData = yaml.safe_load(file)
        return configData
    except FileNotFoundError:
        print(f"Error: Feishu.yaml not found at {os.path.join(current_path, 'Feishu.yaml')}")
        return None
    except Exception as e:
        print(f"Error reading Feishu.yaml: {e}")
        return None

def saveFeishuConfigData(configData):
    """
    保存飞书配置
    :param configData:
    :return:
    """
    current_path = returnConfigPath()
    try:
        with open(os.path.join(current_path, 'Feishu.yaml'), mode='w', encoding='UTF-8') as file:
            yaml.dump(configData, file)
    except Exception as e:
        print(f"Error saving Feishu.yaml: {e}")

def returnRoomMsgDbPath():
    return os.path.join(returnConfigPath(), 'RoomMsg.db')

def returnUserDbPath():
    return os.path.join(returnConfigPath(), 'User.db')

def returnRoomDbPath():
    return os.path.join(returnConfigPath(), 'Room.db')

def returnGhDbPath():
    return os.path.join(returnConfigPath(), 'Gh.db')

def returnPointDbPath():
    return os.path.join(returnConfigPath(), 'Point.db')
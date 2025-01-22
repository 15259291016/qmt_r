from BotServer.MainServer import MainServer
from cprint import cprint

Bot_Logo = """
    _______  _______  _______  _______  _______  _______  _______  _______
"""

if __name__ == '__main__':
    cprint.info(Bot_Logo.strip())
    try:
        Ms = MainServer()
        Ms.processMsg()
    except KeyboardInterrupt:
        Ms.Pms.stopPushServer()

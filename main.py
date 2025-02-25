from BotServer.MainServer import MainServer
from cprint import cprint
import uvicorn
import threading

Bot_Logo = """
    _______  _______  _______  _______  _______  _______  _______  _______
"""



def run_main_server():
    Ms = MainServer()
    Ms.processMsg()


if __name__ == '__main__':
    cprint.info(Bot_Logo.strip())

    # 创建并启动 MainServer 线程
    main_server_thread = threading.Thread(target=run_main_server)
    main_server_thread.start()
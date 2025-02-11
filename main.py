from BotServer.MainServer import MainServer
from cprint import cprint
import uvicorn
import threading

Bot_Logo = """
    _______  _______  _______  _______  _______  _______  _______  _______
"""


def run_app():
    try:
        from modules.fapp.app import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
        print("成功启动")
    except ImportError as e:
        print(e)


def run_main_server():
    Ms = MainServer()
    Ms.processMsg()


if __name__ == '__main__':
    cprint.info(Bot_Logo.strip())

<<<<<<< HEAD

=======
>>>>>>> e087e014910e90fe51c437b9f2755d67175880e0
    # 创建并启动 MainServer 线程
    main_server_thread = threading.Thread(target=run_main_server)
    main_server_thread.start()

    # 等待两个线程完成
    run_app()
    main_server_thread.join()
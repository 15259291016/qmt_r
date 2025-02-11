from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any
import requests
import json
import time
import pywencai as pywc
from queue import Queue
from DrissionPage import ChromiumPage, ChromiumOptions
from threading import Thread
import time

# 创建 FastAPI 应用实例
app = FastAPI()
co = ChromiumOptions().auto_port()  # 指定程序每次使用空闲的端口和临时用户文件夹创建浏览器
# co.headless(True)  # 无头模式
# co.set_argument('--no-sandbox')  # 无沙盒模式
# co.set_argument('--headless=new')  # 无界面系统添加
# co.set_paths(browser_path="/usr/bin/google-chrome")  # 设置浏览器路径
page = ChromiumPage(co)
page.get("https://om.tencent.com/attendances/check_out/23301583")
tab1 = page.get_tab()
q = Queue()
res = dict()
tab1.wait.doc_loaded()
try:
    tab1('x://html/body/div/div/div[4]/form/div[3]/div/div/div[2]/div[2]/button').click('js')  # 简化写法
except Exception as e:
    print(e)
tab1.ele("#username").input("v_zhicniu")
tab1.ele("#password_input").input(f"611698{126895}")
tab1('x://html/body/div[4]/div/div/div[4]/span').click('js')  # 简化写法
# tab1.ele("#checkout_btn").click('js')

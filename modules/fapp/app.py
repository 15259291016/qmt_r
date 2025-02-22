import os.path

from fastapi import FastAPI
from typing import Dict, Any
import pywencai as pywc
from queue import Queue
from DrissionPage import ChromiumPage, ChromiumOptions
from threading import Thread
import time
import asyncio

# 创建 FastAPI 应用实例
app = FastAPI()
# ----------------
短视频_co = ChromiumOptions().auto_port()  # 指定程序每次使用空闲的端口和临时用户文件夹创建浏览器
# 短视频_co.headless(True)  # 无头模式
# 短视频_co.set_argument('--no-sandbox')  # 无沙盒模式
# 短视频_co.set_argument('--headless=new')  # 无界面系统添加
短视频_page = ChromiumPage(短视频_co)
短视频_page.get("https://www.xiazaitool.com/dy")
短视频_tab1 = 短视频_page.get_tab()
q = Queue()
签到信息队列 = Queue()
res = dict()
签到结果字典 = dict()
短视频_tab1('x://html/body/div[2]/nav/div/div/ul[2]/li[2]/a').click('js')  # 简化写法
jym = 短视频_tab1.ele('#verifyImg', timeout=5).src
jym_str = ""
while jym_str == "":
    jym_str = str(jym).split(" ")[8][5:-1]
    print(jym_str)
    time.sleep(1)
a = input("请输入一个值:")
print(a)

短视频_tab1.ele("#account").input("19026045487")
短视频_tab1.ele("#password").input("6116988.niu")
短视频_tab1.ele("#imgCode").input(a)
短视频_tab1.ele("#get_login").click('js')
短视频_tab1.wait.doc_loaded()
# -----------------------------------
co_qd = ChromiumOptions().auto_port()  # 指定程序每次使用空闲的端口和临时用户文件夹创建浏览器
# co_qd.headless(True)  # 无头模式
# co_qd.set_argument('--no-sandbox')  # 无沙盒模式
# co_qd.set_argument('--headless=new')  # 无界面系统添加
# co_qd.set_paths(browser_path="/usr/bin/google-chrome")  # 设置浏览器路径
page_qd = ChromiumPage(co_qd)

page_qd.get("https://om.tencent.com/attendances/check_out/23301583")
tab1_qd = page_qd.get_tab()
tab1_qd.wait.doc_loaded()
def consumer(tab1, q):
    while True:
        word_list = q.get()
        count = 0
        tab1.refresh()  # 刷新页面
        tab1.ele("#button-addon2").click('js')          # 清楚输入框
        tab1.ele("#urlInput").input(word_list)          # 输入查询条件

        while "a" not in res and count < 5:
            count += 1
            tab1.ele("#downloadButton").click('js')  # 点击查询
            # tab1.wait.doc_loaded()
            # tab1.wait.ele_hidden("#waitAnimation")  # 等待查询结果
            # time.sleep(1)
            # tab1.ele("#downloadButton").click('js')
            source = tab1.ele('tag:source')
            images = tab1.eles('.preview-image')
            if source:
                res["a"] = {"videourl": source.attr("src"), "type": "video"}
                continue
            if images:
                res["a"] = {"imagesurl": [image.attr("src") for image in images], "type": "image"}
                continue
            try:
                if "解析失败" in tab1("x://html/body/div[2]/div/div/div[2]").text or "网络不稳定" in tab1("x://html/body/div[2]/div/div/div[2]").text:
                    res["a"] = {"info": "解析失败", "type": "text"}
                    tab1("x://html/body/div[2]/div/div/div[3]/button").click('js')
                    continue
            except Exception as e:
                print(e)
            
        time.sleep(10)


def 上班下班线程(tab1, 签到信息队列):
    while True:
        word_list = 签到信息队列.get()
        count = 0
        while "a" not in 签到结果字典 and count < 5:
            tab1.refresh()  # 刷新页面
            发起验证按钮 = tab1.ele(".tfa-button")
            if 发起验证按钮:
                发起验证按钮.click("js")
                time.sleep(20)
                签到结果字典["a"] = "点击了发起验证按钮"
                continue
            count += 1
            tab1.ele("#downloadButton").click('js')  # 点击查询
            tab1.wait.doc_loaded()
            tab1.wait.ele_hidden("#waitAnimation")  # 等待查询结果
            time.sleep(1)
            tab1.ele("#downloadButton").click('js')
            source = tab1.ele('tag:source')
            images = tab1.eles('.preview-image')
            if source:
                res["a"] = {"videourl": source.attr("src"), "type": "video"}
                continue
            if images:
                res["a"] = {"imagesurl": [image.attr("src") for image in images], "type": "image"}
                continue
            try:
                if "解析失败" in tab1("x://html/body/div[2]/div/div/div[2]").text or "网络不稳定" in tab1(
                        "x://html/body/div[2]/div/div/div[2]").text:
                    res["a"] = {"info": "解析失败", "type": "text"}
                    tab1("x://html/body/div[2]/div/div/div[3]/button").click('js')
                    continue
            except Exception as e:
                print(e)

# 创建一个 POST 接口来接收 User 数据
@app.post("/短视频爬虫")
async def 短视频爬虫(item: Dict[str, Any]):
    info = item.get("info", "")
    if info == "":
        return {"error": "info is empty!"}
    global q
    q.put(info)
    while True:
        if "a" in res:
            re = res["a"]
            res.pop("a")
            return {
                "data": re
                }
        await asyncio.sleep(0.1)


@app.post("/wc")
async def wc(item: Dict[str, Any]):
    stock_name = item['params'].get("stock_name", "")
    res = pywc.get(query=f"{stock_name}散户指标")
    return {
        "data": str(res)
        }


@app.post("/上班")
async def 上班(item: Dict[str, Any]):
    global co_qd, page_qd, tab1_qd
    # co_qd = ChromiumOptions().auto_port()  # 指定程序每次使用空闲的端口和临时用户文件夹创建浏览器
    # co_qd.headless(True)  # 无头模式
    # co_qd.set_argument('--no-sandbox')  # 无沙盒模式
    # co_qd.set_argument('--headless=new')  # 无界面系统添加
    # co_qd.set_paths(browser_path="/usr/bin/google-chrome")  # 设置浏览器路径
    try:
        # page_qd = ChromiumPage(co_qd)

        page_qd.get("https://om.tencent.com/attendances/check_out/23301583")
        tab1_qd = page_qd.get_tab()
        tab1_qd.wait.doc_loaded()
        发起验证按钮 = tab1_qd.ele(".tfa-button")
        if 发起验证按钮:
            发起验证按钮.click("js")
            return "点击了发起验证按钮"
        code = item.get("code", "")
        tab1_qd.ele("#username").input("v_zhicniu")
        tab1_qd.ele("#password_input").input(f"611698{code}")
        tab1_qd.ele("#login_button").click('js')
        tab1_qd('x://html/body/div[4]/div/div/div[4]/span').click('js')  # 简化写法
        return "成功"
    except Exception as e:
        print(e)
        return e


@app.post("/下班")
async def 下班(item: Dict[str, Any]):
    global co_qd, page_qd, tab1_qd
    # co_qd = ChromiumOptions().auto_port()  # 指定程序每次使用空闲的端口和临时用户文件夹创建浏览器
    # co_qd.headless(True)  # 无头模式
    # co_qd.set_argument('--no-sandbox')  # 无沙盒模式
    # co_qd.set_argument('--headless=new')  # 无界面系统添加
    # co_qd.set_paths(browser_path="/usr/bin/google-chrome")  # 设置浏览器路径
    # page_qd = ChromiumPage(co_qd)

    # page_qd.get("https://om.tencent.com/attendances/check_out/23301583")
    # tab1_qd = page_qd.get_tab()
    # tab1_qd.wait.doc_loaded()
    code = item.get("code", "")

    发起验证按钮 = tab1_qd.ele(".tfa-button")
    if 发起验证按钮:
        发起验证按钮.click("js")
        time.sleep(20)
        tab1_qd.ele("#username").input("v_zhicniu")
        tab1_qd.ele("#password_input").input(f"611698{code}")
        tab1_qd.ele("#login_button").click('js')
        下班按钮 = tab1_qd('x://html/body/div[4]/div/div/div[4]/span')
        if 下班按钮:
            下班按钮.click('js')  # 简化写法
            return "下班成功"

    tab1_qd.ele("#username").input("v_zhicniu")
    tab1_qd.ele("#password_input").input(f"611698{code}")
    tab1_qd.ele("#login_button").click('js')
    tab1_qd('x://html/body/div[4]/div/div/div[4]/span').click('js')  # 简化写法
    try:
        img = tab1_qd.ele("#image")
        if img:
            f_path = img.save(path=os.path.join("FileCache"), name=f"qd{code}.png")
            return f_path
        tab1_qd("x://html/body/div[7]/div[3]/div/a[1]").click('js')
        return "成功"
    except Exception as e:
        print(e)
        tab1_qd("x://html/body/div[7]/div[3]/div/a[1]").click('js')
        return "成功"


@app.post("/验证码")
async def 验证码(item: Dict[str, Any]):
    global tab1_qd
    code = item.get("code", "")
    tab1_qd.ele("#code_input").input(code)
    tab1_qd("x://html/body/div[7]/div[3]/div/a[1]").click('js')
    return "成功"


@app.post("/tjwc")
async def tjwc(item: Dict[str, Any]):
    info = item['params'].get("info", "")
    res = pywc.get(query=f"{info}")
    return {
        "data": str(res)
        }

Thread(target=consumer, args=(短视频_tab1, q)).start()          # chrome浏览器
# Thread(target=上班下班线程, args=(tab1_qd, 签到信息队列)).start()          # chrome浏览器

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20
# @Author  : Soner
# @version : 1.0.0


from appium import webdriver
from Providers.get_port import PortInfo
from Providers.device_info import MachinePool
from Providers.logger import Logger, error_format
from threading import Lock

import time
import os
import subprocess

log = Logger("server_info").getlog()
# 获取当前路径
now_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
port_info = PortInfo()
devices = MachinePool()

lock = Lock()


def stater():
    global port_info, devices, lock
    try:
        with lock:
            # 生成 所需的端口
            device = devices.get_device()
            while not device:
                time.sleep(5)
                device = devices.get_device()
                if device:
                    break

            version = devices.get_version(device)
            port = port_info.get_port()
            bport = port_info.get_bport()
            sys_port = port_info.get_sys_port()
            chrome_port = port_info.get_chrome_port()

        # 开启 appium 服务
        status = start_server(port, bport, chrome_port, device)

        desired_caps = {
            "platformName": "Android",
            "deviceName": device,
            "udid": device,
            "platformVersion": version,
            "appPackage": "com.tianyancha.skyeye",
            # 启动driver前需要卸载的包，可以是 单个、列表、*
            "uninstallOtherPackages": "com.tianyancha.skyeye",
            "appActivity": ".activity.SplashActivity",
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            # 是否重置应用程序状态
            # 'noReset': True,
            # 禁止重签名
            "noSign": True,
            # 让appium自动授权app权限, 不能和noReset同时使用
            "autoGrantPermissions": True,
            # 获取toast必须添加配置项
            "automationName": "UiAutomator2",
            "app": now_dir + "/app/android.apk",
            # 移至非ChromeDriver Web视图时，终止ChromeDriver会话
            "recreateChromeDriverSessions": True,
            "systemPort": sys_port,
        }
        # appium 服务开启
        while status:
            remote = "http://127.0.0.1:{}/wd/hub".format(port)
            driver = webdriver.Remote(remote, desired_caps)
            break

        # 检测是否安装搜狗输入法
        if driver.is_app_installed("appPackage=com.iflytek.inputmethod.google"):
            log.info("设备 {} 已经安装讯飞输入法特别版".format(device))
        else:
            log.info("设备 {} 未安装，执行安装讯飞输入法特别版".format(device))
            driver.install_app(now_dir+"/app/ifly.apk")
        log.info("成功开启driver：{}".format(remote))
        return driver, device, port
    except Exception as e:
        log.error(error_format(e))
        devices.release_device(device)


def start_server(port, bport, chrome_port, device):
    cmd = "appium --session-override -p {} -bp {} --chromedriver-port {} -U {}".format(
        port, bport, chrome_port, device
    )
    status = None
    appium = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        close_fds=True,
    )
    log.info("执行启动命令：{}".format(cmd))
    while True:
        appium_line = appium.stdout.readline().strip().decode()
        if "listener started" in appium_line or "Error: listen" in appium_line:
            log.info("----server_ 成功---")
            status = True
            break

    return status


def stop_device(name):
    """
    释放设备
    """
    global devices
    devices.release_device(name)


def stop_server(port):
    """
    释放服务
    """
    pid = ""
    cmd = "lsof -i :{}".format(port)
    cmd = "lsof -sTCP:LISTEN -i:{} -t".format(port)
    pid = os.popen(cmd).readline().strip("\n")
    if pid != "":
        os.popen("kill -9 {}".format(pid))
        log.info("端口：{} 的 PID：{} 被释放".format(port, pid))
    else:
        log.error("端口：{} 的 PID：{} 获取失败".format(port, pid))

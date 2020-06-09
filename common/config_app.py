# -*- coding: utf-8 -*-
# @Time    : 2019-09-22 09:37
# @Author  : ZYF
# @File    : config_app.py

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.readconfig import ReadConfig
# from Providers.operation_server import Operation_Server
import re
import os

class Config_app(object):
    def __init__(self):
        # 获取 aapt 命令位置
        abd_path = os.popen('adb --version').readlines()[2].split(' ')[2].strip('\n')
        android_path = os.path.dirname(os.path.dirname(abd_path))
        files = os.listdir(android_path + '/build-tools')
        aapt_path = ""
        for f in files:
            if os.path.exists(android_path + '/build-tools/' + f + '/aapt'):
                aapt_path = android_path + '/build-tools/' + f + '/aapt'
                break
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        appLocation = self.BASE_DIR + "/app/android.apk"
        # 读取设备 id
        readDeviceId = list(os.popen('adb devices').readlines())
        # 正则表达式匹配出 id 信息
        self.deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
        # 读取设备系统版本号
        deviceAndroidVersion = list(os.popen('adb shell getprop ro.build.version.release').readlines())
        self.deviceVersion = re.findall(r'^\w*\b', deviceAndroidVersion[0])[0]
        if aapt_path:
            # 读取 APK 的 package 信息
            appPackageAdb = list(os.popen(aapt_path + ' dump badging ' + appLocation).readlines())
            # self.appPackage = re.findall(r'\'com\w*.*?\'', appPackageAdb[0])[0]
            self.a_list = []
            for i in appPackageAdb:
                appPackage = re.findall(r'\'com.tianyancha\w*.*?\'', i)
                if appPackage and (not appPackage in self.a_list):
                    self.a_list = self.a_list + appPackage
            if "'com.tianyancha.skyeye.permission.MIPUSH_RECEIVE'" in self.a_list:
                self.a_list.remove("'com.tianyancha.skyeye.permission.MIPUSH_RECEIVE'")

        # Operation_Server().start_appium()

    def Android(self):
        try:
            print('启动Android')
            # 设备及安装包信息
            desired_caps = {
                'platformName': 'Android',
                'deviceName': self.deviceId,
                'platformVersion': self.deviceVersion,
                'appPackage': self.a_list[0].replace("'", ""),
                'appActivity': self.a_list[1].replace("'", ""),
                # 'appWaitActivity': 'com.tianyancha.skyeye.MainActivity',
                'unicodeKeyboard': True,
                'resetKeyboard': True,
                # 是否重置应用程序状态
                # 'noReset': True,
                # 禁止重签名
                'noSign': True,
                # 让appium自动授权app权限, 不能和noReset同时使用
                'autoGrantPermissions': True,
                # 获取toast必须添加配置项
                'automationName': 'Uiautomator2',
                'app': self.BASE_DIR + '/app/android.apk',
                # 移至非ChromeDriver Web视图时，终止ChromeDriver会话
                'recreateChromeDriverSessions': True,
                # 当手机已安装过uiAutomator2，可以跳过
                # 'skipServerInstallation': True,
                # 'skipDeviceInitialization': True
            }
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

            # 检测是否安装搜狗输入法
            if self.driver.is_app_installed('com.sohu.inputmethod.sogou'):
                print("已经安装搜狗输入法")
            else:
                print('未安装，执行安装搜狗输入法')
                self.driver.install_app(self.BASE_DIR + '/app/sougou.apk')
                adb1 = 'adb shell ime set io.appium.settings/.UnicodeIME'
                os.system(adb1)
            print('启动完成')
            return self.driver
        except Exception as e:
            print(e)

    def ios(self):
        platformName = 'ios'
        print('启动ios')

        # 设备及安装包信息
        desired_caps = {
            "platformName": "IOS",
            "deviceName": "“xu”的 iPhone",
            "platformVersion": "12.2",
            "bundleid": "com.jindi.zyf.wda.integrationApp",
            "app": "/Users/zhangyufeng/Downloads/NewSkyEyes.ipa",
            "udid": "00008020-000A2C3E2669002E",
            "unicodeKeyboard": "True",
            "resetKeyboard": "True",
            "noRest": False,
            "automationName": "XCUITest"
        }
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

        """监测系统弹框"""
        for i in range(5):
            loc = ("xpath", "//*[@text='始终允许']")
            # loc = ("xpath", "//*[@text='确定']")
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except:
                pass

        print('启动完成')
        return self.driver

    def config_app(self):

        r = ReadConfig()
        platformName = r.get_platformName('platformName')
        # print('platformName------', platformName)
        if platformName == 'android':
            self.driver = self.Android()
            return self.driver

        elif platformName == "ios":
            self.driver = self.ios()
            return self.driver

if __name__ == '__main__':
    d = Config_app() #读取的是配置文件 调试的时候手动写入
    d.config_app()

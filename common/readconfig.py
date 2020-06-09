# -*- coding: utf-8 -*-
# @Time    : 2019-09-22 15:24
# @Author  : ZYF
# @File    : readconfig.py


import os
import codecs
import configparser

# 获取该文件的真实路径,然后分割路径和文件名存入一个元祖
proDir = os.path.split(os.path.realpath(__file__))[0]
# 获取上层目录
parDir = os.path.dirname(proDir)

configPath = os.path.join(parDir, "config.ini")


# print("prodir:",proDir,configPath)


class ReadConfig(object):
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding="utf-8-sig")

    # 获取配置文件中的分组（eg:EMAIL）中的对应选项(eg:name)的值
    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_ftp(self, name):
        value = self.cf.get("FTP", name)
        return value

    # 手机设备
    def get_platformName(self, name):
        value = self.cf.get("platformName", name)
        return value

# 测试类用
# p = ReadConfig()
# print(p.get_platformName('platformName'))
# print(p.get_screen('switch'))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/19
# @Author  : Soner
# @version : 1.0.0

from Providers.logger import Logger


log = Logger("server_info").getlog()
class PortInfo():
    def __init__(self):
        self.port = 4723
        self.bport = 4823
        self.sys_port = 8200
        self.chrome_port = 5113

    def get_port(self):
        """
        获取 port 端口
        """
        self.port = self.port + 2
        log.info("获取port端口：{}".format(self.port))
        return self.port


    def get_bport(self):
        """
        获取 bport 端口
        """
        self.bport = self.bport + 2
        log.info("获取bport端口：{}".format(self.bport))
        return self.bport


    def get_sys_port(self):
        """
        获取 系统 端口
        """
        self.sys_port = self.sys_port + 2
        log.info("获取sys_port端口：{}".format(self.sys_port))
        return self.sys_port


    def get_chrome_port(self):
        """
        获取 ChromeDriverPort端口
        """
        self.chrome_port = self.chrome_port + 2
        log.info("获取chromd_port端口：{}".format(self.chrome_port))
        return self.chrome_port



if __name__ == '__main__':
    port = PortInfo()
    for i in range(0,10):
        print(port.get_port())
        print(port.get_bport())
        print(port.get_sys_port())
        print(port.get_chrome_port())




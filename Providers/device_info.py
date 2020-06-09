#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/18
# @Author  : Soner
# @version : 1.0.0


import os
import json
import random
from Providers.phone_info import PhoneInfo
from Providers.logger import Logger


log = Logger("device_info").getlog()

driver_dict = {}
class MachinePool():
    #  获取项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file = BASE_DIR + '/config/driver_list.json'
    config_file = BASE_DIR + '/config/'
    phone = PhoneInfo()

    def init(self):
        global driver_dict

        data = {}
        # self.driver_dict = {}
        # 判断文件是否存在
        if not os.path.isfile(self.file):
            # 判断文件夹是否存在
            if not os.path.exists(self.config_file):
                os.mkdir(self.config_file)
            with open(self.file, 'w', encoding='UTF-8') as f:
                json.dump(data, f)
        # 判断文件是否为空
        if not os.path.getsize(self.file):
            with open(self.file, 'w', encoding='UTF-8') as f:
                json.dump(data, f)
        # 初始化设备列表，设置状态
        self.change_device()

        log.info("初始化设备列表：{}".format(driver_dict))



    def _load_json(self):
        # 判断文件夹是否存在
        if not os.path.exists(self.config_file):
            os.mkdir(self.config_file)
            with open(self.file, 'w', encoding='UTF-8') as f:
                json.dump(dict(), f)

        with open(self.file, 'r', encoding='UTF-8') as f:
            driver_json = json.load(f)
        return driver_json

    def _dump_json(self, driver_dict):
        # 判断文件夹是否存在
        if not os.path.exists(self.config_file):
            os.mkdir(self.config_file)

        with open(self.file, 'w', encoding='UTF-8') as f:
            json.dump(driver_dict, f)


    def change_device(self):
        """
        更新设备列表
        """
        global driver_dict

        driver_list = PhoneInfo().group_call()
        log.info('实时driver_list:{}'.format(driver_list))

        # 判断 json文件是否为空
        # 为空则，将所有设备name写入，并赋初始值0
        if not driver_dict:
            # 初始化 设备状态
            for driver in driver_list:
                driver_dict[driver] = {
                    "version":self.phone.version_number(driver),
                    "status": 0
                }
            # 更新设备列表文件
            self._dump_json(driver_dict)
        # 不为空，则判断传入的设备name是否已存在
        else:
            # 需要添加的driver设备
            add_driver_list = list(set(driver_list).difference(set(driver_dict.keys())))
            for driver in add_driver_list:
                driver_dict[driver] = {
                    "version": self.phone.version_number(driver),
                    "status": 0
                }
            # 需要移除的driver设备
            del_driver_list = list(set(driver_dict.keys()).difference(set(driver_list)))
            for key in del_driver_list:
                driver_dict.pop(key)

            # 更新设备列表文件,做备份
            self._dump_json(driver_dict)
            log.info("更新后的设备列表:{}".format(driver_dict))


    def get_device(self):
        global driver_dict
        """
        随机获取一个设备名字
        """
        self.change_device()
        driver = None
        # 获取所有key值
        driver_keys = list(driver_dict.keys())

        # 判断设备列表数量，如果只有一个并且没有被使用，将这个设备返回
        if len(driver_keys) == 1:
            if driver_dict[driver_keys[0]]["status"] == 0:
                driver = driver_keys[0]
                driver_dict[driver]['status'] = 1
            else:
                log.info("没有多余设备")
        else:
            # 将设备列表去重
            driver_status = [driver_dict[i]["status"] for i in driver_dict]
            deduplication = len(set(driver_status))
            while True:
                if deduplication <= 1 and 1 in set(driver_status):
                    log.info("没有空闲设备")
                    break
                num = random.randint(0, len(driver_keys)-1)
                if driver_dict[driver_keys[num]]["status"] == 0:
                    driver = driver_keys[num]
                    driver_dict[driver]["status"] = 1
                    # 更新设备列表文件,做备份
                    self._dump_json(driver_dict)
                    break
        log.info("获取到 {} 设备".format(driver))
        return driver


    def get_version(self, name):
        """
        返回设备系统版本号
        """
        if name in driver_dict.keys():
            version =  driver_dict[name]['version']
        else:
            version = self.phone.version_number(name)
        return version


    def release_device(self, driver_name):
        """
        释放设备
        """
        global driver_dict

        if driver_name in list(driver_dict.keys()):
            driver_dict[driver_name]["status"] = 0
            # 更新设备列表文件,做备份
            self._dump_json(driver_dict)
            log.info("设备 {} 已被释放".format(driver_name))
            log.info("释放后的列表：{}".format(driver_dict))
        else:
            log.info("传递的设备名字不存在")


    def get_status(self, flag=False):
        """
        获取设备状态
        flag：   False：设备是否有可用；True：返回可用设备数
        """
        global driver_dict

        # 获取状态先，先更新设备列表
        self.change_device()
        status = False
        usable = 0
        keys = list(driver_dict.keys())
        for key in keys:
            if driver_dict[key]["status"] == 0:
                usable += 1
                status = True
        if flag:
            return usable
        else:
            return status




if __name__ == '__main__':
    driver = MachinePool()
    driver.init()

    # import time
    #
    # for i in range(1, 6):
    #     time.sleep(5)
    #     # print("=============start=============")
    #     # 获取设备列表
    #     driver.change_device()
    #     driver_name = driver.get_device()
    #     # print("获取的driver_name:{}".format(driver_name))
    #     driver.release_device(driver_name)
    #     # print("=============end=============")
    #     print("")

    print(driver.get_status(flag=True))

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



log = Logger("MachinePool").getlog()
class MachinePool():
    def __init__(self):
        #  获取项目根目录
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file = BASE_DIR + '/config/driver_list.json'
        config_file = BASE_DIR+'/config/'

        data = {}
        self.driver_dict = {}
        # 判断文件是否存在
        if not os.path.isfile(self.file):
            # 判断文件夹是否存在
            if not os.path.exists(config_file):
                os.mkdir(config_file)
            with open(self.file, 'w', encoding='UTF-8') as f:
                json.dump(data, f)
        # 判断文件是否为空
        if not os.path.getsize(self.file):
            with open(self.file, 'w', encoding='UTF-8') as f:
                json.dump(data, f)

        self.phone = PhoneInfo()
        self.change_driver()

        log.info(self.driver_dict)



    def _load_json(self):
        with open(self.file, 'r', encoding='UTF-8') as f:
            driver_dict = json.load(f)
        return driver_dict

    def _dump_json(self, driver_dict):
        with open(self.file, 'w', encoding='UTF-8') as f:
            json.dump(driver_dict, f)


    def change_driver(self):
        """
        更新设备列表
        """
        driver_list = PhoneInfo().group_call()
        log.info('实时driver_list:{}'.format(driver_list))

        # 判断 json文件是否为空
        # 为空则，将所有设备name写入，并赋初始值0
        if not self.driver_dict:
            # 初始化 设备状态
            for driver in driver_list:
                self.driver_dict[driver] = {
                    "version":self.phone.version_number(driver),
                    "status": 0
                }
            # 更新设备列表文件
            self._dump_json(self.driver_dict)
        # 不为空，则判断传入的设备name是否已存在
        else:
            # 需要添加的driver设备
            add_driver_list = list(set(driver_list).difference(set(self.driver_dict.keys())))
            for driver in add_driver_list:
                self.driver_dict[driver] = {
                    "version": self.phone.version_number(driver),
                    "status": 0
                }
            # 需要移除的driver设备
            del_driver_list = list(set(self.driver_dict.keys()).difference(set(driver_list)))
            for key in del_driver_list:
                self.driver_dict.pop(key)

            # 更新设备列表文件,做备份
            self._dump_json(self.driver_dict)
            log.info("更新后的设备列表:{}".format(self.driver_dict))


    def get_drvier(self):
        """
        随机获取一个设备名字
        """

        # 获取所有key值
        driver_keys = list(self.driver_dict.keys())

        driver = None
        if len(driver_keys) == 1:
            if self.driver_dict[driver_keys[0]]["status"] == 0:
                driver = driver_keys[0]
            else:
                log.info("没有多余设备")
        else:
            # 将设备列表去重
            driver_status = [self.driver_dict[i]["status"] for i in self.driver_dict]
            deduplication = len(set(driver_status))
            while True:
                if deduplication <= 1 and 1 in set(driver_status):
                    log.info("没有空闲设备")
                    break
                num = random.randint(0, len(driver_keys)-1)
                if self.driver_dict[driver_keys[num]]["status"] == 0:
                    driver = driver_keys[num]
                    self.driver_dict[driver]["status"] = 1
                    # 更新设备列表文件,做备份
                    self._dump_json(self.driver_dict)
                    break
        log.info("获取到的设备名字：{}".format(driver))
        return driver


    def release_drvier(self, driver_name):
        """
        释放设备
        """

        if driver_name in self.driver_dict.keys():
            self.driver_dict[driver_name]["status"] = 0
            # 更新设备列表文件,做备份
            self._dump_json(self.driver_dict)
            log.info("设备 {} 已被释放".format(driver_name))
        else:
            log.info("传递的driver_name不存在")




if __name__ == '__main__':
    driver = MachinePool()

    import time

    for i in range(1, 6):
        time.sleep(5)
        # print("=============start=============")
        # 获取设备列表
        driver.change_driver()
        driver_name = driver.get_drvier()
        # print("获取的driver_name:{}".format(driver_name))
        driver.release_drvier(driver_name)
        # print("=============end=============")
        print("")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/7
# @Author  : Soner
# @version : 1.0.0

import os
import re
from Providers.logger import Logger, error_format


log = Logger("Phone_Info").getlog()
class PhoneInfo:
    def version_number(self, devices):
        # 读取设备系统版本号
        deviceAndroidVersion = list(
            os.popen("adb -s {} shell getprop ro.build.version.release".format(devices)).readlines()
        )
        try:
            # deviceVersion = re.findall(r"^\w*\b", deviceAndroidVersion[0])[0]
            deviceVersion = deviceAndroidVersion[0].strip("\n")
            return deviceVersion
        except Exception as e:
            log.error("设备：{} 执行cmd结果为：「{}」，发生错误：{}".format(devices, deviceAndroidVersion, error_format(e)))
            raise e

    def group_call(self):
        # 读取设备 id
        readDeviceId = list(os.popen("adb devices").readlines())
        deviceIdList = []
        for i in range(1, len(readDeviceId) - 1):
            # 正则表达式匹配出 id 信息
            deviceId = re.findall(r"^\w*\b", readDeviceId[i])[0]
            deviceIdList.append(deviceId)
        return deviceIdList


if __name__ == "__main__":
    phone_info = PhoneInfo()
    call = phone_info.group_call()
    print(call[0])
    print(phone_info.version_number(call[0]))

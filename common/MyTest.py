# -*- coding: utf-8 -*-
# @Time    : 2019-09-20 09:19
# @Author  : ZYF
# @File    : MyTest.py

"""
1.继承unittest父类，方便testcase使用
2.初始化和清理方法

"""
import unittest
from common.extend import Extend
import warnings
from Providers.skip_guide import skip_guide, agree_license
from Providers.back_to_index import back_to_index
from Providers.cancel_update import cancel_update
from Providers.statr_server import stater, stop_device, stop_server
from Providers.account.account import Account

from threading import Lock


class MyTest(unittest.TestCase):
    lock = Lock()

    @classmethod
    def setUpClass(cls):
        # 忽略waring提示
        warnings.simplefilter("ignore", ResourceWarning)
        cls.driver, cls.device, cls.port = stater()
        cls.extend = Extend(cls.driver)
        # 点击同意用户协议
        agree_license(cls.driver)
        # 跳过引导页
        skip_guide(cls.driver)
        # 跳过更新提示
        cancel_update(cls.driver)
        cls.account = Account()

    def setUp(self):
        pass

    def tearDown(self):
        # 回到首页
        back_to_index(self.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # 加锁
        with cls.lock:
            # 释放 设备 及 服务
            stop_device(cls.device)
            stop_server(cls.port)


if __name__ == "__main__":
    unittest.main()

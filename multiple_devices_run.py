# # #!/usr/bin/env python
# # # -*- coding: utf-8 -*-
# # # @Time    : 2019/11/28 17:05
# # # @Author  : Soner
# # # @version : 1.0.0

from threading import Thread, Lock
from random import randint
import unittest
import HTMLTestRunner_PY3
import time
import datetime
import os
from Providers.get_files import CaseFilses
from Providers.device_info import MachinePool
from Providers.create_sum import create_summary
from Providers.logger import Logger
from Providers.account.account import Account
from common.send_email import sendmail
from common.send_ding_message import send_message

log = Logger("main_program").getlog()
# 获取当前路径
now_dir = os.path.dirname(os.path.abspath(__file__))
# case路径
test_dir = now_dir + "/testcase"
# 报告路径
test_report = now_dir + "/report/HTML"
now = time.strftime("%Y-%m-%d-%H%M%S")
jenkins_path = "/opt/tomcat8/webapps/log/app_auto_result"


def kill_adb():
    os.popen("killall adb")
    os.popen("killall node")
    os.system("adb start-server")


def suit(case):
    global test_report
    testsuit = unittest.defaultTestLoader.discover(
        test_dir, pattern="{}.py".format(case), top_level_dir=test_dir
    )
    if os.path.exists(jenkins_path):
        test_report = jenkins_path
    # 获取当前时间
    if not os.path.exists(test_report + "/{}".format(now)):
        os.makedirs(test_report + "/{}".format(now))

    # 定义测试报告的名字
    filename = test_report + "/{}/{}_result.html".format(now, case)

    fp = open(filename, "wb")
    runner = HTMLTestRunner_PY3.HTMLTestRunner(
        stream=fp, title="APP 测试报告", description="运行环境Android"
    )
    runner.run(testsuit)
    fp.close()


def consumer(devices, case, lock):
    while True:
        with lock:
            status = devices.get_status()

        # 如果有可用设备
        if status:
            # 执行用例
            suit(case)
            log.info(" {} 被我消费了".format(case))
            break
        else:
            # 没有可用设备，则每隔10秒检测一次
            time.sleep(10)
            devices.change_device()


if __name__ == "__main__":
    start_time = time.time()
    s_time = datetime.datetime.now()
    log.info(time.strftime("开始时间：%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
    kill_adb()

    lock = Lock()
    # 初始化账户列表
    Account().init_account()
    # 获取case 文件列表
    case_list = CaseFilses()
    cases = case_list.case_files
    # 获取 case 文件数
    cases_count = len(cases)

    # 设备操作 实例化
    devices = MachinePool()
    devices.init()

    threads = []
    # case文件数 是否大于0
    while cases_count > 0:
        with lock:
            # 判断 是否有可用设备
            if not devices.get_status():
                time.sleep(2)
                continue

        cases_count -= 1
        random_num = randint(0, cases_count)
        # 随机一个cae 文件
        case_file = cases.pop(random_num)
        try:
            thread = Thread(target=consumer, args=(devices, case_file, lock,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            log.info("执行用例：{}||待执行用例：{}".format(case_file, cases))
        except Exception as e:
            cases.append(case_file)
            cases_count += 1
        time.sleep(2)

    if threads:
        for t in threads:
            t.join()
    succ = 0
    fail = 0
    err = 0
    index_url = "http://10.2.20.198:10001/app_auto_result/" + now + "/" + "index.html"
    try:
        # end_time = time.time()
        e_time = datetime.datetime.now()
        # log.info(time.strftime("开始时间：%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
        succ, fail, err = create_summary(test_report + "/{}".format(now), s_time, e_time)
        log.info(
            "create summary success. succ:{} fail:{} err:{}".format(succ, fail, err)
        )
    except Exception as e:
        log.error(e)
    try:
        send_message(index_url, succ, fail, err)
        sendmail(test_report + "/{}".format(now), s_time, e_time, succ, fail, err)
        log.info("send mail success")
    except Exception as e:
        log.error(e)

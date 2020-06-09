# coding:utf-8
# __author__ = 'ZYF'

"""
程序运行入口：
    1.查找testcase
    2.运行testsuite
"""
import unittest, os, time
import HTMLTestRunner_PY3
# from configEmail import *
from common.send_email import sendmail
# 获取当前路径
now_dir = os.path.dirname(os.path.abspath(__file__))

test_dir = now_dir + '/' + 'testcase'
test_report = now_dir + '/' + 'report' + '/' + 'HTML'


def clean_dir(goal_path):
    '''运行前清理以前生成的报告'''
    # 1---获取目标目录下的文件
    ls = os.listdir(goal_path)
    # 2---遍历列表进行删除
    for i in ls:
        # 3---连接目录和文件名，然后用方法进行删除
        file = os.path.join(goal_path, i)
        if os.path.isdir(file):
            clean_dir(file)
        else:
            os.remove(file)


if __name__ == '__main__':
    # 判断目录是否存在，不存在新建
    if not os.path.exists(test_report):
        os.mkdir(test_report)
    clean_dir(test_report)
    testsuit = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py', top_level_dir=test_dir)
    # 获取当前时间
    now = time.strftime("%Y-%m-%d-%H_%M_%S")
    # 定义测试报告的名字
    filename = test_report + '/' + now + '_result.html'

    fp = open(filename, 'wb')
    runner = HTMLTestRunner_PY3.HTMLTestRunner(stream=fp, title='APP 测试报告',
                                               description='运行环境Android')
    runner.run(testsuit)

    print('已经运行完discover')
    fp.close()
    sendmail(filename)

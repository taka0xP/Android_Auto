#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2018/8/13 14:04
# @Author  : Soner
# @version : 1.0.0

#
# import logging
# import os.path
# import time
#
#
# class Logger(object):
#
#     def __init__(self, logger):
#         '''
#             指定保存日志的文件路径，日志级别，以及调用文件
#             将日志存入到指定的文件中
#             此处的项目名，可以使用方法，直接获得根目录，就不用在手写
#         '''
#         #  获取项目根目录
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         # 判断以当前时间命名的文件夹是否存在，不存在则新建
#         LOG_ROOT= BASE_DIR + '/logs/'
#         if not os.path.exists(LOG_ROOT):
#             os.makedirs(LOG_ROOT)
#         # filepath = os.path.dirname(os.path.abspath('./项目名')) + '/logs/' + time.strftime("%Y-%m-%d")
#         filepath = BASE_DIR + '/logs/' + time.strftime("%Y-%m-%d")
#         if not os.path.exists(filepath):
#             os.makedirs(filepath)
#
#         # 创建一个logger
#         self.logger = logging.getLogger(logger)
#         self.logger.setLevel(logging.DEBUG)
#         # 创建一个handler，用于写入日志文件
#         # rq = time.strftime("AppiumClient_%H_%M_%S", time.localtime(time.time()))
#         log_path = BASE_DIR + '/logs/%s/' % time.strftime("%Y-%m-%d")
#         # 如果case组织结构式 /testsuit/featuremodel/xxx.py ， 那么得到的相对路径的父路径就是项目根目录
#         # log_name = log_path + rq + '.log'
#         log_name = log_path + logger + '.log'
#
#         # 如果logger.handlers列表为空，则添加，否则，直接去写日志
#         if not self.logger.handlers:
#             fh = logging.FileHandler(log_name)
#             fh.setLevel(logging.INFO)
#
#             # 再创建一个handler，用于输出到控制台
#             ch = logging.StreamHandler()
#             ch.setLevel(logging.INFO)
#
#             # 定义handler的输出格式
#             formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
#             fh.setFormatter(formatter)
#             ch.setFormatter(formatter)
#
#             # 给logger添加handler
#             self.logger.addHandler(fh)
#             self.logger.addHandler(ch)
#
#
#
#     def getlog(self):
#         return self.logger
#
# if __name__ == '__main__':
#     Logger("123").getlog()


import os

try:
    from loguru import logger
except ImportError as I:
    conne = os.popen("pip install loguru").read()
    if conne:
        if "Successfully" in conne:
            from loguru import logger
        else:
            raise ImportError
import time


now = time.strftime("%Y-%m-%d")


class Logger:
    def __init__(self, file_name):
        self.file_name = file_name
        #  获取项目根目录
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 判断以当前时间命名的文件夹是否存在，不存在则新建
        self.LOG_ROOT = "{}/logs/{}".format(BASE_DIR, now)
        if not os.path.exists(self.LOG_ROOT):
            os.makedirs(self.LOG_ROOT)
        self.log_bind = logger.bind(task=file_name)

    def getlog(self):
        self.log = logger
        # retention: 设置日志有效时长   enqueue:异步写入
        self.log.add(
            "{}/{}.log".format(self.LOG_ROOT, self.file_name),
            colorize=True,
            format="<g>{time:YYYY-MM-DD HH:mm:ss.SSS}</g> | <c>{level: <7}</c> | <e>{file}</e> | <m>{function}()</m> | <yellow>{line: <4}</yellow> | 消息：<lvl>{message}</lvl>",
            enqueue=True,
            retention="2 days",
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
            catch=True,
            filter=lambda record: record["extra"]["task"] == self.file_name,
        )

        return self.log_bind


def error_format(e):
    """
    格式化error错误
    @param e:
    @return:
    """
    line = e.__traceback__.tb_lineno
    file = e.__traceback__.tb_frame.f_globals["__name__"]
    return "发生错误的文件：{}，行数：{}，错误：{}".format(file, line, repr(e))


if __name__ == "__main__":
    # logger.remove()
    # lo1 = logger.bind(task='123')
    log = Logger("123").getlog()
    log.info("sfs2")
    log.error("232")

    log2 = Logger("12").getlog()
    log2.info("test")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9
# @Author  : Soner
# @version : 1.0.0


import re
import random
import datetime
import getpass
import pymysql
from Providers.logger import Logger, error_format
from threading import Lock

log = Logger("账号管理处").getlog()
lock = Lock()

# 过滤的账号
exclude_account = [
    "11099990151",
    "11099990152",
    "11099990153",
    "11099990154",
    "11099990155",
    "11099990156",
    "11099990157",
    "11099990158",
    "11099990159",
    "11099990160",
    "11099995051",
    "11099995052",
    "11099995053",
    "11099995054",
    "11099995055",
    "11099995056",
    "11099995057",
    "11099995058",
    "11099995059",
    "11099995060",
    "11099995021",  # 监控列表专用
]

user_dict = {
    "soner": "李君",
    "xu": "许思瑞",
}


class Account:
    def __init__(self):
        db_config = {
            "host": "10.2.22.232",
            # "host": "localhost",
            "port": 3306,
            "database": "android_appium",
            "user": "root",
            "password": "stdgn",
            # "password": "111111",
            "charset": "utf8",
        }
        self.db = pymysql.connect(**db_config)

    # 判断表是否存在
    def table_exists(self, table):
        sql = "show tables"
        with self.db.cursor() as cursor:
            cursor.execute(sql)
        tables = cursor.fetchall()
        tables_list = re.findall("('.*?')", str(tables))
        tables_list = [re.sub("'", "", each) for each in tables_list]
        if table in tables_list:
            log.info("table exists")
        else:
            try:
                sql = "CREATE TABLE IF NOT EXISTS {} (id BIGINT(10) NOT NULL AUTO_INCREMENT, phone VARCHAR(11) NOT NULL COMMENT '手机号', status VARCHAR(1) NOT NULL COMMENT '使用状态', vip VARCHAR(1) COMMENT '是否vip', special VARCHAR(1) COMMENT '是否特殊账号', create_time DATETIME COMMENT '创建时间', update_time DATETIME COMMENT '更新时间', user VARCHAR(120) COMMENT '使用人', PRIMARY KEY(id))".format(
                    table
                )
                with self.db.cursor() as cursor:
                    cursor.execute(sql)
                self.db.commit()
                log.info("Successfully added table")
            except Exception as e:
                self.db.rollback()
                log.error(error_format(e))

    def make_account(self):
        """
        制造account
        @return:
        """
        try:
            self.table_exists("account")
            base = 11099995001
            vip_base = 11099990101
            with self.db.cursor() as cursor:
                for i in range(0, 100):
                    dt = datetime.datetime.now()
                    dt_now = dt.strftime("%Y-%m-%d %H:%M:%S")
                    # 是否是特殊账号
                    if str(base + i) in exclude_account:
                        account_sql = "insert into account (phone, status, create_time, vip, special) values ('{}','{}','{}', '{}', '{}')".format(
                            str(base + i), "0", dt_now, "0", "1"
                        )
                    else:
                        account_sql = "insert into account (phone, status, create_time, vip, special) values ('{}','{}','{}', '{}', '{}')".format(
                            str(base + i), "0", dt_now, "0", "0"
                        )
                    # VIP 是否是特殊账号
                    if str(vip_base + i) in exclude_account:
                        account_sql_vip = "insert into account (phone, status, create_time, vip, special) values ('{}','{}','{}', '{}', '{}')".format(
                            str(vip_base + i), "0", dt_now, "1", "1"
                        )
                    else:
                        account_sql_vip = "insert into account (phone, status, create_time, vip, special) values ('{}','{}','{}', '{}', '{}')".format(
                            str(vip_base + i), "0", dt_now, "1", "0"
                        )
                    cursor.execute(account_sql)
                    cursor.execute(account_sql_vip)
            self.db.commit()
        except Exception as e:
            log.error(error_format(e))
            self.db.rollback()

    def init_account(self):
        """
        初始化账号
        @return:
        """
        try:
            with self.db.cursor() as cursor:
                dt = datetime.datetime.now()
                dt_now = dt.strftime("%Y-%m-%d %H:%M:%S")
                update_sql = "UPDATE account SET status = '0', update_time = '{}'".format(
                    dt_now
                )
                # update_sql_vip = "UPDATE account_vip SET status = '0', update_time = '{}'".format(dt_now)
                cursor.execute(update_sql)
                # cursor.execute(update_sql_vip)
            self.db.commit()
        except Exception as e:
            log.error(error_format(e))
            self.db.rollback()

    def _operation_account(self, vip_type, account_special):
        """
        处理具体获取账号流程
        @param vip_type: 0：非VIP、1：VIP
        @return:
        """
        account_sql = "SELECT * FROM account WHERE status='0' and vip='{}' and special='{}'".format(
            vip_type, account_special
        )
        with self.db.cursor() as cursor:
            cursor.execute(account_sql)
        fetchall = cursor.fetchall()
        fetchall_count = len(fetchall)
        if fetchall_count == 0:
            log.info("没有可用的账号")
            return None
        random_num = random.randint(0, fetchall_count - 1)
        account = fetchall[random_num][1]
        self._update_account_status(account, "1", vip_type, account_special)
        if vip_type == "0":
            log.info("获取普通账号：{}，并更新使用状态".format(account))
        elif vip_type == "1":
            log.info("获取VIP账号：{}，并更新使用状态".format(account))
        return account

    def _update_account_status(self, account, status, vip_type, account_special):
        """
        更新account状态
        @param account: 账号
        @param status: 使用状态
        @param vip_type: 账号类型
        @return:
        """
        try:
            user = getpass.getuser()
            with self.db.cursor() as cursor:
                dt = datetime.datetime.now()
                dt_now = dt.strftime("%Y-%m-%d %H:%M:%S")
                update_sql = "UPDATE account SET status = '{}', update_time = '{}', user = '{}' WHERE phone='{}' and vip='{}' and special='{}'".format(
                    status,
                    dt_now,
                    user_dict.setdefault(user.lower(), user),
                    account,
                    vip_type,
                    account_special,
                )
                cursor.execute(update_sql)
            self.db.commit()
        except Exception as e:
            log.error(error_format(e))
            self.db.rollback()

    def get_account(self, account_type="account", account_special="0"):
        """
        根据类型获取账号，默认为非VIP账户
        @param account_type: 账号类型
        @param account_special: 是否特殊账号 0：不是、1：是
        @return:
        """
        global account_dict, account_vip_dict
        with lock:
            if account_type.lower() == "account":
                vip_type = "0"
            elif account_type.lower() == "vip":
                vip_type = "1"
            else:
                log.error("无效的账户类型")
            account = self._operation_account(vip_type, account_special)
            return account

    def release_account(self, account, account_type="account", account_special="0"):
        """
        归还使用的账号
        @param account: 账号
        @param account_type: 账号类型
        @param account_special: 是否特殊账号 0：不是、1：是
        @return:
        """
        global account_dict, account_vip_dict
        with lock:
            if account_type == "account":
                vip_type = "0"
            elif account_type.lower() == "vip":
                vip_type = "1"
            else:
                log.error("无效的账户类型")
            self._update_account_status(account, "0", vip_type, account_special)
        log.info("账号：{} 已归还".format(account))

    def get_pwd(self):
        """
        默认密码
        @return:
        """
        return "ef08beca"


if __name__ == "__main__":
    account = Account()
    account.make_account()
    # account.init_account()
    # ac_vip = account.get_account("VIP")
    # ac = account.get_account()
    #
    # import time
    # time.sleep(8)
    # account.release_account(ac)
    # account.release_account(ac_vip, 'vip')
    # # accounts = list()
    # for i in range(2):
    #     acc_name =account.get_account()
    #     acc_vip_name = account.get_account('vip')
    #     log.info("account：{}、account_vip：{}、密码为：{}".format(acc_name, acc_vip_name, account.get_pwd()))
    #     account.release_account(acc_name)
    #     account.release_account(acc_vip_name, 'vip')

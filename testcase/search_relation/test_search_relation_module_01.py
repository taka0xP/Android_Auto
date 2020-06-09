# -*- coding: utf-8 -*-
# @Time    : 2019-11-19 16:45
# @Author  : XU
# @File    : Search_relationTest.py
# @Software: PyCharm
from common.operation import Operation, getimage
import unittest
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger, error_format
from Providers.sift.sift_opera import SiftOperation
from Providers.relation.relation_opera import RelationOperation
from Providers.account.account import Account

log = Logger("查关系_01").getlog()


class Search_relationTest(MyTest, Operation):
    """查关系_01"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_relation")
    account = Account()
    phone_vip = account.get_account("vip")
    phone_normal = account.get_account()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)
        cls.rel_opera = RelationOperation(cls.driver, cls.ELEMENT)

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, 'vip')
        cls.account.release_account(cls.phone_normal)
        super().tearDownClass()

    @getimage
    def test_001_cgx_ss_p0(self):
        """点击热搜关系"""
        log.info(self.test_001_cgx_ss_p0.__doc__)
        try:
            rela_tag, hot_tag, home_tag = self.rel_opera.hot_relation()
            self.assertEqual(rela_tag, "输入公司名称或老板姓名", "===失败-查关系tab切换失败===")
            self.assertTrue(hot_tag, "===失败-热搜关系图节点展示失败===")
            self.assertTrue(home_tag, "===失败-关系图页，点击天眼查logo回到首页===")
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_ss_p0(self):
        """输入查关系节点"""
        log.info(self.test_002_cgx_ss_p0.__doc__)
        try:
            log.info("查关系-未登陆态")
            logout_tag = self.rel_opera.search_relation_point(index=1)
            self.assertEqual(logout_tag, self.ELEMENT['passwd_login_text'], "===失败-拉起登陆页失败===")

            log.info("查关系-登陆非VIP")
            self.sift_opera.login_normal(self.phone_normal, self.account.get_pwd())
            login_normal_tag = self.rel_opera.search_relation_point(index=2)
            self.assertEqual(login_normal_tag, "VIP会员可无限次查关系", "===失败-弹出vip弹窗失败===")

            log.info("查关系-登陆VIP")
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            login_vip_tag = self.rel_opera.search_relation_point(index=3)
            self.assertEqual(login_vip_tag, self.ELEMENT['relation_point_target'], "===失败-查关系结果关系图错误===")

            human_tag, relation_point_tag = self.rel_opera.check_relation()
            # 断言-节点输入人员，匹配对应结果
            self.assertEqual(human_tag, "白夏冰", "===失败-搜索结果页，带入人员名称失败===")
            # 断言-公司与人员关系查询
            self.assertEqual(relation_point_tag, "北京金堤征信服务有限公司", "===失败-查关系结果关系图错误===")

        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgx_gxt_p0(self):
        """查关系结果图"""
        log.info(self.test_003_cgx_gxt_p0.__doc__)
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            self.rel_opera.exam_relation()

            # 断言-点击全屏按钮
            discover_btn_tag, exit_fullscreen_tag, relation_point_tag = self.rel_opera.all_screen()
            self.assertFalse(discover_btn_tag, "===失败-查关系按钮未隐藏===")
            self.assertTrue(exit_fullscreen_tag, "===失败-未获取到退出全屏按钮===")
            self.assertTrue(relation_point_tag, "===失败-关系图全屏展示后，图谱节点展示异常===")

            # 断言-退出全屏
            exit_fullscreen_tag, discover_btn_tag = self.rel_opera.exit_screen()
            self.assertFalse(exit_fullscreen_tag, "===失败-退出全屏按钮未隐藏===")
            self.assertTrue(discover_btn_tag, "===失败-退出全屏失败===")

            # 断言-关系图页，「清空」二次确认弹框
            delte_tag, confirm_tag, point_tag, cancel_tag, empty_tag = self.rel_opera.confirm()
            self.assertTrue(delte_tag, "===失败-二次确认弹窗未弹出===")
            self.assertFalse(confirm_tag, "===失败-二次确认弹窗未关闭===")
            self.assertTrue(point_tag, "===失败-关闭弹窗后，关系图显示异常===")
            self.assertFalse(cancel_tag, "===失败-二次确认弹窗未关闭===")
            self.assertTrue(empty_tag, "===失败-关系图清空，占位图未展示===")

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : wlx
# @File    : DiscussTest.py
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format

log = Logger("问答_04").getlog()


class Discuss_Test_4(MyTest, Operation):
    """问答_04"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("discuss")
        cls.vip_user = cls.account.get_account("vip", "0")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.vip_user, account_type="vip", account_special="0")

    @getimage
    def test_001(self):
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.new_find_element(By.XPATH, self.ELEMENT["home_headline"]).click()
            sleep(10)
            question = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/rl_title", outtime=10)
            question.click()
            if self.isElementExist(By.XPATH, self.ELEMENT['question_following']):
                self.new_find_element(By.ID, self.ELEMENT['question_follow_icon']).click()
            self.new_find_element(By.ID, self.ELEMENT['question_follow_icon']).click()
            self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT['question_following']), '关注问题功能错误')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        import re
        log.info(self.test_002.__doc__)
        try:
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_my_answers").click()
            self.new_find_element(By.XPATH, self.ELEMENT["mine_question_follow_tab"]).click()
            question = self.new_find_elements(By.ID, self.ELEMENT["question_follow_list_title"])[0]
            list_title = re.search(r"[\u4e00-\u9fa5]+", question.text).group()
            question.click()
            b = self.ocr(By.XPATH, self.ELEMENT["question_detail_title"])
            detail_title = re.search(r"[\u4e00-\u9fa5]+", b).group()
            self.new_find_element(By.ID, self.ELEMENT['question_follow_icon']).click()
            self.assertEqual(list_title, detail_title, '关注问题列表问题标题{}与问题详情页标题{}不一致'.format(list_title, detail_title))
            self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT['question_follow']), '取消关注问题功能错误')
            self.driver.keyevent(4)
            self.swipeDown(y1=0.4, y2=0.8)
            sleep(2)
            if self.new_find_elements(By.ID, self.ELEMENT["question_follow_list_title"]):
                self.assertNotEqual(list_title, question.text, '取消问题关注后列表仍展示问题{}'.format(question.text))
            else:
                self.assertFalse(self.isElementExist(By.ID, self.ELEMENT["question_follow_list_title"]))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

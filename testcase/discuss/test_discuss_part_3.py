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

log = Logger("问答_03").getlog()


class Discuss_Test_3(MyTest, Operation):
    """问答_03"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("discuss")
        cls.user = cls.account.get_account()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.user, account_type="account", account_special="0")

    @getimage
    def test_001(self):
        log.info(self.test_001.__doc__)
        try:
            self.login(self.user, self.account.get_pwd())
            self.new_find_element(By.XPATH, self.ELEMENT["home_headline"]).click()
            sleep(10)
            question = self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/rl_title", outtime=10
            )
            question.click()
            self.swipeUp()
            a = self.new_find_element(By.XPATH, self.ELEMENT["agree_count"]).text
            self.new_find_element(By.XPATH, self.ELEMENT["agree_btn"]).click()
            b = self.isElementExist(By.XPATH, "//*[contains(@text,'已点过赞')]")
            if b == True:
                pass
            else:
                if a == "点赞":
                    count = self.new_find_element(
                        By.XPATH, self.ELEMENT["agree_count"]
                    ).text
                    self.assertEqual(count, "1", "回答点赞错误")
                else:
                    count = int(
                        self.new_find_element(By.XPATH, self.ELEMENT["agree_count"]).text
                    )
                    self.assertEqual(count, int(a) + 1, "回答点赞错误")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
    @getimage
    def test_002(self):
        log.info(self.test_002.__doc__)
        try:
            self.new_find_element(By.XPATH, self.ELEMENT["home_headline"]).click()
            sleep(10)
            question = self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/rl_title", outtime=10
            )
            question.click()
            self.swipeUp()
            # 非VIP私信VIP限制
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/iv_avatar', outtime=10)[
                0
            ].click()
            self.new_find_element(By.XPATH, self.ELEMENT["im_btn"]).click()
            self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/bar_edit_text"
            ).send_keys("你好")
            self.driver.keyevent(66)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["im_vip_toast"], outtime=15),
                "非vip用户进行私信无VIP弹窗",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
    @getimage
    def test_003(self):
        log.info(self.test_003.__doc__)
        try:
            self.new_find_element(By.XPATH, self.ELEMENT["home_headline"]).click()
            sleep(10)
            question = self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/rl_title", outtime=10
            )
            question.click()
            self.swipeUp()
            # 回复不足两个字toast提示
            self.new_find_element(By.XPATH, self.ELEMENT["reply"], outtime=10).click()
            self.new_find_element(By.ID, self.ELEMENT["reply_edit"]).send_keys("1")
            self.new_find_element(By.ID, self.ELEMENT["reply_send"]).click()
            a = self.isElementExist(By.XPATH, self.ELEMENT["reply_send_toast1"])
            self.assertTrue(a, "回复不足2个字toast提示错误")
            self.driver.keyevent(4)
            # 回复详情页进行点赞
            a = self.new_find_element(By.XPATH, self.ELEMENT["agree_count"]).text
            self.new_find_element(By.XPATH, self.ELEMENT["agree_btn"]).click()
            b = self.isElementExist(By.XPATH, "//*[contains(@text,'已点过赞')]")
            if b == True:
                pass
            else:
                if a == "点赞":
                    count = self.new_find_element(
                        By.XPATH, self.ELEMENT["agree_count"]
                    ).text
                    self.assertEqual(count, "1", "回答点赞错误")
                else:
                    count = int(
                        self.new_find_element(By.XPATH, self.ELEMENT["agree_count"]).text
                    )
                    self.assertEqual(count, int(a) + 1, "回答点赞错误")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : wlx
# @File    : Human_detailTest.py
from Providers.back_to_index import back_to_index
from Providers.random_str.random_str import RandomStr
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format

log = Logger("老板认证_01").getlog()


class Boss_claim_Test_1(MyTest, Operation):
    """老板认证_01"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("human_detail")
        cls.vip_user = cls.account.get_account("vip", "0")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.vip_user, account_type="vip", account_special="0")

    def im_boss(self, boss_name, index=0):
        self.search_boss(boss_name)
        self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/information_click_block')[index].click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_name_tv').click()

    def post_pohoto(self, type=0, click=True):
        if type == 0:
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_id_card_photo_iv').click()
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/tv_title')[1].click()
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/iv_thumb')[0].click()
            if click:
                self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_summit').click()
                self.assertTrue(self.isElementExist(By.XPATH, "//*[@text='请上传身份证信息']"), '未提交身份证信息时无toast提示')
        elif type == 1:
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_id_card_emblem_iv').click()
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/tv_title')[1].click()
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/iv_thumb')[0].click()
            if click:
                self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_summit').click()
                self.assertTrue(self.isElementExist(By.XPATH, "//*[@text='请上传名片/其他身份补充材料']"), '未提交身份证信息时无toast提示')

        elif type == 2:
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_work_card_iv').click()
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/tv_title')[1].click()
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/iv_thumb')[0].click()
            if click:
                self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_summit').click()
                self.new_find_element(By.XPATH, "//*[@text='提交成功']")

    def cancel_boss(self,company='百度'):
        back_to_index(self.driver)
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tab_iv_5').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/iv_haslogin').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_company_tv').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_info_suggest_clear_iv').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_info_suggest_input_et').send_keys(company)
        self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/tv_com_name')[0].click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_message_submit_btn').click()
        if self.isElementExist(By.XPATH, "//*[@text='确定更换[公司/学校]信息么？']"):
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_pos').click()
        if self.isElementExist(By.XPATH, "//*[@text='该昵称已被占用']"):
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_edit_nickname_iv').click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_clear_nickname_iv').click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_nickname_et').send_keys(RandomStr().zh_cn(5))
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_message_submit_btn').click()
        if self.isElementExist(By.XPATH, "//*[@text='确定更换[公司/学校]信息么？']"):
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_pos').click()

    def is_boss_claim(self):
        back_to_index(self.driver)
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tab_iv_5').click()
        if self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/iv_company_claim'):
            claim_status = self.ocr(By.ID, 'com.tianyancha.skyeye:id/iv_company_claim')
            if claim_status == '认证中':
                return True
            else:
                return False
        else:
            if self.isElementExist(By.XPATH, "//*[contains(@text,'暂无公司信息')]"):
                return False
            else:
                return True

    @getimage
    def test_001(self):
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            cliam_status = self.is_boss_claim()
            if cliam_status:
                self.cancel_boss()
            self.im_boss('冯一桂', 1)
            if self.isElementExist(By.XPATH, "//*[@text='失败原因']"):
                self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_summit').click()
                self.new_find_element(By.XPATH, "//*[@text='提交成功']")
            else:
                self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_summit').click()
                self.assertTrue(self.isElementExist(By.XPATH, "//*[@text='请上传身份证信息']"), '未提交身份证信息时无toast提示')
                for i in range(0, 3):
                    self.post_pohoto(i)
            self.cancel_boss()
            cliam_status = self.is_boss_claim()
            self.assertFalse(cliam_status, '账号{}未取消老板认证'.format(self.vip_user))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))

    @getimage
    def test_002(self):
        log.info(self.test_002.__doc__)
        try:
            self.search_boss('冯一')
            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/information_click_block')[1].click()

            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/title_1').click()
            company1 = self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/com_name_tv')[1].text

            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/title_2').click()
            company2 = self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/com_name_tv')[1].text

            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/title_3').click()
            company3 = self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/com_name_tv')[1].text

            self.driver.keyevent(4)

            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/information_click_block')[1].click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_name_tv').click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_company_name_list_ll').click()
            self.new_find_element(By.XPATH, "//*[@text='{}']".format(company1)).click()
            sleep(1)
            self.assertTrue(self.isElementExist(By.XPATH, "//*[@text='法定代表人']"), '老板认证选择的公司{}无法人选项'.format(company1))

            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_company_name_list_ll').click()
            self.new_find_element(By.XPATH, "//*[@text='{}']".format(company2)).click()
            sleep(1)
            self.assertTrue(self.isElementExist(By.XPATH, "//*[@text='股东']"), '老板认证选择的公司{}无股东选项'.format(company2))

            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/company_auth_company_name_list_ll').click()
            self.new_find_element(By.XPATH, "//*[@text='{}']".format(company3)).click()
            sleep(1)
            self.assertTrue(self.isElementExist(By.XPATH, "//*[@text='董监高']"), '老板认证选择的公司{}无董监高选项'.format(company3))
            self.driver.keyevent(4)
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_neg').click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))

    @getimage
    def test_002(self):
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("珠海激情百度文化传播有限公司")

            self.cancel_boss('宁夏天元锰业')

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
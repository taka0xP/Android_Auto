from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import time
import unittest
import re

log = Logger("查公司_03").getlog()


class Search_companyTest(MyTest, Operation):
    """查公司_03"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_company")

    def login_page_check(self,way,element):
        '''判断是否在登录页面'''
        if way == 1:
            self.new_find_element(By.ID,element).click()
        elif way == 2:
            self.new_find_element(By.XPATH,element).click()
        result = self.isElementExist(By.ID,"com.tianyancha.skyeye:id/btv_title")
        text = self.new_find_element(By.ID,"com.tianyancha.skyeye:id/btv_title").text
        if text == '短信验证码登录':
            log.info('当前在短信验证码登录页面')
        elif text == '密码登录':
            log.info('当前在密码登录页面')
        return result
    def search_clear(self):
        '''清除输入框'''
        self.new_find_element(By.ID,self.ELEMENT['search_clean']).click()
    def get_title_name(self):
        '''获取页面title名称'''
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return text

    @getimage
    def test_CGS_SSZJY_0001(self):
        '''搜索中间页-最近浏览-项目品牌/投资机构'''
        log.info(self.test_CGS_SSZJY_0001.__doc__)

        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        result = self.isElementExist(By.ID, self.ELEMENT["read_history_all"])
        if result == False:
            goal_01 = "进入项目品牌详情页不生成最近浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("天眼查")
            self.new_find_element(By.XPATH, self.ELEMENT["brand-name"]).click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            result_01 = self.isElementExist(By.XPATH, self.ELEMENT["read_history_all"])
            self.assertFalse(result_01, "错误————%s" % goal_01)

            goal_02 = "进入投资机构详情页不生成最近浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("浦信资本")
            self.new_find_element(By.XPATH, self.ELEMENT["organization_name"]).click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            result_02 = self.isElementExist(By.XPATH, self.ELEMENT["read_history_all"])
            self.assertFalse(result_02, "错误————%s" % goal_02)
        else:
            log.error("未执行用例test_CGS_SSZJY_0001——有浏览记录，请先删除")

    @getimage
    def test_CGS_ZSSJGY_0002(self):
        '''搜索结果页-模糊关键词拼音'''
        log.info(self.test_CGS_ZSSJGY_0002.__doc__)

        goal_01 = "搜索模糊关键词拼音查看搜索结果"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("mayun")
        result_01 = self.isElementExist(By.XPATH, self.ELEMENT["keyword_error"])
        self.assertTrue(result_01, "错误————%s" % goal_01)

        goal_02 = "点击关键词纠错，模块消失"
        self.new_find_element(By.XPATH, self.ELEMENT["keyword_error"]).click()
        time.sleep(1)
        test = self.isElementExist(By.XPATH, self.ELEMENT["keyword_error"])
        self.assertFalse(test, "错误————%s" % goal_02)

    @getimage
    def test_CGS_ZSSJGY_0003(self):
        '''搜索结果页-相关人员'''
        log.info(self.test_CGS_ZSSJGY_0003.__doc__)

        goal = ["搜索项目品牌名称能匹配到公司相关人员", "搜索公司名称能匹配到公司相关人员"]
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("蘑菇街")
        result_01 = self.isElementExist(By.ID, self.ELEMENT["search_result_personnel_title"])
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("北京金堤科技有限公司")
        result_02 = self.isElementExist(By.ID, self.ELEMENT["search_result_personnel_title"])
        self.assertTrue(result_01, "错误————%s" % goal[0])
        self.assertTrue(result_02, "错误————%s" % goal[1])

    @getimage
    def test_CGS_ZSSJGY_0004(self):
        '''搜索结果页-相关人员-全部规则&交互01'''
        log.info(self.test_CGS_ZSSJGY_0004.__doc__)

        goal = ["匹配到的公司相关人员大于2条标题栏有【全部】入口", "点击【全部】进入全部老板列表页"]
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("蘑菇街")
        result_01 = self.isElementExist(By.ID, self.ELEMENT["same_boss_seeall"])
        self.assertTrue(result_01, "错误————%s" % goal[0])
        self.new_find_element(By.ID, self.ELEMENT["same_boss_seeall"]).click()
        text_02 = self.get_title_name()
        self.assertEqual(text_02,'老板',"错误————%s" % goal[1])

    @getimage
    def test_CGS_ZSSJGY_0005(self):
        '''搜索结果页-相关人员-全部规则&交互02'''
        log.info(self.test_CGS_ZSSJGY_0005.__doc__)

        goal = "匹配到的公司相关人员小于等于2条标题栏无【查看全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("山西怡飞百泰科技有限公司")
        text = self.new_find_element(By.ID, self.ELEMENT["search_result_personnel_title"]).text
        result = re.findall(r"\d+\.?\d*", text)[0]
        num = int(result)
        if num <= 2:
            submit = self.isElementExist(By.ID, self.ELEMENT["same_boss_seeall"])
            self.assertFalse(submit, "错误————%s" % goal)
        else:
            log.error("case相关人员大于2条")

    @getimage
    def test_CGS_ZSSJGY_0006(self):
        '''搜索结果页-相关人员-全部规则&交互03'''
        log.info(self.test_CGS_ZSSJGY_0006.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()

        goal_01 = "未登录点击匹配到的公司相关人员跳转登陆页"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("京东")
        result_01 = self.login_page_check(2,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name']")
        self.assertTrue(result_01,"错误————%s" % goal_01)

        goal_02 = "登陆点击匹配到的公司相关人员能进入人员详情页"
        account = self.account.get_account()
        self.login(account, self.account.get_pwd())
        text_02 = self.isElementExist(By.ID, self.ELEMENT["person_detail"])
        self.assertTrue(text_02, "错误————%s" % goal_02)

        self.logout()
        self.account.release_account(account)

    @getimage
    def test_CGS_ZSSJGY_0007(self):
        '''搜索结果页-相关人员-全部规则&交互04'''
        log.info(self.test_CGS_ZSSJGY_0007.__doc__)

        goal_01 = "匹配到的公司相关人员大于20条滑动区域末尾显示【查看全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("长白山")
        text = self.new_find_element(By.ID, self.ELEMENT["search_result_personnel_title"]).text
        result = re.findall(r"\d+\.?\d*", text)[0]
        num = int(result)
        if num > 20:
            for n in range(6):
                l = self.driver.get_window_size()
                x1 = l["width"] * 0.95
                y1 = l["height"] * 0.25
                x2 = l["width"] * 0.05
                time.sleep(0.5)
                try:
                    self.driver.swipe(x1, y1, x2, y1, 500)
                except:
                    pass
            result_01 = self.isElementExist(By.ID, self.ELEMENT["personnel_all"])
            self.assertTrue(result_01, "错误————%s" % goal_01)
        else:
            log.error("case相关人员小于20条")

    @getimage
    def test_CGS_ZSSJGY_0008(self):
        '''搜索结果页-相关人员-全部规则&交互05'''
        log.info(self.test_CGS_ZSSJGY_0008.__doc__)

        goal_01 = "匹配到的公司相关人员小于等于20条滑动区域末尾不显示【查看全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("金堤")
        text = self.new_find_element(By.ID, self.ELEMENT["search_result_personnel_title"]).text
        result = re.findall(r"\d+\.?\d*", text)[0]
        num = int(result)
        if num <= 20:
            for n in range(6):
                l = self.driver.get_window_size()
                x1 = l["width"] * 0.95
                y1 = l["height"] * 0.25
                x2 = l["width"] * 0.05
                time.sleep(0.5)
                try:
                    self.driver.swipe(x1, y1, x2, y1, 500)
                except:
                    pass
            result_01 = self.isElementExist(By.ID, self.ELEMENT["personnel_all"])
            self.assertFalse(result_01, "错误————%s" % goal_01)
        else:
            log.error("case相关人员大于20条")

    @getimage
    def test_CGS_ZSSJGY_0009(self):
        '''搜索结果页-相关人员-全部规则&交互06'''
        log.info(self.test_CGS_ZSSJGY_0009.__doc__)

        goal = "搜索关键词匹配到的公司无相关人员数据"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("奇遇记忆")
        text = self.isElementExist(By.XPATH, self.ELEMENT["search_result_personnel_title"])
        self.assertFalse(text, "错误————%s" % goal)

    @getimage
    def test_CGS_ZSSJGY_0010(self):
        '''搜索结果页-同名老板规则&交互01'''
        log.info(self.test_CGS_ZSSJGY_0010.__doc__)

        goal_01 = "搜索关键词能匹配到同名老板"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("马云")
        result_01 = self.isElementExist(By.ID, self.ELEMENT["same_boss_title"])
        self.assertTrue(result_01, "错误————%s" % goal_01)

        goal_02 = "搜索关键词匹配不到同名老板"
        self.search_clear()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("苏泊车")
        result_02 = self.isElementExist(By.XPATH, self.ELEMENT["same_boss_title"])
        self.assertFalse(result_02, "错误————%s" % goal_02)

    @getimage
    def test_CGS_ZSSJGY_0011(self):
        '''搜索结果页-同名老板规则&交互02'''
        log.info(self.test_CGS_ZSSJGY_0011.__doc__)

        goal_01 = "匹配到的同名老板大于2条标题栏有【全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("马云")
        text = self.new_find_element(By.ID, self.ELEMENT["same_boss_title"]).text
        result = re.findall(r"\d+\.?\d*", text)[0]
        num_01 = int(result)
        if num_01 > 2:
            result_02 = self.isElementExist(By.ID, self.ELEMENT["same_boss_seeall"])
            self.assertTrue(result_02, "错误————%s" % goal_01)
            goal_02 = "点击【全部】入口能进入马云的人员搜索页"
            self.new_find_element(By.ID, self.ELEMENT["same_boss_seeall"]).click()
            text_02 = self.new_find_element(By.ID, self.ELEMENT["app_title_name"]).text
            self.assertEqual(text_02, "马云", "错误————%s" % goal_02)
        else:
            result_02 = self.isElementExist(By.ID, self.ELEMENT["same_boss_seeall"])
            self.assertFalse(result_02, "错误————%s" % goal_01)

    @getimage
    def test_CGS_ZSSJGY_0012(self):
        '''搜索结果页-同名老板规则&交互03'''
        log.info(self.test_CGS_ZSSJGY_0012.__doc__)

        goal_01 = "匹配到的同名老板小于等于2条标题栏无【全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("易烊千玺")
        text_01 = self.new_find_element(By.ID, self.ELEMENT["same_boss_title"]).text
        result = re.findall(r"\d+\.?\d*", text_01)[0]
        num_01 = int(result)
        if num_01 > 2:
            result_02 = self.isElementExist(By.ID, self.ELEMENT["same_boss_seeall"])
            self.assertTrue(result_02, "错误————%s" % goal_01)
        else:
            result_02 = self.isElementExist(By.ID, self.ELEMENT["same_boss_seeall"])
            self.assertFalse(result_02, "错误————%s" % goal_01)

    @getimage
    def test_CGS_ZSSJGY_0013(self):
        '''搜索结果页-同名老板规则&交互04'''
        log.info(self.test_CGS_ZSSJGY_0013.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()

        goal_01 = "未登录点击匹配到的同名老板能跳转登陆页"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("李彦宏")
        self.new_find_element(By.ID, self.ELEMENT["same_boss_first"]).click()
        submit_01 = self.new_find_element(By.ID, self.ELEMENT["login_title"])
        test_01 = submit_01.text
        self.assertEqual(test_01, "短信验证码登录", "错误————%s" % goal_01)

        goal_02 = "已登陆点击匹配到的同名老板能进入人员详情页"
        account = self.account.get_account()
        self.login(account, self.account.get_pwd())
        test_02 = self.isElementExist(By.ID, self.ELEMENT["person_detail"])
        self.assertTrue(test_02, "错误————%s" % goal_02)

        self.logout()
        self.account.release_account(account)

    @getimage
    def test_CGS_ZSSJGY_0014(self):
        '''搜索结果页-同名老板规则&交互05'''
        log.info(self.test_CGS_ZSSJGY_0014.__doc__)

        goal = "匹配到的同名老板大于20条滑动区域末尾显示【查看全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("柳超")
        text = self.new_find_element(By.ID, self.ELEMENT["same_boss_title"]).text
        result = re.findall(r"\d+\.?\d*", text)[0]
        num = int(result)
        if num > 20:
            for n in range(6):
                l = self.driver.get_window_size()
                x1 = l["width"] * 0.95
                y1 = l["height"] * 0.25
                x2 = l["width"] * 0.05
                time.sleep(0.5)
                try:
                    self.driver.swipe(x1, y1, x2, y1, 500)
                except:
                    pass
            result_01 = self.isElementExist(By.ID, self.ELEMENT["personnel_all"])
            self.assertTrue(result_01, "错误————%s" % goal)
        else:
            log.error("case相关人员小于20条")

    @getimage
    def test_CGS_ZSSJGY_0015(self):
        '''搜索结果页-同名老板规则&交互06'''
        log.info(self.test_CGS_ZSSJGY_0015.__doc__)

        goal = "匹配到的同名老板小于等于20条滑动区域末尾不显示【查看全部】入口"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("王思诚")
        text = self.new_find_element(By.ID, self.ELEMENT["same_boss_title"]).text
        result = re.findall(r"\d+\.?\d*", text)[0]
        num = int(result)
        if num <= 20:
            for n in range(6):
                l = self.driver.get_window_size()
                x1 = l["width"] * 0.95
                y1 = l["height"] * 0.2
                x2 = l["width"] * 0.05
                time.sleep(0.5)
                try:
                    self.driver.swipe(x1, y1, x2, y1, 500)
                except:
                    pass
            result_01 = self.isElementExist(By.ID, self.ELEMENT["personnel_all"])
            self.assertFalse(result_01, "错误————%s" % goal)
        else:
            log.error("case相关人员大于20条")

    @getimage
    def test_CGS_ZSSJGY_0016(self):
        '''搜索结果页-项目品牌规则&交互'''
        log.info(self.test_CGS_ZSSJGY_0016.__doc__)

        goal_01 = "搜索的关键词能匹配到项目品牌"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("天眼查")
        result = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name'and @text='天眼查']")
        self.assertTrue(result, "错误————%s" % goal_01)

        goal_02 = "点击匹配到的项目品牌能进入项目品牌详情页"
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name'and @text='天眼查']").click()
        text_02 = self.new_find_element(By.ID, self.ELEMENT["detail_page_title"]).text
        self.assertEqual(text_02, "品牌详情", "错误————%s" % goal_02)

    @getimage
    def test_CGS_ZSSJGY_0017(self):
        '''搜索结果页-项目品牌规则&交互'''
        log.info(self.test_CGS_ZSSJGY_0017.__doc__)

        goal_01 = "搜索的关键词能匹配到投资机构"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("浦信资本")
        result = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name'and @text='浦信资本']")
        self.assertTrue(result, "错误————%s" % goal_01)

        goal_02 = "点击匹配到的投资机构能进入投资机构详情页"
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name'and @text='浦信资本']").click()
        text_02 = self.new_find_element(By.ID, self.ELEMENT["detail_page_title"]).text
        self.assertEqual(text_02, "机构详情", "错误————%s" % goal_02)

    @getimage
    def test_CGS_ZSSJGY_0018(self):
        '''搜索结果页-项目品牌/投资机构'''
        log.info(self.test_CGS_ZSSJGY_0018.__doc__)

        goal = "搜索到的关键词匹配不到项目品牌/投资机构"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("天天酷跑")
        test = self.isElementExist(By.ID, self.ELEMENT["brand_organization_title"])
        self.assertFalse(test, "错误————%s" % goal)

if __name__ == "__main__":
    unittest.main()

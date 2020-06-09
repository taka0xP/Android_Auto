# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : wlx
# @File    :DiscussTest.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format

log = Logger("问答_01").getlog()


class Discuss_Test_1(MyTest, Operation):
    """问答_01"""

    a = Read_Ex()
    ELEMENT = a.read_excel("discuss")

    def go_question_ugc(self, type=1, company=None):
        # 进入问题编辑器入口方法1：问大家列表进入； 2：公司详情侧边问大家按钮 ；3：投资机构进入问答编辑器；
        # 4：品牌机构进入问题编辑器；5：人员详情页进入问答编辑器6：公司详情页底部问大家入口

        # 问大家列表进入问题编辑器
        if type == 1:
            self.new_find_element(By.ID, self.ELEMENT["home_discuss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["diacuss_list_send_ask"]).click()

        # 公司详情-侧边问大家按钮进入问大家编辑器
        elif type == 2:
            self.search_company(company)
            self.new_find_element(
                By.XPATH,
                "(//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name'])[1]",
            ).click()
            sleep(2)
            self.new_find_element(By.ID, self.ELEMENT["company_official_ask"]).click()

        # 投资机构进入问答编辑器
        elif type == 3:
            self.search_company(company)
            self.new_find_element(By.XPATH, self.ELEMENT["tzjg_name"]).click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["brand_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_question_ugc"]
            ).click()
        # 品牌机构进入问题编辑器
        elif type == 4:
            self.search_company(company)
            self.new_find_element(By.XPATH, self.ELEMENT["brand_name"]).click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["brand_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_question_ugc"]
            ).click()
        # 人员详情页进入问答编辑器
        elif type == 5:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["top_search"]).click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["person_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_question_ugc"]
            ).click()
        # 公司详情页底部问大家入口
        elif type == 6:
            self.search_company(company)
            self.new_find_element(
                By.XPATH,
                "(//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name'])[1]",
            ).click()
            sleep(2)
            x = self.driver.get_window_size()["width"]
            y = self.driver.get_window_size()["height"]
            count = 0
            while True:
                if count > 8:
                    print("-----------滑动找不到问大家入口，请手动校验-----------")
                    break
                else:
                    try:
                        self.driver.find_element_by_xpath(
                            self.ELEMENT["company_question_ugc"]
                        )
                        break
                    except:
                        self.driver.swipe(0.5 * x, 0.8 * y, 0.5 * x, 0.2 * y, 1200)
                        count += 1
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_question_ugc"]
            ).click()

    def go_hot_question_list(self, type=0, company=None):
        # 进入问大家问题列表方法
        # 首页--商业头条进入问大家列表
        if type == 0:
            self.new_find_element(By.XPATH, self.ELEMENT["home_headline"]).click()
            self.new_find_element(By.ID, self.ELEMENT["home_all_question"]).click()
        # 首页问大家tab进入热门问答列表
        elif type == 1:
            self.new_find_element(By.ID, self.ELEMENT["home_discuss"]).click()

        # 公司详情-进入热门问答列表
        elif type == 2:
            self.search_company(company)
            self.new_find_element(
                By.XPATH,
                "(//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name'])[1]",
            ).click()
            sleep(2)
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["company_hot_question_title"], check_cover=True)
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["company_all_hot_question"], check_cover=True,
                                            click=True)

        # 投资机构进入热门问答列表
        elif type == 3:
            self.search_company(company)
            self.new_find_element(By.XPATH, self.ELEMENT["tzjg_name"]).click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["brand_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_all_hot_question"]
            ).click()

        # 品牌机构进入热门问答列表
        elif type == 4:
            self.search_company(company)
            self.new_find_element(By.XPATH, self.ELEMENT["brand_name"]).click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["brand_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_all_hot_question"]
            ).click()

        # 人员详情页进入热门问答列表
        elif type == 5:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["top_search"]).click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["person_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_all_hot_question"]
            ).click()

        elif type == 6:
            self.search_company(company)
            self.new_find_element(
                By.XPATH,
                "(//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name'])[1]",
            ).click()
            sleep(2)
            self.new_find_element(By.ID, self.ELEMENT["company_self"]).click()
            self.swipe_up_while_ele_located(By.XPATH,self.ELEMENT["company_hot_question_title"], click=True)

    def go_mydiscuss_tab(self, tab=0, back_max=30):
        back_count = 0
        while True:
            if back_count > back_max:
                break
            try:
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/home_tab1")
                break
            except:
                self.driver.keyevent(4)
                back_count += 1
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_my_answers").click()

        if tab == 1:
            self.new_find_element(By.XPATH, self.ELEMENT["mytab_myanswer_tab"]).click()
        elif tab == 2:
            self.new_find_element(By.XPATH, self.ELEMENT["mytab_invite_tab"]).click()
        elif tab == 0:
            pass

    @getimage
    def test_001(self):
        import re
        log.info(self.test_001.__doc__)
        try:
            # 首页商业头条进入热门问答列表
            self.go_hot_question_list()
            self.assertTrue(
                self.new_find_elements(By.XPATH, self.ELEMENT["hot_questions_list"]),
                "首页商业头条进入热门问答列表失败",
            )
            self.driver.keyevent(4)

            # 首页商业头条进入问题详情页
            a = self.new_find_element(By.ID, self.ELEMENT["home_question_name"]).text
            list_title = re.search(r"[\u4e00-\u9fa5]+", a).group()
            self.new_find_element(By.ID, self.ELEMENT["home_question_name"]).click()
            b = self.ocr(By.XPATH, self.ELEMENT["question_detail_title"])
            detail_title= re.search(r"[\u4e00-\u9fa5]+", b).group()
            self.assertEqual(list_title, detail_title, "首页商业头条进入问题详情页失败")
            self.driver.keyevent(4)

            # 首页问大家tab进入热门问答列表
            self.go_hot_question_list(1)
            self.assertTrue(
                self.new_find_elements(By.XPATH, self.ELEMENT["hot_questions_list"]),
                "首页问大家tab进入热门问答列表失败",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        log.info(self.test_002.__doc__)
        try:
            # 公司详情页--官方信息进入问答热门问答列表、问题编辑器
            self.go_hot_question_list(2, "深圳市腾讯计算机系统有限公司")
            self.assertTrue(
                self.new_find_elements(
                    By.XPATH, self.ELEMENT["hot_questions_list"], outtime=10
                ),
                "公司详情页进入热门问答列表失败",
            )
            self.driver.keyevent(4)
            self.new_find_element(By.ID, self.ELEMENT["company_official_ask"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["question_ugc_title"]),
                "公司详情页进入问题编辑器失败",
            )
            self.assertFalse(
                self.new_find_element(By.ID, self.ELEMENT["question_ugc_relation_company"]),
                "公司详情页进入问答编辑器有关联公司按钮",
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
            self.go_hot_question_list(3, "腾讯")
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["hot_questions_list"]),
                "投资机构热门问答列表失败",
            )
            self.driver.keyevent(4)
            self.new_find_element(By.XPATH, self.ELEMENT["company_question_ugc"]).click()
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["question_ugc_toolbar"]),
                "投资机构无法进入编辑器",
            )
            self.assertFalse(
                self.new_find_element(By.ID, self.ELEMENT["question_ugc_relation_company"]),
                "投资机构详情页进入问答编辑器有关联公司按钮",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_004(self):
        log.info(self.test_004.__doc__)
        try:
            self.go_hot_question_list(4, "腾讯")
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["hot_questions_list"]),
                "项目品牌进入热门问答列表失败",
            )
            self.driver.keyevent(4)
            self.new_find_element(By.XPATH, self.ELEMENT["company_question_ugc"]).click()
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["question_ugc_toolbar"]),
                "项目品牌无法进入编辑器",
            )
            self.assertFalse(
                self.new_find_element(By.ID, self.ELEMENT["question_ugc_relation_company"]),
                "项目品牌详情页进入问答编辑器有关联公司按钮",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_005(self):
        log.info(self.test_005.__doc__)
        try:
            self.go_hot_question_list(6, "上海熊猫互娱文化有限公司")
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["hot_questions_list"]),
                "公司详情页自主信息tab进入热门问答列表失败",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_006(self):
        log.info(self.test_006.__doc__)
        try:
            self.go_hot_question_list(5)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["hot_questions_list"]),
                "人员详情页进入热门问答列表失败",
            )
            self.driver.keyevent(4)
            self.new_find_element(By.XPATH, self.ELEMENT["company_question_ugc"]).click()
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["question_ugc_toolbar"]),
                "人员详情页无法进入编辑器",
            )
            self.assertFalse(
                self.new_find_element(By.ID, self.ELEMENT["question_ugc_relation_company"]),
                "人员详情页进入问答编辑器有关联公司按钮",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_007(self):
        log.info(self.test_007.__doc__)
        try:
            self.new_find_element(By.XPATH, self.ELEMENT["home_headline"]).click()
            sleep(10)
            question = self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/rl_title", outtime=10
            )
            question.click()
            self.swipeUp()
            self.new_find_element(By.XPATH, self.ELEMENT["reply"], outtime=10).click()
            self.new_find_element(By.ID, self.ELEMENT["reply_edit"]).send_keys(
                self.ELEMENT["answer"]
            )
            self.new_find_element(By.ID, self.ELEMENT["reply_send"]).click()
            login_use_pwd = self.isElementExist(By.XPATH, self.ELEMENT["login_use_pwd"])
            login_new = self.isElementExist(By.XPATH, self.ELEMENT["login_new"])
            if login_use_pwd == True or login_new == True:
                result = True
            else:
                result = False
            self.assertTrue(result, "问答点击发送回复未调起登录")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

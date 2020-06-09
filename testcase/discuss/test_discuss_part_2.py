# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : wlx
# @File    : DiscussTest.py
import random
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format
from Providers.random_str.random_str import RandomStr

log = Logger("问答_02").getlog()


class Discuss_Test_2(MyTest, Operation):
    """问答_02"""

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

    # a = Read_Ex()
    # ELEMENT = a.read_excel("discuss")

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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
            self.new_find_element(By.ID, self.ELEMENT["company_official_ask"]).click()

        # 投资机构进入问答编辑器
        elif type == 3:
            self.search_company(company)
            self.new_find_element(By.XPATH, self.ELEMENT["tzjg_name"]).click()
            sleep(3)
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
            x = self.driver.get_window_size()["width"]
            y = self.driver.get_window_size()["height"]
            count = 0
            while True:
                if count > 11:
                    print("-----------滑动找不到热门问答列表----------")
                    break
                else:
                    try:
                        self.driver.find_element_by_xpath(
                            self.ELEMENT["company_hot_question_title"]
                        )
                        break
                    except:
                        self.driver.swipe(0.5 * x, 0.8 * y, 0.5 * x, 0.2 * y, 1200)
                        count += 1
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_all_hot_question"]
            ).click()

        # 投资机构进入热门问答列表
        elif type == 3:
            self.search_company(company)
            self.new_find_element(By.XPATH, self.ELEMENT["tzjg_name"]).click()
            sleep(3)
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
            sleep(3)
            self.new_find_element(By.ID, self.ELEMENT["brand_question_tab"]).click()
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_all_hot_question"]
            ).click()

        # 人员详情页进入热门问答列表
        elif type == 5:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["top_search"]).click()
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
            self.new_find_element(
                By.ID, self.ELEMENT["person_question_tab"], outtime=10
            ).click()
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
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn"):
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn").click()
            self.new_find_element(By.ID, self.ELEMENT["company_self"]).click()
            x = self.driver.get_window_size()["width"]
            y = self.driver.get_window_size()["height"]
            count = 0
            while True:
                if count > 1:
                    print("-----------公司详情页自主信息tab进入热门问答列表滑动找不到入口，请手动查找----------")
                    break
                else:
                    try:
                        self.driver.find_element_by_xpath(
                            self.ELEMENT["company_hot_question_title"]
                        )
                        break
                    except:
                        self.driver.swipe(0.5 * x, 0.8 * y, 0.5 * x, 0.2 * y, 1200)
                        count += 1
            self.new_find_element(
                By.XPATH, self.ELEMENT["company_all_hot_question"]
            ).click()

    def add_pic(self):
        self.new_find_element(By.ID, self.ELEMENT["question_ugc_addpic"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["add_pic_album"]).click()
        # 添加图片超过9张toast校验
        if self.isElementExist(By.XPATH, self.ELEMENT["select_pic"]):
            a = self.new_find_elements(By.XPATH, self.ELEMENT["select_pic"])
            if len(a) > 9:
                for i in range(10):
                    a[i].click()
                b = self.new_find_element(By.XPATH, self.ELEMENT["select_pic_toast"]).text
                self.assertEqual(b, "最多选择9张图片", "从相册添加图片超出提示错误")
                ok = self.new_find_element(By.ID, self.ELEMENT["ok_btn"])
                self.assertEqual(ok.text, "完成(9/9)", "选择图片界面完成按钮数量显示错误")
                ok.click()
                sleep(15)
                delete_btn = self.new_find_elements(
                    By.XPATH, self.ELEMENT["delete_pic"], outtime=10
                )
                self.assertEqual(len(delete_btn), 9, "上传图片数量错误")
                for i in range(9):
                    self.new_find_elements(By.XPATH, self.ELEMENT["delete_pic"])[0].click()
                delete_btn = self.new_find_elements(By.XPATH, self.ELEMENT["delete_pic"])
                self.assertFalse(delete_btn, "删除图片功能错误")
            else:
                for i in range(len(a)):
                    a[i].click()
                ok = self.new_find_element(By.ID, self.ELEMENT["ok_btn"])
                self.assertEqual(ok.text, "完成({}/9)".format(str(len(a))), "选择图片界面完成按钮数量显示错误")
                ok.click()
                sleep(15)
                delete_btn = self.new_find_elements(
                    By.XPATH, self.ELEMENT["delete_pic"], outtime=10
                )
                self.assertEqual(len(delete_btn), len(a), "上传图片数量错误")
                for i in range(len(a)):
                    self.new_find_elements(By.XPATH, self.ELEMENT["delete_pic"])[0].click()
                delete_btn = self.isElementExist(By.XPATH, self.ELEMENT["delete_pic"])
                self.assertFalse(delete_btn, "删除图片功能错误")
        else:
            self.driver.keyevent(4)

    @getimage
    def test_001(self):
        log.info(self.test_001.__doc__)
        try:
            login_status = self.is_login()
            if login_status == True:
                self.logout()
            self.go_question_ugc()
            self.new_find_element(By.ID, self.ELEMENT["send_question"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["question_ugc_toast_1"]),
                "问题编辑器标题少于6个字无提示",
            )
            # 无关联主体toast校验

            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_title").send_keys(
                RandomStr().zh_cn(6)
            )
            title = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_title").text
            self.new_find_element(By.ID, self.ELEMENT["send_question"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["question_ugc_toast_2"]),
                "问题编辑器无关联主体无提示",
            )

            # 关联问题主体
            self.new_find_element(
                By.ID, self.ELEMENT["question_ugc_relation_company"]
            ).click()
            self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/et_search_input"
            ).send_keys("库车县小卖部")
            a = self.new_find_element(
                By.XPATH, "(//*[@resource-id='com.tianyancha.skyeye:id/tv_com_name'])[1]"
            )
            relation_company = a.text
            a.click()
            ugc_relation_company = self.new_find_element(
                By.ID, self.ELEMENT["question_ugc_relation_company"]
            ).text
            self.assertEqual(relation_company, ugc_relation_company, "问题编辑器关联公司添加失败")

            # 描述超长toast
            # content = self.ELEMENT["ugc_content_100"]
            self.new_find_element(By.ID, self.ELEMENT["ugc_content"]).send_keys(RandomStr().zh_cn(110))
            self.new_find_element(By.ID, self.ELEMENT["send_question"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["question_ugc_toast_3"]),
                "问题编辑器描述内容超过100字无提示",
            )

            # 添加图片
            self.new_find_element(By.ID, self.ELEMENT["ugc_content"]).click()
            self.add_pic()
            self.driver.keyevent(4)
            # 查看草稿是否保存标题，关联主体，提示卡片是否恢复展示
            self.new_find_element(By.ID, self.ELEMENT["diacuss_list_send_ask"]).click()
            sleep(3)
            title_saved = self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/et_title"
            ).text
            self.assertEqual(title, title_saved, "问题编辑器未保存草稿")
            ugc_relation_company = self.new_find_element(
                By.ID, self.ELEMENT["question_ugc_relation_company"]
            ).text
            self.assertEqual(relation_company, ugc_relation_company, "问题编辑器草稿关联公司错误")

            # 输入超长标题提示校验
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_title").send_keys(
                RandomStr().zh_cn(51)
            )
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["long_title_tip"]), "标题超出无提示文字"
            )
            self.new_find_element(By.ID, self.ELEMENT["send_question"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["question_ugc_toast_4"]),
                "问题编辑器标题超出点击提交无提示",
            )

            # 正常提交问题

            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_title").send_keys(
                RandomStr().zh_cn(10)
            )
            words = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_title").text
            self.new_find_element(
                By.ID, self.ELEMENT["question_ugc_relation_company"]
            ).click()
            self.new_find_element(
                By.ID, self.ELEMENT["question_ugc_relation_company"]
            ).click()
            self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/et_search_input"
            ).send_keys("库车县小卖部")
            a = self.new_find_element(
                By.XPATH, "(//*[@resource-id='com.tianyancha.skyeye:id/tv_com_name'])[1]"
            )
            ugc_company = a.text
            a.click()
            self.new_find_element(By.ID, self.ELEMENT["ugc_content"]).send_keys(RandomStr().zh_cn(10))
            self.new_find_element(By.ID, self.ELEMENT["send_question"]).click()
            self.login(11099990110, self.account.get_pwd())
            sleep(2)

            # 我的提问列表检验刚提交问题
            my_question_title = self.new_find_element(
                By.XPATH, self.ELEMENT["my_question_title"]
            ).text
            self.assertIn(words, my_question_title, "我的提问列表显示刚提交问题失败")

            # 关联公司校验
            my_question_company = self.new_find_element(
                By.XPATH, "(//*[@resource-id='com.tianyancha.skyeye:id/tv_sub_about'])[1]"
            ).text
            self.assertIn(ugc_company, my_question_company, "我的提问列表关联公司校验失败")

            # 删除问题
            # self.new_find_element(By.XPATH, "(//*[@resource-id='com.tianyancha.skyeye:id/tv_delete'])[1]").click()
            delbtn = self.new_find_elements(
                By.ID, "com.tianyancha.skyeye:id/tv_delete"
            )
            for i in range(len(delbtn)):
                delbtn[0].click()
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["question_ugc_toast_6"]),
                "删除问题toast错误",
            )
            a = self.new_find_elements(By.XPATH, self.ELEMENT["my_question_title"])
            if a == True:
                title = a[0].text
                self.assertNotEqual(title, words, "删除问题失败")
            else:
                pass
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        log.info(self.test_002.__doc__)
        try:
            # 商业头条tab进入热门问答列表
            self.go_hot_question_list()
            # 热门问答进入问题详情页
            self.new_find_element(By.ID, self.ELEMENT["home_question_name"]).click()

            # 不输入回答内容toast校验
            self.new_find_element(By.ID, self.ELEMENT["send_answer"]).click()
            self.new_find_element(By.ID, self.ELEMENT["send_answer_ugc"]).click()
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["answer_ugc_toast_1"]),
                "未输入回答toast校验失败",
            )

            # 回答编辑器输入超限校验
            # long_answer = self.ELEMENT["long_answer"]
            self.new_find_element(By.ID, self.ELEMENT["ugc_content"]).send_keys(RandomStr().zh_cn(510))
            self.new_find_element(By.ID, self.ELEMENT["send_answer_ugc"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["answer_ugc_toast_2"]),
                "回答编辑器描述内容超过500字无提示",
            )

            # 相册添加图片
            self.new_find_element(By.ID, self.ELEMENT["ugc_content"]).send_keys(RandomStr().zh_cn(20))
            self.new_find_element(By.ID, self.ELEMENT["ugc_content"]).click()
            self.add_pic()
            # 发布回答
            self.new_find_element(By.ID, self.ELEMENT["send_answer_ugc"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["answer_ugc_toast_3"]), "回答发布无提示"
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    def test_003(self):
        log.info(self.test_003.__doc__)
        try:
            # 商业头条tab进入热门问答列表
            self.go_hot_question_list()
            # 热门问答进入问题详情页
            self.new_find_element(By.ID, self.ELEMENT["home_question_name"]).click()

            self.new_find_element(By.ID, self.ELEMENT["send_answer"]).click()
            self.new_find_element(By.ID, self.ELEMENT["question_ugc_addpic"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["add_pic_album"]).click()
            if self.isElementExist(By.XPATH, self.ELEMENT["select_pic"]):
                a = self.new_find_elements(By.XPATH, self.ELEMENT["select_pic"])
                a[0].click()
                self.new_find_element(By.ID, self.ELEMENT["ok_btn"]).click()
                sleep(5)
                self.new_find_element(By.ID, self.ELEMENT["send_answer_ugc"]).click()
                self.assertTrue(
                    self.isElementExist(By.XPATH, self.ELEMENT["answer_ugc_toast_3"]),
                    "回答发布一张图片无提示",
                )
            else:
                pass
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_004(self):
        log.info(self.test_004.__doc__)
        try:
            # 进入我的问答tab
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_my_answers").click()
            self.new_find_element(By.XPATH, self.ELEMENT["mytab_myanswer_tab"]).click()
            delbtn = self.new_find_elements(
                By.ID, "com.tianyancha.skyeye:id/tv_delete"
            )
            for i in range(len(delbtn)):
                delbtn[0].click()
            self.assertTrue(
                self.new_find_element(By.XPATH, self.ELEMENT["question_ugc_toast_6"]),
                "删除问题toast错误",
            )
            self.assertFalse(
                self.new_find_element(By.XPATH, self.ELEMENT["answer_list_title"]), "删除回答失败"
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
            self.search_company("北京裕洲信息科技有限公司")
            self.new_find_elements(
                By.ID, self.ELEMENT["search_result_question_title"], outtime=15
            )[0].click()
            a = self.isElementExist(
                By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_question']"
            )
            self.assertTrue(a, "搜索结果页进入有关企业问答列表错误")
            self.new_find_elements(
                By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_question']"
            )[0].click()
            self.new_find_element(By.ID, self.ELEMENT["company_tag"])
            company_name = self.new_find_element(By.ID, self.ELEMENT["company_tag"]).text
            self.assertEqual(company_name, "北京裕洲信息科技有限公司", "问题详情页关联公司标签错误")

            self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/iv_avatar', outtime=10)[
                0
            ].click()
            self.new_find_element(By.XPATH, self.ELEMENT["im_btn"]).click()
            self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/bar_edit_text"
            ).send_keys(RandomStr().zh_cn(20))
            self.driver.keyevent(66)
            self.assertFalse(
                self.isElementExist(By.XPATH, self.ELEMENT["im_vip_toast"]),
                "vip用户进行私信有VIP弹窗",
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["im_edit_massage"]), "VIP进入私信有问题"
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import time
import unittest
import re

log = Logger("查公司_05").getlog()


class Search_companyTest(MyTest, Operation):
    """查公司_05"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_company")

    def search_result_list_check(self, company, company_type=None, index=0):
        # 检查不同公司展示字段方法
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(company)
        legal = self.new_find_elements(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/search_item_legal_title']")[index].text
        money = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_capital']")[index].text
        build_date = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_check_date']")[index].text
        # 0普通公司 1 个体工商户 2个人独资企业 3合伙制企业 4香港企业 5台湾企业 6基金会 7事业单位  8社会组织 9律所
        if company_type == 0:
            goal = "搜索结果页普通公司法定代表人字段校验"
            self.assertEqual(legal, "法定代表人", "错误————%s" % goal)
            goal = "搜索结果页普通公司注册资本字段校验"
            self.assertEqual(money, "注册资本", "错误————%s" % goal)
            goal = "搜索结果页普通公司成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 1:
            goal = "搜索结果页个体工商户经营者字段校验"
            self.assertEqual(legal, "经营者", "错误————%s" % goal)
            goal = "搜索结果页个体工商户注册资本字段校验"
            self.assertEqual(money, "注册资本", "错误————%s" % goal)
            goal = "搜索结果页个体工商户成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 2:
            goal = "搜索结果页个人独资企业投资人字段校验"
            self.assertEqual(legal, "投资人", "错误————%s" % goal)
            goal = "搜索结果页个人独资企业注册资本字段校验"
            self.assertEqual(money, "注册资本", "错误————%s" % goal)
            goal = "搜索结果页个人独资企业成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 3:
            goal = "搜索结果页合伙制企业执行事务合伙人字段校验"
            self.assertEqual(legal, "执行事务合伙人", "错误————%s" % goal)
            goal = "搜索结果页合伙制企业注册资本字段校验"
            self.assertEqual(money, "注册资本", "错误————%s" % goal)
            goal = "搜索结果页合伙制企业成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 4:
            goal = "搜索结果页香港企业董事长字段校验"
            self.assertEqual(legal, "董事长", "错误————%s" % goal)
            goal = "搜索结果页香港企业股本字段校验"
            self.assertEqual(money, "股本", "错误————%s" % goal)
            goal = "搜索结果页香港企业成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 5:
            goal = "搜索结果页台湾企业代表人字段校验"
            self.assertEqual(legal, "代表人", "错误————%s" % goal)
            goal = "搜索结果页台湾企业资本总额字段校验"
            self.assertEqual(money, "资本总额", "错误————%s" % goal)
            goal = "搜索结果页台湾企业核准设立日期字段校验"
            self.assertEqual(build_date, "核准设立日期", "错误————%s" % goal)
        elif company_type == 6:
            goal = "搜索结果页基金会理事长字段校验"
            self.assertEqual(legal, "理事长", "错误————%s" % goal)
            goal = "搜索结果页基金会原始基金字段校验"
            self.assertEqual(money, "原始基金", "错误————%s" % goal)
            goal = "搜索结果页基金会成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 7:
            goal = "搜索结果页事业单位法定代表人字段校验"
            self.assertEqual(legal, "法定代表人", "错误————%s" % goal)
            goal = "搜索结果页事业单位开办资金字段校验"
            self.assertEqual(money, "开办资金", "错误————%s" % goal)
            goal = "搜索结果页事业单位成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
        elif company_type == 8:
            goal = "搜索结果页社会组织法定代表人字段校验"
            self.assertEqual(legal, "法定代表人", "错误————%s" % goal)
            goal = "搜索结果页社会组织资本总额字段校验"
            self.assertEqual(money, "注册资本", "错误————%s" % goal)
            goal = "搜索结果页社会组织成立登记日期字段校验"
            self.assertEqual(build_date, "成立登记日期", "错误————%s" % goal)
        elif company_type == 9:
            goal = "搜索结果页律所负责人字段校验"
            self.assertEqual(legal, "负责人", "错误————%s" % goal)
            goal = "搜索结果页律所注册资本字段校验"
            self.assertEqual(money, "注册资本", "错误————%s" % goal)
            goal = "搜索结果页律所成立日期字段校验"
            self.assertEqual(build_date, "成立日期", "错误————%s" % goal)
    def result_tag(self, company, status=None, index=0):
        # 不同状态标签展示校验
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(company)
        tag = self.new_find_elements(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/search_reg_status_tv']",)[index].text
        # 1开业 2存续 3在业 4注销 5吊销 6吊销未注销 7迁出 8正常
        if status == 1:
            goal = "搜索结果页开业标签校验"
            self.assertEqual(tag, "开业", "错误————%s" % goal)
        elif status == 2:
            goal = "搜索结果页存续标签校验"
            self.assertEqual(tag, "存续", "错误————%s" % goal)
        elif status == 3:
            goal = "搜索结果页在营企业标签校验"
            self.assertEqual(tag, "在营企业", "错误————%s" % goal)
        elif status == 4:
            goal = "搜索结果页注销标签校验"
            self.assertEqual(tag, "注销", "错误————%s" % goal)
        elif status == 5:
            goal = "搜索结果页吊销标签校验"
            self.assertEqual(tag, "吊销", "错误————%s" % goal)
        elif status == 6:
            goal = "搜索结果页吊销未注销标签校验"
            self.assertEqual(tag, "吊销，未注销", "错误————%s" % goal)
        elif status == 7:
            goal = "搜索结果页迁出标签校验"
            self.assertEqual(tag, "迁出", "错误————%s" % goal)
        elif status == 8:
            goal = "搜索结果页正常标签校验"
            self.assertEqual(tag, "正常", "错误————%s" % goal)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/search_clean_iv").click()


    # 001-010检查不同公司展示字段
    @getimage
    def test_CGS_ZSSJGY_0001(self):
        '''普通公司-搜索结果展示字段'''
        log.info(self.test_CGS_ZSSJGY_0001.__doc__)
        self.search_result_list_check("百度", 0)

    @getimage
    def test_CGS_ZSSJGY_0002(self):
        '''个体工商户搜索结果展示字段'''
        log.info(self.test_CGS_ZSSJGY_0002.__doc__)
        self.search_result_list_check("台江区东福食品商行", 1)

    @getimage
    def test_CGS_ZSSJGY_0003(self):
        '''个人独资企业搜索结果展示字段'''
        log.info(self.test_CGS_ZSSJGY_0003.__doc__)
        self.search_result_list_check("深圳市恒昌餐饮设备企业", 2)

    @getimage
    def test_CGS_ZSSJGY_0004(self):
        '''合伙制企业搜索结果展示字段'''
        log.info(self.test_CGS_ZSSJGY_0004.__doc__)
        self.search_result_list_check("深圳四开股权投资基金（有限合伙）", 3)

    @getimage
    def test_CGS_ZSSJGY_0005(self):
        '''香港企业搜索结果展示字段'''
        log.info(self.test_CGS_ZSSJGY_0005.__doc__)
        self.search_result_list_check("联升科技有限公司", 4)

    @getimage
    def test_CGS_ZSSJGY_0006(self):
        '''台湾企业搜索结果展示字段'''
        log.info(self.test_CGS_ZSSJGY_0006.__doc__)
        self.search_result_list_check("华润雪花啤酒有限公司", 5)

    @getimage
    def test_CGS_ZSSJGY_0007(self):
        '''基金会搜索结果展示字段+无状态标签'''
        log.info(self.test_CGS_ZSSJGY_0007.__doc__)
        goal = "搜索结果页无公司状态标签"
        self.search_result_list_check("老牛基金会", 6)
        tag = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name'and @text='老牛基金会']//following-sibling::android.widget.TextView",)
        self.assertFalse(tag, "错误————%s" % goal)

    @getimage
    def test_CGS_ZSSJGY_0008(self):
        '''事业单位搜索结果展示字段+无状态标签'''
        log.info(self.test_CGS_ZSSJGY_0008.__doc__)
        self.search_result_list_check("中山大学", 7)

    @getimage
    def test_CGS_ZSSJGY_0009(self):
        '''社会组织搜索结果展示字段+无状态标签'''
        log.info(self.test_CGS_ZSSJGY_0009.__doc__)
        self.search_result_list_check("中国注册会计师协会", 8)

    @getimage
    def test_CGS_ZSSJGY_0010(self):
        '''律师事务所搜索结果展示字段+无状态标签'''
        log.info(self.test_CGS_ZSSJGY_0010.__doc__)
        self.search_result_list_check("天津振华律师事务所", 9)

    @getimage
    def test_CGS_ZSSJGY_0011(self):
        '''搜索结果页-自主信息'''
        log.info(self.test_CGS_ZSSJGY_0010.__doc__)

        goal = ["搜索结果页自主信息跳转自主信息页", "搜索结果页自主信息展示"]
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("安徽国讯芯微科技有限公司")
        claim_info = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/rl_claim_info")
        self.assertTrue(claim_info, "错误————%s" % goal[0])
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/rl_claim_info").click()
        company_detail_claim_info = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_group_title'and @text='业务标签']")
        self.assertTrue(company_detail_claim_info, "错误————%s" % goal[1])

    @getimage
    def test_CGS_ZSSJGY_0012(self):
        '''搜索结果页-无结果'''
        log.info(self.test_CGS_ZSSJGY_0012.__doc__)
        goal = "搜索结果页无结果"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("与物无忤呜呜")
        no_result = self.isElementExist(By.XPATH, "//*[@class='android.widget.TextView' and @text='抱歉，没有找到相关企业！']")
        self.assertTrue(no_result, "错误————%s" % goal)

    @getimage
    def test_CGS_ZSSJGY_0013(self):
        '''搜索结果页-搜索结果展示'''
        log.info(self.test_CGS_ZSSJGY_0013.__doc__)
        goal = [
            "搜索公司列表展示-logo",
            "搜索公司列表展示-公司名称",
            "搜索公司列表展示-状态标签",
            "搜索公司列表展示-属性标签",
            "搜索公司列表展示-法定代表人",
            "搜索公司列表展示-注册资本",
            "搜索公司列表展示-成立日期"]
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
        test_01 = self.isElementExist(By.CLASS_NAME, self.ELEMENT["company_logo"])
        test_02 = self.isElementExist(By.XPATH, self.ELEMENT["company_name"])
        test_03 = self.isElementExist(By.XPATH, self.ELEMENT["status_tag"])
        test_04 = self.isElementExist(By.XPATH, self.ELEMENT["attribute_tag"])
        test_05 = self.isElementExist(By.XPATH, self.ELEMENT["legal_representative"])
        test_06 = self.isElementExist(By.XPATH, self.ELEMENT["registered_capital"])
        test_07 = self.isElementExist(By.XPATH, self.ELEMENT["date_establishment"])
        self.assertTrue(test_01, "错误————%s" % goal[0])
        self.assertTrue(test_02, "错误————%s" % goal[1])
        self.assertTrue(test_03, "错误————%s" % goal[2])
        self.assertTrue(test_04, "错误————%s" % goal[3])
        self.assertTrue(test_05, "错误————%s" % goal[4])
        self.assertTrue(test_06, "错误————%s" % goal[5])
        self.assertTrue(test_07, "错误————%s" % goal[6])
        # 公司有logo,关键词标红

    @getimage
    def test_CGS_ZSSJGY_0014(self):
        '''搜索结果页-超长名称'''
        log.info(self.test_CGS_ZSSJGY_0014.__doc__)

        goal = "搜索结果页超长名称公司全展示"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("宝鸡有一群")
        company_name = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_name").text
        company_name1 = "宝鸡有一群怀揣着梦想的少年相信在牛大叔的带领下会创造生命的奇迹网络科技有限公司"
        self.assertEqual(company_name, company_name1, "错误————%s" % goal)

    # 015-022检查状态标签
    # 1开业 2存续 3在业 4注销 5吊销 6吊销未注销 7迁出 8正常
    @getimage
    def test_CGS_ZSSJGY_0015(self):
        '''搜索结果页-企业状态标签-开业'''
        log.info(self.test_CGS_ZSSJGY_0015.__doc__)
        self.result_tag("西安普林房地产开发有限责任公司", 1)

    @getimage
    def test_CGS_ZSSJGY_0016(self):
        '''搜索结果页-企业状态标签-存续'''
        log.info(self.test_CGS_ZSSJGY_0016.__doc__)
        self.result_tag("鞍山锦阳建材贸易有限公司", 2)

    @getimage
    def test_CGS_ZSSJGY_0017(self):
        '''搜索结果页-企业状态标签-在业'''
        log.info(self.test_CGS_ZSSJGY_0017.__doc__)
        self.result_tag("广东省粤科金融集团有限公司", 3)

    @getimage
    def test_CGS_ZSSJGY_0018(self):
        '''搜索结果页-企业状态标签-注销'''
        log.info(self.test_CGS_ZSSJGY_0018.__doc__)
        self.result_tag("深圳市宝安区共乐富临塑胶电器厂", 4)

    @getimage
    def test_CGS_ZSSJGY_0019(self):
        '''搜索结果页-企业状态标签-吊销'''
        log.info(self.test_CGS_ZSSJGY_0019.__doc__)
        self.result_tag("北京市京兴织袜厂", 5)

    @getimage
    def test_CGS_ZSSJGY_0020(self):
        '''搜索结果页-企业状态标签-吊销未注销'''
        log.info(self.test_CGS_ZSSJGY_0020.__doc__)
        self.result_tag("广安市恒星达纺织品有限公司", 6)

    @getimage
    def test_CGS_ZSSJGY_0021(self):
        '''搜索结果页-企业状态标签-迁出'''
        log.info(self.test_CGS_ZSSJGY_0021.__doc__)
        self.result_tag("北京清华大学企业集团", 7)

    @getimage
    def test_CGS_ZSSJGY_0022(self):
        '''搜索结果页-企业状态标签-正常'''
        log.info(self.test_CGS_ZSSJGY_0022.__doc__)
        self.result_tag("北京大成律师事务所", 8)

    @getimage
    def test_CGS_ZSSJGY_0023(self):
        '''搜索结果页-项目'''
        log.info(self.test_CGS_ZSSJGY_0023.__doc__)
        goal = "搜索项目出现对应公司"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("天眼查")
        company = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[0]
        name_list = company.text
        name = "北京天眼查科技有限公司"
        self.assertEqual(name, name_list, "错误————%s" % goal)
        company.click()
        name_detail = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/firm_detail_name_tv").text
        goal = "搜索项目出现对应公司进入公司详情页"
        self.assertEqual(name_list, name_detail, "错误————%s" % goal)

    @getimage
    def test_CGS_ZSSJGY_0024(self):
        '''搜索结果页-搜索结果无属性标签，展示字段内容为空'''
        log.info(self.test_CGS_ZSSJGY_0024.__doc__)
        goal_02 = "搜索结果页无属性标签"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("兆协投资")
        tag = self.isElementExist(By.XPATH,"(//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name'])[1]/../following-sibling::*[@resource-id='com.tianyancha.skyeye:id/rl_label']",)
        self.assertFalse(tag, "错误————%s" % goal_02)

        goal_03 = ["搜索结果页法人为空", "搜索结果页注册资本为空", "搜索结果页成立日期为空"]
        legal_man = self.new_find_element(By.XPATH,"(//*[@resource-id='com.tianyancha.skyeye:id/search_legal_man_tv'])[1]").text
        money = self.new_find_element(By.XPATH,"(//*[@resource-id='com.tianyancha.skyeye:id/search_reg_capital_tv'])[1]").text
        date = self.new_find_element(By.XPATH,"(//*[@resource-id='com.tianyancha.skyeye:id/search_estiblish_time_tv'])[1]").text
        self.assertEqual(legal_man, "-", "错误————%s" % goal_03[0])
        self.assertEqual(money, "-", "错误————%s" % goal_03[1])
        self.assertEqual(date, "-", "错误————%s" % goal_03[2])

    @getimage
    def test_CGS_ZSSJGY_0025(self):
        '''搜索结果页-地址'''
        log.info(self.test_CGS_ZSSJGY_0025.__doc__)
        goal = "搜索地址显示结果"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("北京市海淀区知春路65号院")
        address = self.isElementExist(By.XPATH,"(//*[@resource-id='com.tianyancha.skyeye:id/search_match_field_content_tv'  and contains(@text,'北京市海淀区知春路65号院')])[2]")
        self.assertTrue(address, "错误————%s" % goal)

if __name__ == "__main__":
    unittest.main()

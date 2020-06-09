# -*- coding: utf-8 -*-
# @Time    : 2020-03-02 16:36
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : company_detail_business_info.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.ReadData import Read_Ex
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
from Providers.logger import Logger
from common.check_rules import *
import re
from Providers.account.account import Account


excel = Read_Ex()
elements = excel.read_excel("companydetailsunkai")
log = Logger("企业背景").getlog()


# 企业背景-工商信息
class TestBusinessInfo(MyTest, Operation):
    account = Account()
    username = account.get_account('vip')
    password = account.get_pwd()

    def into_company_detail(self, company):
        """
        通过搜索进入公司详情页，搜索结果选择第一条
        :param company: 搜索公司名称
        :return: None
        """
        self.new_find_element(By.ID, elements["index_search_input"]).click()
        self.new_find_element(By.ID, elements["search_result_input"]).send_keys(company)
        self.new_find_elements(By.ID, elements["search_result_item"])[0].click()

    # def swipe_up_while_ele_located(self, *loc, click=False, time=10, group=False):
    #     """
    #     定位不到元素向上滑动循环定位直到达到最大次数限制并且点击
    #     :param time: 查找次数
    #     :param loc: 定位元素
    #     :param click: 是否点击找到的元素
    #     :param group: 是否使用find_elements
    #     :return: None
    #     """
    #     count = 0
    #     timeout = 8
    #     screen_size = self.driver.get_window_size()
    #     ele = None
    #     while True:
    #         if count == time:
    #             break
    #         else:
    #             if group:
    #                 ele = self.new_find_elements(*loc, outtime=timeout)
    #             else:
    #                 ele = self.new_find_element(*loc, outtime=timeout)
    #         if ele:
    #             if click and not group:
    #                 ele.click()
    #             break
    #         else:
    #             self.driver.swipe(
    #                 0.5 * screen_size["width"],
    #                 0.8 * screen_size["height"],
    #                 0.5 * screen_size["width"],
    #                 0.4 * screen_size["height"],
    #                 1500,
    #             )
    #             count += 1
    #             timeout = 3
    #     return ele

    @getimage
    def test_1_registration_info_1(self):
        """企业背景-工商信息-登记信息-vip-part-1"""
        log.info(self.__doc__)
        if not self.is_login():
            self.login(self.username, self.password)
        check = UnifiedSocialCreditIdentifier()
        self.into_company_detail("京东数字科技控股有限公司")
        log.info("case --- 京东数字科技控股有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["business_info"], click=True)

        # 查看历史工商信息
        log.info("查看历史工商信息")
        self.new_find_element(By.ID, elements["history_business"]).click()
        history_business_title = self.new_find_element(
            By.ID, elements["app_page_title"], outtime=15
        ).text
        self.assertEqual(history_business_title, "历史工商信息", "跳转历史工商信息失败")
        self.driver.keyevent(4)

        # 法定代表人跳转
        log.info("法定代表人跳转")
        self.new_find_element(By.ID, elements["person"]).click()
        jump_flag = self.isElementExist(By.ID, elements["person_detail_title"])
        self.assertTrue(jump_flag, "工商信息法定代表人跳转失败")
        self.driver.keyevent(4)

        # 他有xxx家公司跳转
        log.info("他有xxx家公司跳转")
        self.new_find_element(By.ID, elements["have_company"]).click()
        company_flag = self.isElementExist(By.ID, elements["person_detail_title"])
        self.assertTrue(company_flag, "他有xx家公司跳转失败")
        self.driver.keyevent(4)

        # 成立日期
        log.info("成立日期")
        create_time = self.new_find_element(By.ID, elements["create_time"]).text
        time_format = check_time(create_time, is_compare=True)
        self.assertTrue(time_format, "成立时间{}格式展示不正确".format(create_time))

        # 经营状态
        log.info("经营状态")
        status = self.new_find_element(By.ID, elements["status"]).text
        self.assertIn(
            status, ("在业", "存续", "吊销", "注销", "迁出"), "经营状态{}展示错误".format(status)
        )

        # 注册资本
        log.info("注册资本")
        capital = self.new_find_element(By.ID, elements["capital"]).text
        capital_flag = is_bill_available(capital)
        self.assertTrue(capital_flag, "注册资本{}展示错误".format(capital))

        # 实缴资本
        log.info("实缴资本")
        real_capital = self.new_find_element(By.ID, elements["real_capital"]).text
        real_capital_flag = is_bill_available(real_capital)
        self.assertTrue(real_capital_flag, "实缴资本{}展示错误".format(real_capital))

        # 统一社会信用代码
        log.info("统一社会信用代码")
        credit_code = self.new_find_element(By.ID, elements["credit_code"]).text
        credit_flag = check.check_social_credit_code(credit_code)
        self.assertTrue(credit_flag, "统一社会信用代码{}校验未通过".format(credit_code))

        # 工商注册号
        log.info("工商注册号")
        business_code = self.new_find_element(By.ID, elements["business_code"]).text
        business_code_flag = re.match(r"^\d{15}$", business_code)
        self.assertIsNotNone(business_code_flag, "工商注册号{}校验未通过".format(business_code))

        # 组织机构代码
        log.info("组织机构代码")
        organize_code = self.new_find_element(By.ID, elements["organize_code"]).text
        organize_flag = check.check_organization_code(organize_code)
        self.assertTrue(organize_flag, "组织机构代码{}校验未通过".format(organize_code))

        # 纳税人识别号
        log.info("纳税人识别号")
        tax_code = self.new_find_element(By.ID, elements["tax_code"]).text
        tax_flag = check.check_tax_code(tax_code)
        self.assertTrue(tax_flag, "纳税人识别号{}校验未通过".format(tax_code))

        # 纳税人资质
        log.info("纳税人资质")
        tax_person = self.new_find_element(By.ID, elements["tax_person"]).text
        self.assertEqual(tax_person, "-", "纳税人资质{}校验失败".format(tax_person))

    @getimage
    def test_2_registration_info_2(self):
        """企业背景-工商信息-登记信息-vip-part-2"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("河北苹乐面粉机械集团有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["business_info"], click=True)

        # 企业类型
        log.info("企业类型")
        company_type = self.new_find_element(By.ID, elements["company_type"]).text
        self.assertEqual(
            company_type, "有限责任公司(自然人投资或控股)", "企业类型{}展示错误".format(company_type)
        )

        # 行业
        log.info("行业")
        industry = self.new_find_element(By.ID, elements["industry"]).text
        self.assertEqual(industry, "专用设备制造业", "行业{}校验失败".format(industry))

        # 营业期限
        log.info("营业期限")
        over_time = self.new_find_element(By.ID, elements["over_time"]).text
        if over_time == "-":
            self.assertEqual(over_time, "-", "营业期限{}格式校验错误".format(over_time))
        else:
            check_result = re.findall(
                "[1,2][0, 9][0-9][0-9]-[0-9][0-9]-[0-3][0-9]", over_time
            )
            self.assertEqual(len(check_result), 2, "营业期限{}格式校验错误".format(over_time))

        # 人员规模
        log.info("人员规模")
        person_size = self.swipe_up_while_ele_located(
            By.ID, elements["person_size"]
        ).text
        person_size_flag = re.match(r"^\d(.*?)人$", person_size)
        self.assertTrue(
            person_size == "-" or person_size_flag, "人员规模{}规则校验失败".format(person_size)
        )

        # 参保人数
        log.info("参保人数")
        protect_person = self.swipe_up_while_ele_located(
            By.ID, elements["protect_person"]
        ).text
        protect_person_flag = re.match(r"^\d*", protect_person)
        self.assertTrue(
            protect_person == "-" or protect_person_flag,
            "参保人数{}规则校验失败".format(protect_person),
        )

        # 英文名称
        log.info("英文名称")
        english_name = self.swipe_up_while_ele_located(
            By.ID, elements["english_name"]
        ).text
        english_name_flag = re.match(r"^[a-zA-Z](.*?)Ltd\.$", english_name)
        self.assertTrue(
            english_name == "-" or english_name_flag, "英文名称{}校验失败".format(english_name),
        )

        # 曾用名
        log.info("曾用名")
        past_name = self.swipe_up_while_ele_located(By.ID, elements["past_name"]).text
        self.assertTrue(
            past_name == "-" or len(past_name) > 5, "曾用名{}校验失败".format(past_name)
        )

        # 登记机关
        log.info("登记机关")
        reg_institute = self.swipe_up_while_ele_located(
            By.ID, elements["reg_institute"]
        ).text
        self.assertTrue(
            reg_institute == "-" or len(reg_institute) > 5,
            "登记机关{}校验失败".format(reg_institute),
        )

        # 核准日期
        log.info("核准日期")
        approved_time = self.swipe_up_while_ele_located(
            By.ID, elements["approved_time"]
        ).text
        approved_time_flag = re.match(
            "[1,2][0, 9][0-9][0-9]-[0-9][0-9]-[0-3][0-9]", approved_time,
        )
        self.assertTrue(
            approved_time == "-" or approved_time_flag,
            "核准日期{}校验失败".format(approved_time),
        )

        # 注册地址
        log.info("注册地址")
        reg_address = self.swipe_up_while_ele_located(By.ID, elements["reg_address"])
        if reg_address.text == "-":
            self.assertEqual(reg_address.text, "-", "注册地址无数据展示错误")
        else:
            reg_address.click()
            map_title = self.new_find_element(By.ID, elements["app_page_title"]).text
            self.assertEqual(map_title, "公司地图", "注册地址跳转失败")
            self.driver.keyevent(4)

        # 经营范围
        log.info("经营范围")
        business_scope = self.swipe_up_while_ele_located(
            By.ID, elements["business_scope"]
        ).text
        self.assertTrue(
            business_scope == "-" or len(business_scope) > 50,
            "经营范围{}校验失败".format(business_scope),
        )

    @getimage
    def test_3_shareholders_info_company(self):
        """企业背景-工商信息-股东信息-公司"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("北京转转精神科技有限责任公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["business_info"], click=True)

        # 股东是公司跳转
        log.info("股东是公司跳转")
        company_holder = self.swipe_up_while_ele_located(
            By.ID, elements["shareholders_info"], group=True
        )[0]
        company_name = company_holder.text
        company_holder.click()
        detail_company_name = self.new_find_element(
            By.ID, elements["detail_company_name"]
        ).text
        self.assertEqual(
            company_name,
            detail_company_name,
            "公司股东{}名称和详情页{}不一致".format(company_name, detail_company_name),
        )
        self.driver.keyevent(4)

        # 股权结构跳转
        log.info("股权结构跳转")
        self.driver.swipe(400, 1500, 400, 1450, 1000)
        structure_map = self.new_find_elements(By.ID, elements["structure_map"])[0]
        structure_map.click()
        page_title = self.new_find_element(
            By.ID, elements["app_page_title"], outtime=15
        ).text
        self.assertEqual(page_title, "股权结构", "股权结构图跳转失败")
        self.driver.keyevent(4)

        # 认缴出资额
        log.info("认缴出资额")
        money_num = self.swipe_up_while_ele_located(
            By.ID, elements["money_num"], group=True
        )[1].text
        money_num_flag = is_bill_available(money_num)
        self.assertTrue(money_num_flag, "公司股东认缴出资额{}校验失败".format(money_num))

        # 认缴出资日期
        log.info("认缴出资日期")
        money_time = self.new_find_elements(By.ID, elements["money_time"])[1].text
        money_time_flag = check_time(money_time)
        self.assertTrue(money_time_flag, "公司股东认缴出资日期{}校验失败".format(money_time_flag))

        # 持股比例
        log.info("持股比例")
        holder_percent = self.swipe_up_while_ele_located(
            By.ID, elements["holder_percent"], group=True
        )[0].text
        holder_percent_flag = is_percentage_available(holder_percent)
        self.assertTrue(holder_percent_flag, "公司股东持股比例{}校验失败".format(holder_percent))

    @getimage
    def test_4_shareholders_info_human(self):
        """企业背景-工商信息-股东信息-人"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("字节跳动有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["business_info"], click=True)

        # 股东是人跳转
        log.info("股东是人跳转")
        human_holder = self.swipe_up_while_ele_located(
            By.ID, elements["shareholders_info"], group=True
        )[0]
        human_name = human_holder.text
        human_holder.click()
        detail_human_name = self.new_find_element(
            By.ID, elements["detail_human_name"]
        ).text
        self.assertEqual(
            human_name,
            detail_human_name,
            "人股东{}名称和详情页{}不一致".format(human_name, detail_human_name),
        )
        self.driver.keyevent(4)

        # 他有xx家公司跳转
        log.info("他有xx家公司跳转")
        self.new_find_elements(By.ID, elements["has_company"])[0].click()
        human_title = self.new_find_element(By.ID, elements["person_detail_title"]).text
        self.assertEqual(human_title, "人员详情", "股东信息人他有xx家公司跳转失败")
        self.driver.keyevent(4)

        # 认缴出资额
        log.info("认缴出资额")
        money_num = self.swipe_up_while_ele_located(
            By.ID, elements["money_num"], group=True
        )[1].text
        money_num_flag = is_bill_available(money_num)
        self.assertTrue(money_num_flag, "人股东认缴出资额{}校验失败".format(money_num))

        # 认缴出资日期
        log.info("认缴出资日期")
        money_time = self.new_find_elements(By.ID, elements["money_time"])[1].text
        money_time_flag = check_time(money_time)
        self.assertTrue(money_time_flag, "人股东认缴出资日期{}校验失败".format(money_time_flag))

        # 持股比例
        log.info("持股比例")
        holder_percent = self.swipe_up_while_ele_located(
            By.ID, elements["holder_percent"], group=True
        )[0].text
        holder_percent_flag = is_percentage_available(holder_percent)
        self.assertTrue(holder_percent_flag, "人股东持股比例{}校验失败".format(holder_percent))

    @getimage
    def test_5_main_person_and_change_list(self):
        """企业背景-工商信息-主要人员"""
        log.info(self.__doc__)
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("北京天眼查科技有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["business_info"], click=True)

        # 主要人员-人员名称跳转
        log.info("主要人员-人员名称跳转")
        main_person = self.swipe_up_while_ele_located(
            By.ID, elements["main_person"], group=True
        )[0]
        main_person.click()
        person_title = self.new_find_element(
            By.ID, elements["person_detail_title"]
        ).text
        self.driver.keyevent(4)
        self.assertEqual(person_title, "人员详情", "主要人员{}跳转失败".format(person_title))

        # 主要人员-他有xx家公司跳转
        log.info("主要人员-他有xx家公司跳转")
        self.new_find_elements(By.XPATH, elements["main_has_company"])[0].click()
        person_title = self.new_find_element(
            By.ID, elements["person_detail_title"]
        ).text
        self.driver.keyevent(4)
        self.assertEqual(
            person_title, "人员详情", "主要人员-他有xx家公司{}跳转失败".format(person_title)
        )

        # 变更记录
        log.info("变更记录")
        # 变更时间
        log.info("变更时间")
        change_time = self.swipe_up_while_ele_located(
            By.ID, elements["change_time"], group=True
        )[0].text
        self.assertTrue(check_time(change_time, is_compare=True))

        # 变更内容
        log.info("变更内容")
        change_before = self.swipe_up_while_ele_located(
            By.ID, elements["change_before"], group=True
        )[0].text
        self.assertIsNot(change_before, "", "变更记录前内容为空")
        change_after = self.new_find_elements(By.ID, elements["change_after"])[0].text
        self.assertIsNot(change_after, "", "变更记录后内容为空")

    @getimage
    def test_6_company_branch(self):
        """企业背景-工商信息-分支机构"""
        log.info(self.__doc__)
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("长江证券股份有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["business_info"], click=True)
        # 分支机构
        log.info("分支机构")
        company_branch = self.swipe_up_while_ele_located(
            By.ID, elements["company_branch"], times=30, group=True
        )[0]
        company_branch_name = company_branch.text
        company_branch.click()
        jump_name = self.new_find_element(By.ID, elements["detail_company_name"]).text
        self.driver.keyevent(4)
        self.assertEqual(
            company_branch_name,
            jump_name,
            "分支机构跳转名称{}和详情页名称{}不一致".format(company_branch_name, jump_name),
        )

    def test_7_release_account(self):
        self.account.release_account(self.username, 'vip')

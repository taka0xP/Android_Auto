from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import time
import unittest
import re
import random

log = Logger("查公司_04").getlog()


class Search_companyTest(MyTest, Operation):
    """查公司_04"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_company")

    # vip：11099990154(无所属公司及姓名)

    def is_valid_date(self, str):
        """判断日期字符串格式是否为YYYY.MM.DD"""
        try:
            time.strptime(str, "%Y.%m.%d")
            return True
        except:
            return False
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
    def go_export(self,keyword):
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(keyword)
        self.new_find_element(By.ID, self.ELEMENT["export_data"]).click()
    def get_title_name(self):
        '''获取页面title名称'''
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return text
    def page_back(self):
        """页面返回"""
        self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_back').click()

    @getimage
    def test_CGS_ZSSJGY_0001(self):
        '''搜索结果页-数据导出-未登录'''
        log.info(self.test_CGS_ZSSJGY_0001.__doc__)

        goal = "未登录下点击导出数据弹出登陆页面"
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("北京金堤科技有限公司")
        result = self.login_page_check(1,self.ELEMENT["export_data"])
        self.assertTrue(result,"错误————%s"%goal)

    @getimage
    def test_CGS_ZSSJGY_0002(self):
        '''搜索结果页-数据导出-非VIP'''
        log.info(self.test_CGS_ZSSJGY_0002.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        account = self.account.get_account()
        self.login(account,self.account.get_pwd())

        goal = "非vip账号已登陆点击数据导出弹出开通vip弹框"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("北京金堤科技有限公司")
        self.new_find_element(By.ID, self.ELEMENT["export_data"]).click()
        text = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_top_title').text
        self.assertEqual(text,'开通VIP会员可导出数据',"错误————%s" % goal)

        self.logout()
        self.account.release_account(account)

    @getimage
    def test_CGS_ZSSJGY_0003(self):
        '''搜索结果页-数据导出-VIP导出不超过5000条'''
        log.info(self.test_CGS_ZSSJGY_0003.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login("11099990154","ef08beca")

        goal_01 = "vip账号已登陆点击数据导出公司数据弹框"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("北京金堤科技有限公司")
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_search_title').text
        count = int(re.sub("\D","",text))
        if count <= 5000:
            self.new_find_element(By.ID, self.ELEMENT["export_data"]).click()
            result = self.isElementExist(By.XPATH, self.ELEMENT["toast"])
            if result == True:
                log.error("今日导出次数已达上限")
            else:
                result_01 = self.isElementExist(By.ID, self.ELEMENT["mailbox_pop_up"])
                self.assertTrue(result_01, "错误————%s" % goal_01)

                goal_02 = "导出公司数据弹框中点击x回到搜索结果页"
                self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_finish').click()
                text_02 = self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).text
                self.assertEqual(text_02, "北京金堤科技有限公司", "错误————%s" % goal_02)

                goal_03 = "导出公司数据弹框中点击一键清空按钮清空输入框内容"
                time.sleep(1)
                self.new_find_element(By.ID, self.ELEMENT["export_data"]).click()
                self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).send_keys("123456")
                self.new_find_element(By.ID, self.ELEMENT["mailbox_search_clean"]).click()
                text_03 = self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).text
                self.assertEqual(text_03, "请输入你的邮箱地址", "错误————%s" % goal_03)

                goal_04 = "邮箱格式不正确点击立即导出,taost：邮箱格式不正确"
                self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).send_keys("123456")
                self.new_find_element(By.ID, self.ELEMENT["btn_pos"]).click()
                text_04 = self.new_find_element(By.XPATH, self.ELEMENT["toast"]).text
                self.assertEqual(text_04, "邮箱格式不正确", "错误————%s" % goal_04)

                goal_05 = "邮箱为空点击发送,taost：邮箱不能为空"
                self.new_find_element(By.ID, self.ELEMENT["mailbox_search_clean"]).click()
                time.sleep(1)
                self.new_find_element(By.ID, self.ELEMENT["btn_pos"]).click()
                text_05 = self.new_find_element(By.XPATH, self.ELEMENT["toast"]).text
                self.assertEqual(text_05, "邮箱不能为空", "错误————%s" % goal_05)

                goal_06 = "邮箱格式正确点击发送,taost：发送成功，请注意查收邮件"
                self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).send_keys("lijiaying@tianyancha.com")
                self.new_find_element(By.ID, self.ELEMENT["btn_pos"]).click()
                text_06 = self.new_find_element(By.XPATH, self.ELEMENT["toast"]).text
                self.assertEqual(text_06, "发送成功，请注意查收邮件", "错误————%s" % goal_06)

                goal_07 = "再次输入不同关键词导出数据时默认为上一次输入的有效邮箱"
                self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
                self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("北京百度网讯网讯科技有限公司")
                self.new_find_element(By.ID, self.ELEMENT["export_data"]).click()
                text_07 = self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).text
                self.assertEqual(text_07, "lijiaying@tianyancha.com", "错误————%s" % goal_07)
                self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_finish').click()

        else:
            log.error('case搜索结果超出5000条')

    @getimage
    def test_CGS_ZSSJGY_0004(self):
        '''搜索结果页-数据导出-VIP导出超过5000条'''
        log.info(self.test_CGS_ZSSJGY_0004.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login("11099990154", "ef08beca")
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        search_word = '京东科技'
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(search_word)
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_search_title').text
        search_num = int(re.sub("\D", "", text))
        if search_num > 5000:
            goal_01 = '点击数据导出弹出导出公司数据弹框'
            self.new_find_element(By.ID, self.ELEMENT["export_data"]).click()
            text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/txt_title').text
            char = '导出公司数据'
            self.assertEqual(text_01,char,msg='错误————%s'%goal_01)

            goal_02 = "vip账号超过5000条数据时点击数据导出展示增值导出服务入口"
            result_02 = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/rl_value_type')
            self.assertTrue(result_02,msg='错误————%s'%goal_02)

            goal_021 = '默认选中VIP导出服务'
            result_021 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/rl_common_type').is_selected()
            self.assertTrue(result_021,msg='错误————%s'%goal_021)

            goal_022 = '超出5000数据2分一条'
            price_022 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_price').text
            search_price = str((search_num-5000)*0.02)
            self.assertEqual(price_022,search_price,msg='错误————%s' % goal_022)

            goal_023 = "导出公司数据弹框中点击一键清空按钮清空输入框内容"
            time.sleep(1)
            self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).send_keys("123456")
            self.new_find_element(By.ID, self.ELEMENT["mailbox_search_clean"]).click()
            text_023 = self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).text
            self.assertEqual(text_023, "请输入你的邮箱地址", "错误————%s" % goal_023)

            goal_024 = "邮箱格式不正确点击立即导出,taost：邮箱格式不正确"
            self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).send_keys("123456")
            self.new_find_element(By.ID, self.ELEMENT["btn_pos"]).click()
            text_024 = self.new_find_element(By.XPATH, self.ELEMENT["toast"]).text
            self.assertEqual(text_024, "邮箱格式不正确", "错误————%s" % goal_024)

            goal_025 = "邮箱为空点击发送,taost：邮箱不能为空"
            self.new_find_element(By.ID, self.ELEMENT["mailbox_search_clean"]).click()
            time.sleep(1)
            self.new_find_element(By.ID, self.ELEMENT["btn_pos"]).click()
            text_025 = self.new_find_element(By.XPATH, self.ELEMENT["toast"]).text
            self.assertEqual(text_025, "邮箱不能为空", "错误————%s" % goal_025)

            goal_03 = '导出数据弹窗展示的数据量与搜索结果一致'
            text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_export_count').text
            toast_num = int(re.sub("\D", "", text_03))
            self.assertEqual(toast_num,search_num,msg='错误————%s'%goal_03)

            goal_04 = '有输入邮箱输入框'
            result_04 = self.isElementExist(By.ID, self.ELEMENT["mailbox_search_box"])
            email = "lijiaying@tianyancha.com"
            self.new_find_element(By.ID, self.ELEMENT["mailbox_search_box"]).send_keys(email)
            self.assertTrue(result_04,msg='错误————%s'%goal_04)

            goal_05 = '点击增值导出入口进入支付页面带入搜索词'
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/rl_value_type').click()
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_pos').click()
            text_05 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_name').text
            self.assertEqual(text_05,search_word,msg='错误————%s'%goal_05)

            goal_06 = '导出数量带入支付页面,数量小于或等于搜索数量'
            realCount = int(self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_count').text)
            if realCount <= search_num:
                result_06 = True
            else:
                result_06 = False
            self.assertTrue(result_06,msg='错误————%s'%goal_06)

            goal_07 = '超出5000数据2分一条'
            text_07 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_price').text
            time.sleep(5)
            num = int(realCount)
            price = (num-5000)*0.02
            num_07 = text_07.replace('¥ ','')
            if '.' in num_07:
                money = float(num_07)
            else:
                money = int(num_07)
            log.info(money)
            log.info(price)
            self.assertEqual(money,price,msg='错误————%s'%goal_07)

            goal_08 = '填写邮箱带入支付页'
            text_08 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/et_email').text
            self.assertEqual(text_08,email,msg='错误————%s'%goal_08)

            goal_09 = '点击？弹出提示弹框'
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/iv_mark').click()
            word = '查询结果因数据差异性会有上下浮动情况，以实际导出数量为准。'
            text_09 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/txt_msg').text
            self.assertEqual(text_09,word,msg='错误————%s'%goal_09)

            goal_10 = '点击我知道了返回增值导出支付页'
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_pos').click()
            result = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name' and @text='%s']"%search_word)
            self.assertTrue(result,msg='错误————%s'%goal_10)
        else:
            log.error('case搜索结果不足5000条')

    @getimage
    def test_CGS_ZSSJGY_0005(self):
        '''搜索结果页-批量联系-未登录'''
        log.info(self.test_CGS_ZSSJGY_0005.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()

        goal = "未登录点击批量联系跳转登陆页"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("土木建筑")
        result = self.login_page_check(1, self.ELEMENT["batch_contact"])
        self.assertTrue(result, "错误————%s" % goal)

    @getimage
    def test_CGS_ZSSJGY_0006(self):
        '''搜索结果页-批量联系-非VIP'''
        log.info(self.test_CGS_ZSSJGY_0006.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        account = self.account.get_account()
        self.login(account, self.account.get_pwd())

        goal = "非vip点击批量联系提示开通vip"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("土木建筑")
        self.new_find_element(By.ID,self.ELEMENT["batch_contact"]).click()
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_top_title').text
        self.assertEqual(text, "开通VIP会员使用批量联系", "错误————%s" % goal)

        self.logout()
        self.account.release_account(account)

    @getimage
    def test_CGS_ZSSJGY_0007(self):
        '''搜索结果页-批量联系-VIP'''
        log.info(self.test_CGS_ZSSJGY_0007.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login("11099990154", "ef08beca")
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        searchKey = '北京阿里巴巴技术有限公司'
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(searchKey)
        text = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_search_title').text
        search_num = re.sub("\D", "", text)
        self.new_find_element(By.ID, self.ELEMENT["batch_contact"]).click()

        goal_01 = '批量联系页面带入搜索列表数量'
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_search_title').text
        self.assertEqual(text_01,text,msg='错误——%s'%goal_01)

        goal_02 = "批量联系页面输入框带入搜索关键词"
        text_02 = self.new_find_element(By.ID, self.ELEMENT["contact_search_box"]).text
        self.assertEqual(text_02,searchKey, "错误————%s" % goal_02)

        goal_03 = "批量联系页面-列表默认展示20条数据"
        self.new_find_element(By.ID, self.ELEMENT["contact_check_all"]).click()
        text_03 = self.new_find_element(By.ID, self.ELEMENT["contact_check_count"]).text
        result = re.sub("\D", "", text_03)
        num = int(result)
        self.assertEqual(num, 20, "错误————%s" % goal_03)

        goal_04 = "批量联系选择页点击取消返回搜索结果页"
        self.new_find_element(By.ID, self.ELEMENT["contact_cancel"]).click()
        text_04 = self.new_find_element(By.ID, (self.ELEMENT["middle_search_box"])).text
        self.assertEqual(text_04,searchKey,"错误————%s" % goal_04)

        goal_05 = "批量联系选择页未选择公司时点击去联系：置灰不可点"
        self.new_find_element(By.ID, self.ELEMENT["batch_contact"]).click()
        result_07 = self.new_find_element(By.ID, self.ELEMENT["go_contact"]).is_enabled()
        self.assertFalse(result_07, "错误————%s" % goal_05)

        goal_06 = '批量联系选择页选择1家公司'
        self.new_find_elements(By.ID, self.ELEMENT["contact_select"])[0].click()
        text_06 = self.new_find_element(By.ID, self.ELEMENT["contact_check_count"]).text
        self.assertEqual(text_06, "1", "错误————%s" % goal_06)

        goal_07 = '批量联系选择页选择公司点击去联系进入批量联系页面'
        self.new_find_element(By.ID,self.ELEMENT['go_contact']).click()
        page_result = self.get_title_name()
        self.assertEqual(page_result, '批量联系', msg="错误——%s"%goal_07)

        goal_08 = ['顶部提示:今日剩余n封','3s后消失']
        result_08_01 = self.isElementExist(By.ID,self.ELEMENT['contactpage_limit'])
        self.assertTrue(result_08_01,msg='错误——%s'%goal_08[0])
        time.sleep(3)
        result_08_02 = self.isElementExist(By.ID,self.ELEMENT['contactpage_limit'])
        self.assertFalse(result_08_02,msg='错误——%s'%goal_08[1])

        goal_09 = '选择公司数量带入'
        text_09 = self.new_find_element(By.ID,self.ELEMENT['contactpage_title']).text
        num_09 = re.sub("\D","", text_09)
        self.assertEqual(num_09,text_06,msg='错误——%s'%goal_09)

        goal_10 = '日期格式YYYY.MM.DD'
        text_10 = self.new_find_element(By.ID,self.ELEMENT['contactpage_time']).text
        result_10 = self.is_valid_date(text_10)
        self.assertTrue(result_10,msg='错误——%s'%goal_10)

        goal_12 = "批量联系页面-用户信息-点击公司输入框:跳转到修改公司页面"
        self.new_find_element(By.ID, self.ELEMENT["contactpage_company"]).click()
        text_12 = self.new_find_element(By.ID, self.ELEMENT["app_title_name"]).text
        self.assertEqual(text_12, "修改公司", "错误————%s" % goal_12)

        goal_13 = "输入“北京金堤”点击一键清除icon:清空输入框内容"
        self.new_find_element(By.ID, self.ELEMENT["contactpage_change_search"]).send_keys("北京金堤")
        self.new_find_element(By.ID, self.ELEMENT["contactpage_suggest_clear"]).click()
        text_13 = self.new_find_element(By.ID, self.ELEMENT["contactpage_change_search"]).text
        self.assertEqual(text_13, "请输入公司名称", "错误————%s" % goal_13)

        goal_14 = "再次输入-北京金堤:下拉列表匹配公司，展示五条"
        self.new_find_element(By.ID, self.ELEMENT["contactpage_change_search"]).send_keys("北京金堤")
        result_list = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_com_name']")
        num_14 = len(result_list)
        self.assertEqual(num_14, 5, "错误————%s" % goal_14)

        goal_15 = ["选择-北京金堤科技有限公司进入批量联系页面", "带入北京金堤科技有限公司"]
        self.new_find_element(By.XPATH, self.ELEMENT["contactpage_company_first"]).click()
        text_1501 = self.new_find_element(By.ID, self.ELEMENT["app_title_name"]).text
        self.assertEqual(text_1501, "批量联系", "错误————%s" % goal_15[0])
        text_1502 = self.new_find_element(By.ID, self.ELEMENT["contactpage_company"]).text
        self.assertEqual(text_1502, "北京金堤科技有限公司", "错误————%s" % goal_15[1])

        goal_16 = "批量联系页面-用户信息-姓名能正确输入"
        self.new_find_element(By.ID, self.ELEMENT["contactpage_person"]).send_keys("测试")
        text_16 = self.new_find_element(By.ID, self.ELEMENT["contactpage_person"]).text
        self.assertEqual(text_16, "测试", "错误————%s" % goal_16)

        goal_17 = ["批量联系页面-洽谈合作默认选中", "title：我的合作意向是：", "描述内容文案：描述你的合作意向"]
        result_1701 = self.new_find_element(By.ID, self.ELEMENT["contactpage_iwanner_1"]).get_attribute("checked")
        self.assertEqual(result_1701, "true", "错误————%s" % goal_17[0])
        text_1702 = self.new_find_element(By.ID, self.ELEMENT["contactpage_intent_iwanner"]).text
        self.assertEqual(text_1702, "我的合作意向是：", "错误————%s" % goal_17[1])
        text_1703 = self.new_find_element(By.ID, self.ELEMENT["contactpage_teamwork_intent"]).text
        self.assertEqual(text_1703, "描述你的合作意向", "错误————%s" % goal_17[2])

        goal_18 = ["批量联系页面-选择商讨投资", "title：我的投资意向是：", "描述内容文案：描述你的投资意向"]
        self.new_find_element(By.ID, self.ELEMENT["contactpage_iwanner_2"]).click()
        result_1801 = self.new_find_element(By.ID, self.ELEMENT["contactpage_iwanner_2"]).get_attribute("checked")
        self.assertEqual(result_1801, "true", "错误————%s" % goal_18[0])
        text_1802 = self.new_find_element(By.ID, self.ELEMENT["contactpage_intent_iwanner"]).text
        self.assertEqual(text_1802, "我的投资意向是：", "错误————%s" % goal_18[1])
        text_1803 = self.new_find_element(By.ID, self.ELEMENT["contactpage_teamwork_intent"]).text
        self.assertEqual(text_1803, "描述你的投资意向", "错误————%s" % goal_18[2])

        goal_19 = "批量联系页面-联系方式默认为登录账号"
        text_19 = self.new_find_element(By.ID, self.ELEMENT["contactpage_person_number"]).text
        self.assertEqual(text_19,"11099990154", "错误————%s" % goal_19)

    @getimage
    def test_CGS_ZSSJGY_0008(self):
        '''搜索结果页-批量联系增值'''
        log.info(self.test_CGS_ZSSJGY_0008.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login("11099990154", "ef08beca")
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        searchKey = '北京阿里巴巴技术有限公司'
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(searchKey)
        # text = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_search_title').text
        # search_num = re.sub("\D", "", text)
        self.new_find_element(By.ID, self.ELEMENT["batch_contact"]).click()
        #划到页面最底部
        count = 0
        while True:
            if count <= 20:
                self.swipeUp(x1=0.5, y1=0.90, y2=0.10, t=500)
                count += 1
            else:
                break

        self.new_find_element(By.ID,self.ELEMENT['contact_check_all']).click()#全部选中
        count = int(self.new_find_element(By.ID, self.ELEMENT["contact_check_count"]).text)#获取已选择数量
        log.info(count)
        if count > 100:
            goal_01 = '选择数量大于100时弹出选择增值弹框'
            self.new_find_element(By.ID,self.ELEMENT['go_contact']).click()
            result_01 = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/lLayout_bg')
            self.assertTrue(result_01,msg='错误——%s'%goal_01)

            goal_02 = '展示剩余n家文案'
            word = '正在使用VIP功能，今日剩余100家'
            text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_common_count').text
            self.assertEqual(word,text_02,msg='错误——%s'%goal_02)

            goal_03 = ['默认选中VIP批量联系','展示可联系n家企业']
            result_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/rl_common_type').is_selected()
            self.assertTrue(result_03,msg='错误——%s'%goal_03[0])
            text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_count').text
            self.assertEqual(text_03,'可联系前100家企业',msg='错误——%s'%goal_03[1])

            goal_04 = ['超出100家公司一条¥0.1','展示可联系n家企业']
            text_04 = float(self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_price').text)
            price = (count-100)*0.1
            self.assertEqual(text_04,price,msg='错误——%s'%goal_04[0])
            text_0401 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_export_count').text
            num = int(re.sub("\D", "",text_0401))
            self.assertEqual(num,count,msg='错误——%s'%goal_04[1])

            goal_05 = '选择增值批量联系点击立即发送进入支付页'
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/rl_value_type').click()
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_pos').click()
            text_05 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_hint').text
            self.assertEqual(text_05,'批量与企业获取联系',msg='错误——%s'%goal_05)

            goal_06 = '增值批量联系支付页带入选择数量、价格'
            text_06 = int(self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_count').text)
            self.assertEqual(text_06,count,msg='带入数量有误')
            price_06 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_price').text
            price = '¥'+str(price)
            self.assertEqual(price,price_06,msg='价格有误')

            goal_07 = '选择VIP批量联系进入批量联系页面'
            self.page_back()
            self.new_find_element(By.ID, self.ELEMENT["batch_contact"]).click()
            self.new_find_element(By.ID, self.ELEMENT['contact_check_all']).click()
            self.new_find_element(By.ID,self.ELEMENT['go_contact']).click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_pos').click()
            page_result = self.get_title_name()
            self.assertEqual(page_result, '批量联系', msg="错误——%s" % goal_07)

        else:
            log.error('case数量小于100%d'%count)



if __name__ == "__main__":
    unittest.main()

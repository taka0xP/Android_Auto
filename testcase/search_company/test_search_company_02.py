from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger
import time
import unittest

log = Logger("查公司_02").getlog()


class Search_companyTest(MyTest, Operation):
    """查公司_02"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_company")

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(company)
        self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[index].click()
    def page_back(self):
        """页面返回"""
        self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_back').click()
    def go_address(self):
        '''进入查公司-搜索中间页-身边老板'''
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["address_book_entrance"]).click()
        result = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/btn_close_guide')
        if result == True:
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_close_guide').click()
        else:
            pass
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

    @getimage
    def test_CGS_SSZJY_0001(self):
        '''搜索中间页-身边老板'''
        log.info(self.test_CGS_SSZJY_0001.__doc__)
        #判断登录&取热搜老板列表
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        else:
            pass
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/home_tab2').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/txt_search_copy1').click()
        list = self.new_find_elements(By.ID, 'com.tianyancha.skyeye:id/tv_name')
        boss_01 = list[0].text
        boss_02 = list[1].text
        bossList = [boss_01, boss_02]
        log.info(bossList)
        self.new_find_element(By.ID, self.ELEMENT['middle_search_back']).click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/home_tab1').click()
        self.go_address()

        goal = '点击搜索中间页立即查看进入身边老板页'
        page_title = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        self.assertEqual(page_title,'身边老板',msg='错误————%s'%goal)

        result = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='没有发现通讯录中的老板']")
        if result == True:
            goal_01 = '手机通讯录中无老板展示推荐监控'
            result_01 = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/ll_boss_recommend_monitor')
            self.assertTrue(result_01,msg='错误———%s'%goal_01)

            goal_02 = '推荐监控老板为热门搜索老板'
            result_02_01 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name' and @text='%s']"%boss_01)
            result_02_02 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_name' and @text='%s']"%boss_02)
            if result_02_01 == True and result_02_02 == True:
                result_02 = True
            else:
                result_02 = False
            self.assertTrue(result_02,msg='错误——%s'%goal_02)

            goal_03 = '未登录点击推荐老板卡片老板跳转登陆页'
            result_03 = self.login_page_check(2,'//androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout')
            self.page_back()
            self.assertTrue(result_03,msg='错误——%s'%goal_03)

            goal_04 = '未登录点击一键监控跳转登陆页'
            result_04 = self.login_page_check(1,'com.tianyancha.skyeye:id/tv_all_monitor')
            self.page_back()
            self.assertTrue(result_04,msg='错误——%s'%goal_04)

            goal_05 = '未登录点击卡片老板监控跳转登陆页'
            result_05 = self.login_page_check(2,"//*[@resource-id='com.tianyancha.skyeye:id/tv_monitoring']")
            self.page_back()
            self.assertTrue(result_05, msg='错误——%s'%goal_05)

            goal_06 = '已登录点击卡片老板监控toast监控成功/已取消监控'
            account = self.account.get_account()
            self.login(account,self.account.get_pwd())
            self.go_address()
            self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_monitoring']").click()
            toast = self.new_find_element(By.XPATH, '/hierarchy/android.widget.Toast').text
            judge = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/txt_title')
            if judge == True:
                self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_neg').click()
            if toast == '已取消监控' or toast == '监控成功':
                result_06 = True
            else:
                result_06 = False
            self.assertTrue(result_06,msg='错误——%s,账号为——%s'%(goal_06,account))

            goal_07 = '已登录点击一键监控按钮变成换一批'
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_all_monitor').click()
            judge = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/txt_title')
            if judge == True:
                self.new_find_element(By.ID,'com.tianyancha.skyeye:id/btn_neg').click()
            result_07 = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='换一批']")
            self.assertTrue(result_07,msg='错误——%s,账号为——%s'%(goal_07,account))

            goal_08 = '点击卡片老板已监控按钮换一批同步为一键监控'
            self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_monitoring']").click()
            result_08 = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/tv_all_monitor')
            self.assertTrue(result_08,msg='错误——%s,账号为——%s'%(goal_08,account))

            goal_09 = '点击换一批toast暂无更新'
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_all_monitor').click()
            self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='换一批']").click()
            toast_09 = self.new_find_element(By.XPATH,'/hierarchy/android.widget.Toast').text
            self.assertEqual(toast_09,'暂无更新',msg='错误——%s,账号为——%s'%(goal_09,account))

            goal_10 = '再次进入时页面时无推荐监控老板不展示推荐监控'
            self.page_back()
            self.new_find_element(By.XPATH, self.ELEMENT["address_book_entrance"]).click()
            result_10 = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/ll_boss_recommend_monitor')
            self.assertFalse(result_10,msg='错误——%s,账号为——%s'%(goal_10,account))

            #删除已监控数据
            self.page_back()
            self.new_find_element(By.ID,self.ELEMENT['top_right_corner']).click()#返回首页
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tab_iv_5').click()#我的
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/rl_my_monitoring').click()#我的监控
            self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_tab_title' and @text='监控列表']").click()#监控列表
            count = 1
            while True:
                if count <= 10:
                    self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_cancel_monitor']").click()
                    count += 1
                else:
                    log.error('删除监控数据错误，账号-%s'%account)
                    break
            self.logout()
            self.account.release_account(account)
        else:
            goal_01 = "手机通讯录中有老板查看通讯录列表页搜索框文案"
            text_01 = self.new_find_element(By.ID, self.ELEMENT["address_search_box"]).text
            self.assertEqual(text_01, "输入联系人姓名或手机号", "错误————%s" % goal_01)

            goal_02 = "手机通讯录无联系人变化，通讯录列表中点击更新能有提示"
            self.new_find_element(By.ID, self.ELEMENT["address_update"]).click()
            text_02 = self.new_find_element(By.XPATH, self.ELEMENT["address_widget_toast"]).text
            self.assertEqual(text_02, "没有发现新增", "错误————%s" % goal_02)

    @getimage
    def test_CGS_SSZJY_0002(self):
        '''搜索中间页-热门搜索模块'''
        log.info(self.test_CGS_SSZJY_0002.__doc__)
        goal = "点击热门搜索模块能进入对应公司详情页"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        result = self.isElementExist(By.ID, self.ELEMENT["hotwords_all"])
        if result == True:
            text_01 = self.new_find_elements(By.ID, self.ELEMENT["hotwords_first"])[0].text
            self.new_find_elements(By.ID, self.ELEMENT["hotwords_first"])[0].click()
            time.sleep(1)
            text_02 = self.new_find_element(By.ID, self.ELEMENT["companypage_name"]).text
            if text_01 in text_02:
                result = True
            else:
                result = False
            self.assertTrue(result, "错误————%s" % goal)
        else:
            log.error("未执行用例test_CGS_SSZJY_0002——无热门搜索模块")

    @getimage
    def test_CGS_SSZJY_0003(self):
        '''搜索中间页-最近搜索/浏览规则&交互'''
        log.info(self.test_CGS_SSZJY_0003.__doc__)
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        result = self.isElementExist(By.ID, self.ELEMENT["hotwords_all"])
        if result == True:
            goal_02 = "点击最近搜索的记录进入搜索结果页"
            self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], "腾讯科技", self.device)
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["search_history_result_first"]).click()
            text_02 = self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).text
            self.assertEqual(text_02, "腾讯科技", "错误————%s" % goal_02)

            goal_03 = "有最近搜索记录不展示热门搜索"
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            result_03 = self.isElementExist(By.ID, self.ELEMENT["hotwords_all"])
            self.assertFalse(result_03, "错误————%s" % goal_03)

            goal_04 = "有最近浏览记录不展示热门搜索"
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
            self.new_find_element(By.XPATH, self.ELEMENT["search_result_first"]).click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            result_04 = self.isElementExist(By.ID, self.ELEMENT["hotwords_all"])
            self.assertFalse(result_04, "错误————%s" % goal_04)

            goal_05 = "点击最近搜索的一键清除icon弹出确认弹框"
            self.new_find_element(By.ID, self.ELEMENT["search_history_delete"]).click()
            result_05 = self.isElementExist(By.ID, self.ELEMENT["pop_up"])
            self.assertTrue(result_05, "错误————%s" % goal_05)

            goal_06 = "最近搜索-确认弹框中选择取消能返回搜索中间页"
            self.new_find_element(By.ID, self.ELEMENT["pop_up_cancel"]).click()
            result_06 = self.isElementExist(By.ID, self.ELEMENT["address_book_all"])
            self.assertTrue(result_06, "错误————%s" % goal_06)

            goal_07 = "最近搜索-确认弹框中选择确认能清空最近搜索记录"
            self.new_find_element(By.ID, self.ELEMENT["search_history_delete"]).click()
            self.new_find_element(By.ID, self.ELEMENT["pop_up_sure"]).click()
            result_07 = self.isElementExist(By.ID, self.ELEMENT["search_history_all"])
            self.assertFalse(result_07, "错误————%s" % goal_07)

            goal_08 = "点击最近浏览的一键清除icon弹出确认弹框"
            self.new_find_element(By.ID, self.ELEMENT["read_history_delete"]).click()
            result_08 = self.isElementExist(By.ID, self.ELEMENT["pop_up"])
            self.assertTrue(result_08, "错误————%s" % goal_08)

            goal_09 = "最近浏览-确认弹框中选择取消能返回搜索中间页"
            self.new_find_element(By.ID, self.ELEMENT["pop_up_cancel"]).click()
            result_09 = self.isElementExist(By.ID, self.ELEMENT["address_book_all"])
            self.assertTrue(result_09, "错误————%s" % goal_09)

            goal_10 = "最近浏览-确认弹框中选择确认能清空最近浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["read_history_delete"]).click()
            self.new_find_element(By.ID, self.ELEMENT["pop_up_sure"]).click()
            result_10 = self.isElementExist(By.ID, self.ELEMENT["search_history_all"])
            self.assertFalse(result_10, "错误————%s" % goal_10)

            goal_11 = "删除最近搜索&最近浏览能展示热门搜索"
            result_11 = self.isElementExist(By.ID, self.ELEMENT["hotwords_all"])
            self.assertTrue(result_11, "错误————%s" % goal_11)

            goal_12 = "无最近搜索记录不展示最近搜索模块"
            result_12 = self.isElementExist(By.XPATH, self.ELEMENT["search_history_all"])
            self.assertFalse(result_12, "错误————%s" % goal_12)

            goal_13 = "无最近浏览记录不展示最近浏览模块"
            result_13 = self.isElementExist(By.XPATH, self.ELEMENT["search_history_all"])
            self.assertFalse(result_13, "错误————%s" % goal_13)
        else:
            log.error("未执行用例test_CGS_SSZJY_0003——无热门搜索模块")

    @getimage
    def test_CGS_SSZJY_0004(self):
        '''搜索中间页-最近搜索最多展示10条'''
        log.info(self.test_CGS_SSZJY_0004.__doc__)
        goal = "搜索11条关键词查看最近搜索记录"
        company_list = ["百度1","百度2","百度3","百度4","百度5","百度6","百度7","百度8","百度9","百度10","百度11"]
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        a = self.new_find_element(By.ID, self.ELEMENT["Recent_search_clean"])
        if a == None:
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).click()
            for i in range(len(company_list)):
                self.adb_send_input(By.ID,self.ELEMENT["middle_search_box"],company_list[i],self.device)
                self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
                i += 1
        else:
            self.new_find_element(By.ID, self.ELEMENT["Recent_search_clean"]).click()
            self.new_find_element(By.ID, self.ELEMENT["pop_up_sure"]).click()
            for i in range(len(company_list)):
                self.adb_send_input(By.ID,self.ELEMENT["middle_search_box"],company_list[i],self.device)
                self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
                i += 1
        value1 = self.new_find_element(By.XPATH, self.ELEMENT["Recent_search1"]).text
        value2 = self.new_find_element(By.XPATH, self.ELEMENT["Recent_search10"]).text
        self.assertEqual("百度11", value1, "错误---%s" % goal)
        self.assertEqual("百度2", value2, "错误---%s" % goal)

    @getimage
    def test_CGS_SSZJY_0005(self):
        '''搜索中间页-最近搜索特殊字符'''
        log.info(self.test_CGS_SSZJY_0005.__doc__)
        goal = "搜索特殊字符查看最近搜索记录"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], "aabb", self.device)
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        value = self.new_find_element(By.XPATH, self.ELEMENT["Recent_search1"]).text
        self.assertEqual("aabb", value, "错误---%s" % goal)
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], "*@", self.device)
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        value = self.new_find_element(By.XPATH, self.ELEMENT["Recent_search1"]).text
        self.assertEqual("*@", value, "错误---%s" % goal)
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], "", self.device)
        value = self.new_find_element(By.XPATH, self.ELEMENT["Recent_search1"]).text
        self.assertEqual("*@", value, "错误---%s" % goal)
        toast_loc = '//*[contains(@text,"输入两个关键字")]'
        try:
            value = self.new_find_element(By.XPATH, toast_loc).text
            log.info('toast提示"%s"' % value)
            self.assertEqual("至少输入两个关键字", value, "错误————%s" % goal)
        except:
            log.error("没有获取到toast信息")

    @getimage
    def test_CGS_SSZJY_0006(self):
        '''搜索中间页-最近搜索相同关键词'''
        log.info(self.test_CGS_SSZJY_0006.__doc__)
        goal = "再次搜索相同关键词时查看最近搜索记录"
        companyname1 = "金堤"
        companyname2 = "网易"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], companyname1, self.device)
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], companyname2, self.device)
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], companyname1, self.device)
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        num = len(self.new_find_elements(By.XPATH, self.ELEMENT["Recent_search_result"]))
        value = self.new_find_elements(By.XPATH, self.ELEMENT["Recent_search_result"])
        for ele in value:
            log.info(ele.text)
        log.info("所有的搜索记录%s条" % num)
        value1 = self.new_find_element(By.XPATH, self.ELEMENT["Recent_search1"]).text
        self.assertEqual(companyname1, value1, "错误---%s" % goal)
        self.new_find_element(By.ID, self.ELEMENT["search_history_delete"]).click()
        self.new_find_element(By.ID, self.ELEMENT["pop_up_sure"]).click()

    @getimage
    def test_CGS_SSZJY_0007(self):
        '''搜索中间页-最近浏览展示'''
        log.info(self.test_CGS_SSZJY_0007.__doc__)
        goal_01 = ["最近浏览-公司logo", "最近浏览-公司名称", "最近浏览-浏览标签"]
        status = self.is_login()
        if status == True:
            self.logout()
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        result = self.isElementExist(By.ID, self.ELEMENT["read_history_all"])
        if result == False:
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
            self.new_find_element(By.XPATH, self.ELEMENT["search_result_first"]).click()
            time.sleep(2)
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            test_01 = self.isElementExist(By.ID, self.ELEMENT["read_history_logo"])
            self.assertTrue(test_01, "错误————%s" % goal_01[0])
            submit_01 = self.new_find_element(By.ID, self.ELEMENT["read_history_name"])
            test_02 = submit_01.text
            submit_02 = self.new_find_element(By.ID, self.ELEMENT["read_history_time"])
            test_03 = submit_02.text
            self.assertEqual(test_02, "北京百度网讯科技有限公司", "错误————%s" % goal_01[1])
            self.assertEqual(test_03, "今天浏览过", "错误————%s" % goal_01[2])

            goal_02 = ["最近浏览-老板logo", "最近浏览-老板名称", "最近浏览-浏览标签"]
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("李彦宏")
            self.new_find_elements(By.ID, self.ELEMENT["same_boss_first"])[0].click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            test_01 = self.isElementExist(By.ID, self.ELEMENT["read_history_logo"])
            self.assertTrue(test_01, "错误————%s" % goal_02[0])
            submit_01 = self.new_find_element(By.ID, self.ELEMENT["read_history_name"])
            test_02 = submit_01.text
            submit_02 = self.new_find_element(By.ID, self.ELEMENT["read_history_time"])
            test_03 = submit_02.text
            self.assertEqual(test_02, "李彦宏", "错误————%s" % goal_02[1])
            self.assertEqual(test_03, "今天浏览过", "错误————%s" % goal_02[2])

            goal_03 = "浏览相同公司只展示最新的浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
            self.new_find_element(By.XPATH, self.ELEMENT["search_result_first"]).click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            submit_01 = self.new_find_element(By.ID, self.ELEMENT["read_history_name"])
            test_01 = submit_01.text
            submit_02 = self.new_find_elements(By.ID, self.ELEMENT["read_history_name"])[1]
            test_02 = submit_02.text
            self.assertEqual(test_01, "北京百度网讯科技有限公司", "错误————%s" % goal_03)
            self.assertEqual(test_02, "李彦宏", "错误————%s" % goal_03)

            goal_04 = "点击浏览记录进入对应的企业详情页"
            self.new_find_element(By.ID, self.ELEMENT["read_history_name"]).click()
            submit = self.new_find_element(By.ID, self.ELEMENT["company_official_information"])
            test = submit.text
            self.assertEqual(test, "官方信息", "错误————%s" % goal_04)

            goal_05 = "未登录点击人员浏览记录跳转登陆页"
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_elements(By.ID, self.ELEMENT["read_history_name"])[1].click()
            submit = self.new_find_element(By.ID, self.ELEMENT["login_title"])
            test = submit.text
            self.assertEqual(test, "短信验证码登录", "错误————%s" % goal_05)

            goal_07 = "最近浏览单条点击删除能删除此浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["read_history_close"]).click()
            time.sleep(1)
            self.new_find_element(By.ID, self.ELEMENT["read_history_close"]).click()
            test = self.isElementExist(By.ID, self.ELEMENT["read_history_all"])
            self.assertFalse(test, "错误————%s" % goal_07)

        else:
            self.new_find_element(By.ID, self.ELEMENT["read_history_delete"]).click()
            self.new_find_element(By.ID, self.ELEMENT["pop_up_sure"]).click()
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
            self.new_find_element(By.XPATH, self.ELEMENT["search_result_first"]).click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            test_01 = self.isElementExist(By.ID, self.ELEMENT["read_history_logo"])
            self.assertTrue(test_01, "错误————%s" % goal_01[0])
            submit_01 = self.new_find_element(By.ID, self.ELEMENT["read_history_name"])
            test_02 = submit_01.text
            submit_02 = self.new_find_element(By.ID, self.ELEMENT["read_history_time"])
            test_03 = submit_02.text
            self.assertEqual(test_02, "北京百度网讯科技有限公司", "错误————%s" % goal_01[1])
            self.assertEqual(test_03, "今天浏览过", "错误————%s" % goal_01[2])

            goal_02 = ["最近浏览-老板logo", "最近浏览-老板名称", "最近浏览-浏览标签"]
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("李彦宏")
            self.new_find_elements(By.ID, self.ELEMENT["same_boss_first"])[0].click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            test_01 = self.isElementExist(By.ID, self.ELEMENT["read_history_logo"])
            self.assertTrue(test_01, "错误————%s" % goal_02[0])
            submit_01 = self.new_find_element(By.ID, self.ELEMENT["read_history_name"])
            test_02 = submit_01.text
            submit_02 = self.new_find_element(By.ID, self.ELEMENT["read_history_time"])
            test_03 = submit_02.text
            self.assertEqual(test_02, "李彦宏", "错误————%s" % goal_02[1])
            self.assertEqual(test_03, "今天浏览过", "错误————%s" % goal_02[2])

            goal_03 = "浏览相同公司只展示最新的浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
            self.new_find_element(By.XPATH, self.ELEMENT["search_result_first"]).click()
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            submit_01 = self.new_find_element(By.ID, self.ELEMENT["read_history_name"])
            test_01 = submit_01.text
            submit_02 = self.new_find_elements(By.ID, self.ELEMENT["read_history_name"])[1]
            test_02 = submit_02.text
            self.assertEqual(test_01, "北京百度网讯科技有限公司", "错误————%s" % goal_03)
            self.assertEqual(test_02, "李彦宏", "错误————%s" % goal_03)

            goal_04 = "点击浏览记录进入对应的企业详情页"
            self.new_find_element(By.ID, self.ELEMENT["read_history_name"]).click()
            submit = self.new_find_element(By.ID, self.ELEMENT["company_official_information"])
            test = submit.text
            self.assertEqual(test, "官方信息", "错误————%s" % goal_04)

            goal_05 = "未登录点击人员浏览记录跳转登陆页"
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_elements(By.ID, self.ELEMENT["read_history_name"])[1].click()
            submit = self.new_find_element(By.ID, self.ELEMENT["login_title"])
            test = submit.text
            self.assertEqual(test, "短信验证码登录", "错误————%s" % goal_05)

            goal_07 = "最近浏览单条点击删除能删除此浏览记录"
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["read_history_close"]).click()
            time.sleep(1)
            self.new_find_element(By.ID, self.ELEMENT["read_history_close"]).click()
            test = self.isElementExist(By.ID, self.ELEMENT["read_history_all"])
            self.assertFalse(test, "错误————%s" % goal_07)

    @getimage
    def test_CGS_SSZJY_0008(self):
        '''搜索中间页-最近浏览展示10条'''
        log.info(self.test_CGS_SSZJY_0006.__doc__)
        goal = "进入十一家公司详情页后查看最近浏览中倒序展示10条浏览记录"
        company_list = ["百度","京东","网易","爱奇艺","阿里巴巴","腾讯","拼多多","苏宁","天眼查","万达","华为"]
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        for i in range(len(company_list)):
            self.search_result(company_list[i], 0)
            self.new_find_element(By.ID, self.ELEMENT["app_title_back"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
            i += 1
        test_01 = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_name']")[8].text
        test_02 = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_name']")[0].text
        self.assertEqual(test_01, "网易（杭州）网络有限公司", "错误————%s" % goal)
        self.assertEqual(test_02, "华为技术有限公司", "错误————%s" % goal)



if __name__ == "__main__":
    unittest.main()

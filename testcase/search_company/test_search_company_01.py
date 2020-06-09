from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import time
import unittest
import re

log = Logger("查公司_01").getlog()


class Search_companyTest(MyTest, Operation):
    """查公司_01"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_company")

    def check_result(self, keyword, value):
        """获取关键词搜索结果列表第一家公司名称"""
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys(keyword)
        if value == 1:
            text = self.new_find_element(By.XPATH, self.ELEMENT["search_result_first"]).text
            return text
        elif value == 0:
            text = self.new_find_element(By.ID, self.ELEMENT["search_result"]).text
            return text
    def search_clear(self):
        self.new_find_element(By.ID,self.ELEMENT['search_clean']).click()

    @getimage
    def test_CGS_SSSY_0001(self):
        '''查公司-首页交互'''
        log.info(self.test_CGS_SSSY_0001.__doc__)

        goal_01 = "首页-输入框文案"
        text_01 = self.new_find_element(By.ID, self.ELEMENT["search_box"]).text
        self.assertEqual(text_01, "输入公司名称、老板姓名、品牌名称等", "错误————%s" % goal_01)

        goal_02 = "首页-点击搜索框能跳转至搜索中间页"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        result_02 = self.new_find_element(By.ID, self.ELEMENT["address_book_all"])
        self.assertTrue(result_02, "错误————%s" % goal_02)

        goal_03 = "搜索中间页-输入框文案"
        text_03 = self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).text
        self.assertEqual(text_03, "输入公司名称、老板姓名、品牌名称等", "错误————%s" % goal_03)

    @getimage
    def test_CGS_SSZJY_0002(self):
        '''查公司-搜索中间页支持搜索范围-公司全称'''
        log.info(self.test_CGS_SSZJY_0002.__doc__)
        goal = "输入公司全称能搜索到公司"
        result = self.check_result("北京金堤科技有限公司", 1)
        self.assertEqual(result, "北京金堤科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0003(self):
        '''查公司-搜索中间页支持搜索范围-统一信用代码'''
        log.info(self.test_CGS_SSZJY_0003.__doc__)
        goal = "输入统一信用代码能搜索到公司"
        result = self.check_result("9111010831813798XE", 1)
        self.assertEqual(result, "北京金堤科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0004(self):
        '''查公司-搜索中间页支持搜索范围-老板名称'''
        log.info(self.test_CGS_SSZJY_0004.__doc__)
        goal = "输入老板名称能搜索到公司"
        result = self.check_result("柳超", 1)
        self.assertEqual(result, "北京金堤科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0005(self):
        '''查公司-搜索中间页支持搜索范围-品牌/机构'''
        log.info(self.test_CGS_SSZJY_0005.__doc__)
        goal_01 = "输入品牌名称能搜索到项目品牌"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("天眼查")
        result_01 = self.isElementExist(By.ID,"com.tianyancha.skyeye:id/tv_title_trademark")
        self.assertTrue(result_01,"错误————%s" % goal_01)

        goal_02 = "输入投资机构名称能搜索到投资机构"
        self.search_clear()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("浦信资本")
        result_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_title_trademark")
        self.assertTrue(result_02, "错误————%s" % goal_02)

    @getimage
    def test_CGS_SSZJY_0006(self):
        '''查公司-搜索中间页支持搜索范围-关键字'''
        log.info(self.test_CGS_SSZJY_0006.__doc__)
        goal = "输入关键字能搜索到公司"
        result = self.check_result("百度", 1)
        self.assertEqual(result, "北京百度网讯科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0007(self):
        '''查公司-搜索中间页支持搜索范围-手机号'''
        log.info(self.test_CGS_SSZJY_0007.__doc__)
        goal = "输入手机号能搜索到公司"
        result = self.check_result("18401651734", 0)
        self.assertEqual(result, "贝壳找房（北京）科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0008(self):
        '''查公司-搜索中间页支持搜索范围-座机号'''
        log.info(self.test_CGS_SSZJY_0008.__doc__)
        goal = "输入座机号能搜索到公司"
        result = self.check_result("010-59328108", 0)
        self.assertEqual(result, "北京链家旅居科技服务有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0009(self):
        '''查公司-搜索中间页支持搜索范围-邮箱'''
        log.info(self.test_CGS_SSZJY_0009.__doc__)
        goal = "输入邮箱能搜索到公司"
        result = self.check_result("dufei@ke.com", 0)
        self.assertEqual(result, "北京高策房地产经纪有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0010(self):
        '''查公司-搜索中间页支持搜索范围-地址'''
        log.info(self.test_CGS_SSZJY_0010.__doc__)
        goal = "输入地址能搜索到公司"
        result = self.check_result("北京市海淀区西二旗西路2号院35号楼", 0)
        self.assertEqual(result, "贝壳找房（北京）科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0011(self):
        '''查公司-搜索中间页支持搜索范围-曾用名'''
        log.info(self.test_CGS_SSZJY_0010.__doc__)
        goal = "输入曾用名能搜索到公司"
        result = self.check_result("链家网（北京）科技有限公司", 0)
        self.assertEqual(result, "贝壳找房（北京）科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0012(self):
        '''查公司-搜索中间页支持搜索范围-英文名'''
        log.info(self.test_CGS_SSZJY_0012.__doc__)
        goal = "输入英文名能搜索到公司"
        result = self.check_result("Beijing Jindi Technology Co.,Ltd.", 0)
        self.assertEqual(result, "北京金堤科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0013(self):
        '''查公司-搜索中间页支持搜索范围-域名'''
        log.info(self.test_CGS_SSZJY_0013.__doc__)
        goal = "输入域名能搜索到公司"
        result = self.check_result("www.tianyancha.com", 0)
        self.assertEqual(result, "北京天眼查科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0014(self):
        '''查公司-搜索中间页支持搜索范围-经营范围'''
        log.info(self.test_CGS_SSZJY_0014.__doc__)
        goal = "输入经营范围能搜索到公司"
        result = self.check_result("二类6821医用电子仪器设备", 0)
        self.assertEqual(result, "江苏中惠医疗科技股份有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0015(self):
        '''查公司-搜索中间页支持搜索范围-商标'''
        log.info(self.test_CGS_SSZJY_0015.__doc__)
        goal = "输入商标名称能搜索到公司"
        result = self.check_result("天眼辣", 0)
        self.assertEqual(result, "北京金堤科技有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0016(self):
        '''查公司-搜索中间页支持搜索范围-专利'''
        log.info(self.test_CGS_SSZJY_0016.__doc__)
        goal = "输入专利名称能搜索到公司"
        result = self.check_result("软基处理中塑料排水板的锚固装置", 0)
        self.assertEqual(result, "中国二十冶集团有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0017(self):
        '''查公司-搜索中间页支持搜索范围-股东/董监高'''
        log.info(self.test_CGS_SSZJY_0017.__doc__)
        goal = "输入股东/高管名称能搜索到公司"
        result = self.check_result("朱永贵", 0)
        self.assertEqual(result, "中国二十冶集团有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0018(self):
        '''查公司-搜索中间页支持搜索范围-项目'''
        log.info(self.test_CGS_SSZJY_0018.__doc__)
        goal = "输入项目名称能搜索到公司"
        result = self.check_result("蘑菇街", 0)
        self.assertEqual(result, "杭州卷瓜网络有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0019(self):
        '''查公司-搜索中间页支持搜索范围-股票代码'''
        log.info(self.test_CGS_SSZJY_0019.__doc__)
        goal = "输入股票代码能搜索到公司"
        result = self.check_result("601800", 0)
        self.assertEqual(result, "中国交通建设股份有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0020(self):
        '''查公司-搜索中间页支持搜索范围-拼音'''
        log.info(self.test_CGS_SSZJY_0020.__doc__)
        goal = "输入拼音能搜索到公司"
        result = self.check_result("jiaotongjianshegufen", 0)
        self.assertEqual(result, "中国交通建设股份有限公司", "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0021(self):
        '''查公司-搜索中间页搜索限制'''
        log.info(self.test_CGS_SSZJY_0021.__doc__)

        goal = "不输入字符进行搜索"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], "", self.device)
        # 获取toast信息
        # toast:使用xpath表达式
        # 不能用等待元素可见。只能用等待元素存在
        toast_loc = '//*[contains(@text,"输入两个关键字")]'
        try:
            value = self.new_find_element(By.XPATH, toast_loc).text
            log.info('toast提示"%s"' % value)
            self.assertEqual("至少输入两个关键字", value,"错误————%s"%goal)
        except:
            log.error("没有获取到toast信息")

        goal_02 = "输入小于范围内的关键字进行搜索能正确提示"
        self.adb_send_input(By.ID, self.ELEMENT["middle_search_box"], "百", self.device)
        # 获取toast信息
        # toast:使用xpath表达式
        # 不能用等待元素可见。只能用等待元素存在
        toast_loc_02 = '//*[contains(@text,"输入两个关键字")]'
        try:
            value_02 = self.new_find_element(By.XPATH, toast_loc_02).text
            log.info('toast提示"%s"' % value_02)
            self.assertEqual("至少输入两个关键字", value_02,"错误————%s"%goal_02)
        except:
            log.error("没有获取到toast信息")

    @getimage
    def test_CGS_SSZJY_0022(self):
        '''查公司-搜索中间页搜索限制'''
        log.info(self.test_CGS_SSZJY_0022.__doc__)

        goal = "输入正常范围内的关键字进行搜索能正确搜索"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
        value1 = self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).text
        self.assertEqual("百度", value1, "错误————%s" % goal)
        self.assertTrue(self.Element("为你找到"), "错误————%s" % goal)
        self.assertTrue(self.isElementExist(By.ID, self.ELEMENT["export_data"]))

    @getimage
    def test_CGS_SSZJY_0023(self):
        '''查公司-搜索中间页一键清除'''
        log.info(self.test_CGS_SSZJY_0023.__doc__)

        goal_01 = "不输入字符时不展示一键清除按钮"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        result_01 = self.isElementExist(By.ID, self.ELEMENT["search_clean"])
        self.assertFalse(result_01, "错误————%s" % goal_01)

        goal_02 = "输入一个字符后能正常展示“一键清除”按钮"
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百")
        result_02 = self.isElementExist(By.ID, self.ELEMENT["search_clean"])
        self.assertTrue(result_02, "错误————%s" % goal_02)

        goal_03 = "输入关键字后点击一键清除能清空输入框内容"
        self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
        text_03 = self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).text
        self.assertEqual(text_03, "输入公司名称、老板姓名、品牌名称等", "错误————%s" % goal_03)

    @getimage
    def test_CGS_SSZJY_0024(self):
        '''查公司-搜索中间页-键盘语音输入'''
        log.info(self.test_CGS_SSZJY_0024.__doc__)

        goal = "启动键盘时能正确展示语音输入"
        self.adbSend_input(self.device)
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.assertTrue(self.isElementExist(By.ID, self.ELEMENT["recognizer_title"]))
        value = self.new_find_element(By.ID, self.ELEMENT["recognizer_title"]).text
        self.assertEqual("按一下，说出公司名称或老板姓名", value, "错误---%s" % goal)

    @getimage
    def test_CGS_SSZJY_0025(self):
        '''查公司-搜索中间页-取消/排序展示规则'''
        log.info(self.test_CGS_SSZJY_0025.__doc__)

        goal_01 = "不输入字符时输入框右侧能正确展示"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        text_01 = self.new_find_element(By.ID, self.ELEMENT["top_right_corner"]).text
        self.assertEqual(text_01, "取消", "错误————%s" % goal_01)

        goal_02 = "输入一个字符时输入框右侧能正确展示"
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百")
        text_02 = self.new_find_element(By.ID, self.ELEMENT["top_right_corner"]).text
        self.assertEqual(text_02, "取消", "错误————%s" % goal_02)

        goal_03 = ["输入两个字符时输入框右侧能正确展示为-排序", "输入两个字符时输入框左侧出现“返回”按钮"]
        self.search_clear()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
        text_03 = self.new_find_element(By.ID, self.ELEMENT["top_right_corner"]).text
        self.assertEqual(text_03, "排序", "错误————%s" % goal_03[0])
        result_03 = self.isElementExist(By.ID, self.ELEMENT["middle_search_back"])
        self.assertTrue(result_03, "错误————%s" % goal_03[1])

        goal_04 = "点击取消能返回首页"
        self.search_clear()
        self.new_find_element(By.ID, self.ELEMENT["top_right_corner"]).click()
        test = self.isElementExist(By.ID, self.ELEMENT["banner"])
        self.assertTrue(test, "错误————%s" % goal_04)

    @getimage
    def test_CGS_SSZJY_0026(self):
        '''查公司-搜索中间页-排序-默认排序'''
        log.info(self.test_CGS_SSZJY_0026.__doc__)

        goal_01 = "输入关键词点击排序时默认选项正确"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度")
        self.new_find_element(By.XPATH, self.ELEMENT["sorting"]).click()
        self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT["sorting"]))
        checkbox = self.new_find_element(By.XPATH, self.ELEMENT["default_sort_select"])
        value = checkbox.get_attribute("checked")
        value1 = checkbox.is_selected()
        self.assertTrue(self.Element("默认排序"), "错误---%s" % goal_01)

    @getimage
    def test_CGS_SSZJY_0027(self):
        '''查公司-搜索中间页-排序-按注册资本从高到低'''
        log.info(self.test_CGS_SSZJY_0027.__doc__)

        goal = "点击排序中-按注册资本从高到低"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("支付宝网络技术有限公司")
        self.new_find_element(By.ID, self.ELEMENT["top_right_corner"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["sort_registered_capital_high"]).click()
        text_01 = self.new_find_elements(By.ID, self.ELEMENT["search_result_registered_capital"])[0].text
        text_02 = self.new_find_elements(By.ID, self.ELEMENT["search_result_registered_capital"])[1].text
        num_01 = re.findall(r"\d+\.?\d*", text_01)[0]  # 提取数字
        num_02 = re.findall(r"\d+\.?\d*", text_02)[0]
        type_01 = float(num_01)
        type_02 = float(num_02)
        self.assertLess(type_02, type_01, "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0028(self):
        '''查公司-搜索中间页-排序-按注册资本从低到高'''
        log.info(self.test_CGS_SSZJY_0028.__doc__)

        goal = "点击排序中-按注册资本从低到高"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("天眼查科技有限公司")
        self.new_find_element(By.ID, self.ELEMENT["top_right_corner"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["sort_registered_capital_low"]).click()
        text_01 = self.new_find_elements(By.ID, self.ELEMENT["search_result_registered_capital"])[0].text
        text_02 = self.new_find_elements(By.ID, self.ELEMENT["search_result_registered_capital"])[1].text
        num_01 = re.findall(r"\d+\.?\d*", text_01)[0]
        num_02 = re.findall(r"\d+\.?\d*", text_02)[0]
        type_01 = float(num_01)
        type_02 = float(num_02)
        self.assertLess(type_01, type_02, "错误————%s" % goal)

    @getimage
    def test_CGS_SSZJY_0029(self):
        '''查公司-搜索中间页-排序-按成立日期从早到晚/按成立日期从晚到早'''
        log.info(self.test_CGS_SSZJY_0029.__doc__)

        goal_01 = "输入关键词点击排序中-按成立日期从早到晚"
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["middle_search_box"]).send_keys("百度网讯")
        self.new_find_element(By.XPATH, self.ELEMENT["sorting"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["early_and_late"]).click()
        time.sleep(1)
        value1 = self.new_find_elements(By.ID, self.ELEMENT["setup_times"])[0].text
        value2 = self.new_find_elements(By.ID, self.ELEMENT["setup_times"])[1].text
        self.assertLessEqual(value1, value2, "错误---%s" % goal_01)

        goal_02 = "输入关键词点击排序中-按成立日期从晚到早"
        self.new_find_element(By.XPATH, self.ELEMENT["sorting"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["late_and_early"]).click()
        value1 = self.new_find_elements(By.ID, self.ELEMENT["setup_times"])[0].text
        value2 = self.new_find_elements(By.ID, self.ELEMENT["setup_times"])[1].text
        self.assertGreaterEqual(value1, value2, "错误---%s" % goal_02)

    @getimage
    def test_CGS_ZSSSY_0030(self):
        '''查公司-搜索首页-扫一扫'''
        log.info(self.test_CGS_ZSSSY_0030.__doc__)

        goal_01 = "未登录点击首页搜索框扫一扫弹出登陆页面"
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        else:
            pass
        self.new_find_element(By.ID, self.ELEMENT["scan"]).click()
        text = self.new_find_element(By.ID, self.ELEMENT["login_title"]).text
        self.assertEqual(text, "短信验证码登录", "错误————%s" % goal_01)

        goal_02 = "已登陆点击首页搜索框扫一扫"
        account = self.account.get_account()
        self.login(account,self.account.get_pwd())
        text_02 = self.new_find_element(By.ID, self.ELEMENT["sweep_qrcode"]).text
        self.assertEqual(text_02, "扫码", "错误————%s" % goal_02)
        self.account.release_account(account)


if __name__ == "__main__":
    unittest.main()

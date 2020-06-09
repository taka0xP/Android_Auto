from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import re
import time

log = Logger("公司详情页-自主信息·求助问答").getlog()


class Company_own_information_help(MyTest, Operation):
    """公司详情页-自主信息·问答"""

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/txt_search_copy1"
        ).click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/search_input_et"
        ).send_keys(company)
        self.new_find_elements(
            By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']"
        )[index].click()

    @getimage
    def test_GSXQY_ZZXX_0001(self):
        """自主信息·求助问答1"""
        log.info(self.test_GSXQY_ZZXX_0001.__doc__)

        goal_01 = "本公司提问没回答时，展示「向你求助的问题」"
        log.info(goal_01)
        company_name = "河南科达工程管理有限公司"
        self.search_result(company_name, 0)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/radio_user_evaluate").click()
        count = 0
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_block_title' and @text = '向你求助的问题 2']"):
                if count <= 5:
                    self.swipeUp(x1=0.5, y1=0.70, y2=0.30, t=500)
                    count += 1
                else:
                    log.error("错误————%s" % goal_01)
                    break
            else:
                break
        self.swipeUp(x1=0.5, y1=0.80, y2=0.20, t=500)

        goal_02 = "「向你求助的问题」模块处有提问数量"
        log.info(goal_02)
        text_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_block_title").text
        str_02 = re.sub("\D", "", text_02)
        self.assertEqual(str_02, "2", msg="错误————%s" % goal_02)

        goal_03 = "「向你求助的问题」模块处有「查看全部」入口"
        log.info(goal_03)
        result_03 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_jump_more")
        self.assertTrue(result_03, msg="错误————%s" % goal_03)

        goal_04 = "点击「查看全部」进入「向你求助的问题」页面"
        log.info(goal_04)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_jump_more").click()
        result_04 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text = '向你求助的问题']")
        self.assertTrue(result_04, msg="错误————%s" % goal_04)

        goal_05 = ["「向你求助的问题」页面提问模块包含公司名称", "问题数量", "问题", "用户", "用户地区"]
        log.info(goal_05)
        text_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_name").text
        self.assertEqual(text_05, company_name, msg="错误————%s" % goal_05[0])
        result_05_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_question_count")
        self.assertTrue(result_05_01, msg="错误————%s" % goal_05[1])
        result_05_02 = self.isElementExist(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_question']")
        self.assertTrue(result_05_02, msg="错误————%s" % goal_05[2])
        result_05_03 = self.isElementExist(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_question_user']")
        self.assertTrue(result_05_03, msg="错误————%s" % goal_05[3])
        result_05_04 = self.isElementExist(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_question_city']")
        self.assertTrue(result_05_04, msg="错误————%s" % goal_05[4])

        goal_06 = "「向你求助的问题」页面提问下展示「我来回答」按钮"
        log.info(goal_06)
        result_06 = self.isElementExist(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_answer']")
        self.assertTrue(result_06, msg="错误————%s" % goal_06)

        goal_07 = "点击问题进入「问答详情」页"
        log.info(goal_07)
        question_list = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_question']")
        question_text = question_list[0].text
        question_list[0].click()
        result_07 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text = '问答详情']")
        self.assertTrue(result_07, msg="错误————%s" % goal_07)

        goal_08 = ["「问答详情」页面包含问题", "问题描述", "公司名称", "暂无回答占位图", "我来回答按钮"]
        log.info(goal_08)
        result_08_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_answer_name")
        self.assertTrue(result_08_01,msg="错误————%s" % goal_08[0])
        result_08_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_describe")
        self.assertTrue(result_08_02, msg="错误————%s" % goal_08[1])
        text_08_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_answer_title").text
        self.assertEqual(text_08_03, company_name, msg="错误————%s" % goal_08[2])
        result_08_04 = self.isElementExist(By.XPATH, "//*[@class='android.widget.TextView' and @text = '暂无回答']")
        self.assertTrue(result_08_04, msg="错误————%s" % goal_08[3])
        result_08_05 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_send")
        self.assertTrue(result_08_05, msg="错误————%s" % goal_08[4])

        goal_09 = "「问答详情」页面点击返回返回到「向你求助的问题」页面"
        log.info(goal_09)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()
        result_09 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text = '向你求助的问题']")
        self.assertTrue(result_09, msg="错误————%s" % goal_09)

        goal_10 = "「向你求助的问题」页面点击「我来回答」进入「回答」页面"
        log.info(goal_10)
        self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_answer']").click()
        result_10 = self.isElementExist(By.XPATH, "//*[@class='android.widget.TextView' and @text = '回答']")
        self.assertTrue(result_10, msg="错误————%s" % goal_10)

        goal_11 = "「回答」页面问题与「向你求助的问题」页面问题一致"
        log.info(goal_11)
        text_11 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_title").text
        self.assertEqual(text_11, question_text, msg="错误————%s" % goal_11)

        goal_12 = "「回答」页面点击「❎」回到「向你求助的问题页面」"
        log.info(goal_12)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_back").click()
        result_12 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text = '向你求助的问题']")
        self.assertTrue(result_12, msg="错误————%s" % goal_12)

        goal_13 = "「向你求助的问题」页面标题数量与本页面提问数量一致"
        log.info(goal_13)
        question_count = len(question_list)
        title_text = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_question_count").text
        title_num = re.sub("\D", "", title_text)
        title_count = int(title_num)
        self.assertEqual(question_count, title_count, msg="错误————%s" % goal_13)

        goal_14 = ["「向你求助的问题」页面顶部为本公司名称", "点击公司名称返回「自主信息页」"]
        log.info(goal_14)
        text_14_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_name").text
        self.assertEqual(text_14_01, company_name, msg="错误————%s" % goal_14[0])
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_name").click()
        text_14_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_name").text
        self.assertEqual(text_14_02, company_name, msg="错误————%s" % goal_14[1])

        goal_15 = "「向你求助的问题」页面提问数量与自主信息页「向你求助的问题」模块处提问数量一致"
        log.info(goal_15)
        text_15 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_block_title").text
        title_num_15 = re.sub("\D", "", text_15)
        title_count_15 = int(title_num_15)
        self.assertEqual(title_count_15, question_count, msg="错误————%s" % goal_15)

        goal_16 = ["「自主信息」页面「向你求助的问题」模块包含：问题", "用户", "用户地区", "我来回答按钮"]
        log.info(goal_16)
        result_16_01 = self.new_find_elements(By.XPATH,"//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView[1]")
        self.assertTrue(result_16_01, msg="错误————%s" % goal_16[0])
        result_16_02 = self.new_find_elements(By.XPATH,"//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView[3]")
        self.assertTrue(result_16_02, msg="错误————%s" % goal_16[1])
        result_16_03 = self.new_find_element(By.XPATH,"//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView[4]")
        self.assertTrue(result_16_03, msg="错误————%s" % goal_16[2])
        result_16_04 = self.new_find_elements(By.XPATH,"//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView[2]")
        self.assertTrue(result_16_04, msg="错误————%s" % goal_16[3])

        goal_17 = "点击问题进入「问答详情」页"
        log.info(goal_17)
        self.new_find_element(By.XPATH,"//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView[1]").click()
        result_17 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text = '问答详情']")
        self.assertTrue(result_17, msg="错误————%s" % goal_17)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()

        goal_18 = "点击我要回答进入「回答」页面"
        log.info(goal_18)
        answer_button = self.new_find_elements(By.XPATH,"//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.TextView[2]")
        answer_button[0].click()
        result_18 = self.isElementExist(By.XPATH, "//*[@class='android.widget.TextView' and @text = '回答']")
        self.assertTrue(result_18, msg="错误————%s" % goal_18)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_back").click()

        goal_19 = "「自主信息」页面底部展示「推荐问题」banner"
        log.info(goal_19)
        result_19 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/ll_recommend_question")
        self.assertTrue(result_19, msg="错误————%s" % goal_19)

        goal_20 = "点击「去回答」进入「问答详情」页面"
        log.info(goal_20)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_to_answer").click()
        result_20 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text = '问答详情']")
        self.assertTrue(result_20, msg="错误————%s" % goal_20)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()

        goal_21 = "点击「❎」「推荐问题」banner消失"
        log.info(goal_21)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/ll_close_ask").click()
        result_21 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/ll_recommend_question")
        self.assertFalse(result_21, msg="错误————%s" % goal_21)

    @getimage
    def test_GSXQY_ZZXX_0002(self):
        """自主信息·求助问答2"""
        log.info(self.test_GSXQY_ZZXX_0002.__doc__)

        goal_01 = "「向你求助的问题」模块提问大于5个时滑动区域尾部有「查看全部」入口"
        log.info(goal_01)
        company_name = "上海钧正网络科技有限公司"
        self.search_result(company_name, 0)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/radio_user_evaluate").click()
        count = 0
        while True:
            if not self.new_find_element(
                By.XPATH,
                "//*[@resource-id='com.tianyancha.skyeye:id/tv_block_title' and @text = '向你求助的问题 7']"):
                if count <= 5:
                    self.swipeUp(x1=0.5, y1=0.70, y2=0.30, t=500)
                    count += 1
                else:
                    log.error("错误————%s" % goal_01)
                    break
            else:
                break
        self.swipeUp(x1=0.5, y1=0.80, y2=0.20, t=500)
        text_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_block_title").text
        title_num_01 = re.sub("\D", "", text_01)
        count_01 = int(title_num_01)
        if count_01 >= 5:
            for n in range(3):
                l = self.driver.get_window_size()
                x1 = l["width"] * 0.95
                y1 = l["height"] * 0.3
                x2 = l["width"] * 0.05
                time.sleep(0.5)
                try:
                    self.driver.swipe(x1, y1, x2, y1, 500)
                except:
                    pass
            test = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_more")
            self.assertTrue(test, "错误————%s" % goal_01)
        else:
            log.error("case向你求助的问题小于5条")

        goal_02 = "点击「查看全部」进入「向你求助的问题」页面"
        log.info(goal_02)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_more").click()
        result_02 = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text='向你求助的问题']")
        self.assertTrue(result_02, msg="错误————%s" % goal_02)

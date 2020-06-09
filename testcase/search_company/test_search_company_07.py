from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import time
import unittest

log = Logger("查公司_07").getlog()
class Search_companyTest(MyTest, Operation):
    '''查公司_07'''
    a = Read_Ex()
    ELEMENT = a.read_excel('Search_company')

    #过期vip：11099995060

    @getimage
    def test_CGS_ZSSJGY_0001(self):
        '''搜索结果页-过期用户搜索结果引导续费VIP'''
        log.info(self.test_CGS_ZSSJGY_0001.__doc__)

        goal = '过期vip搜索关键词查看匹配列表超过100家公司-遮罩引导续费VIP'
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login(11099995060,'ef08beca')
        time.sleep(1)
        self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
        self.new_find_element(By.ID, self.ELEMENT['middle_search_box']).send_keys('京东')
        count1 = 0
        while True:
            if not self.new_find_element(By.XPATH, "//*[@class='android.widget.TextView' and @text='成为VIP']"):
                if count1 <= 20:
                    self.swipeUp(x1=0.5, y1=0.85, y2=0.15, t=500)
                    count1 += 1
                else:
                    log.error('错误————%s' % goal)
                    break
            else:
                break
        self.logout()


if __name__ == '__main__':
    unittest.main()

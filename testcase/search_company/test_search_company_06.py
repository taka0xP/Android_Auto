from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import unittest

log = Logger("查公司_06").getlog()
class Search_companyTest(MyTest, Operation):
    '''查公司_06'''
    a = Read_Ex()
    ELEMENT = a.read_excel('Search_company')

    @getimage
    def test_CGS_ZSSJGY_0001(self):
        '''搜索结果页-未登录&非VIP搜索结果引导登录&VIP'''
        log.info(self.test_CGS_ZSSJGY_0001.__doc__)

        goal =['未登录搜索关键词查看匹配列表超过40家公司-遮罩引导登录','非vip搜索关键词查看匹配列表超过100家公司-遮罩引导VIP']
        self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
        self.new_find_element(By.ID, self.ELEMENT['middle_search_box']).send_keys('京东')
        count = 0
        while True:
            if not self.new_find_element(By.XPATH, "//*[@class='android.widget.TextView' and @text='立即登录']"):
                if count <= 10:
                    self.swipeUp(x1=0.5, y1=0.85, y2=0.15, t=500)
                    count += 1
                else:
                    log.error('错误————%s' % goal[0])
                    break
            else:
                break
        self.new_find_element(By.XPATH, "//*[@class='android.widget.TextView' and @text='立即登录']").click()
        account = self.account.get_account()
        self.login(account, self.account.get_pwd())
        count1 = 0
        while True:

            if not self.new_find_element(By.XPATH, "//*[@class='android.widget.TextView' and @text='成为VIP']"):
                if count1 <= 10:
                    self.swipeUp(x1=0.5, y1=0.85, y2=0.15, t=500)
                    count1 += 1
                else:
                    log.error('错误————%s' % goal[1])
                    break
            else:
                break

        self.logout()
        self.account.release_account(account)



if __name__ == '__main__':
    unittest.main()

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# 速卖通登入
class AliexpressLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = 'https://login.aliexpress.com/seller.htm?flag=1'

    def login(self):
        """
        模拟登录函数，包括自动填充用户名、密码、自动点击验证、最终自动登录
        :return:
        """
        browser.get(self.login_url)
        time.sleep(5)  # 缓冲
        try:
            ifm = browser.find_element_by_xpath("//*[@id=\"localstorage-proxy-ifr-alibabadotcom\"]")
            browser.switch_to.frame(ifm)
            input_name = browser.find_element_by_id('fm-login-id')
            input_pd = browser.find_element_by_id('fm-login-password')
            input_name.clear()
            input_name.send_keys(self.username)
            input_pd.clear()
            input_pd.send_keys(self.password)
            browser.find_element_by_id('fm-login-submit').click()
            time.sleep(5)
            # c = Code(browser)  # 调用验证码识别模块
            # c.main()
            print(browser.get_cookies())
            print('登录成功！')
            time.sleep(0.8)
            print(browser.current_url)
        except NoSuchElementException:
            # 重复尝试登入操作
            print('没有找到元素')
            self.login()

    def add_cookie(self):
        """
            添加相应的cookies 进行具体页面操作
        :return:
        """
        # browser.add_cookie({'name': '_jc_save_fromDate', 'value': self.date})
        # print('cookie添加完成！')
        pass

    def get_cookie(self):

        pass

    def main(self):
        self.login()


# fm-login-id
# fm-login-password
# login-submit click

if __name__ == '__main__':
    begin = time.time()
    # 隐藏浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # 2020.03.28更新
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    # Buy_Ticket类初始化参数，从左到右：出发站，终点站，出发日期，账号，密码，购票类型(默认购买成人票，若要购买学生票，
    # 添加乘客姓名时在后面加上(学生))，把要购买票的乘客姓名放在一个列表里
    b = AliexpressLogin('2048453046@qq.com', 'Bjb421361')
    b.main()
    end = time.time()
    print('总耗时：%d秒' % int(end - begin))
    # browser.close()

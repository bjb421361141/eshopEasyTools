# -*- coding: utf-8 -*-
# @Time: 2021/4/25 11:03
import time

from selenium import webdriver


class DefaultLogin(object):
    """
        默认登入方法
    """
    __slots__ = ("username", "password", "login_url", "browser", "cookies")

    def __init__(self, login_url, username, password):
        self.username = username
        self.password = password
        self.login_url = login_url  # 'https://login.1688.com/member/signin.htm'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # 2020.03.28更新
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.cookies = None

    def login(self):
        """
        模拟登录函数：
            1、自动填充用户名、密码
            2、自动点击验证、
            3、最终自动登录获取对应的cookies 并返回
        :return:
        """
        self.browser.get(self.login_url)
        time.sleep(5)  # 等待页面加载完成
        try:
            self.fill_userinfo(self.username, self.password)
            self.go_login()
            # 通过browser 判断是否登入成功
            self.break_validation()
            self.cookies = self.browser.get_cookies()
        except Exception as err:
            print('登入异常!', err)
            raise Exception(err)
        finally:
            self.browser.quit()

    def fill_userinfo(self, username, password):
        """
        根据不同访问的网站获取对应的控件进行填充用户信息数据
        :return:
        """
        pass

    def break_validation(self):
        """
        根据不同访问的网站做特殊的处理，这边进行登入？
        :return:
        """
        pass

    def go_login(self):
        """
        根据不同访问的网站做特殊的处理,触发相应按钮进行登入,并校验用户名密码信息
        :return:
        """
        pass

    def get_cookies(self):
        """
            返回登入后的cookies信息
        :return:
        """
        return self.cookies

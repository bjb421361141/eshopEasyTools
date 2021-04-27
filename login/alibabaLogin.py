# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from commUtil.propertiesUtil import Properties
from commUtil.rsacrypt import RsaCrypt
from login.defaultLogin import DefaultLogin


# 阿里巴巴登入
class AlibabaLogin(DefaultLogin):

    def __init__(self, username, password):
        p = Properties("../login/config.properties")
        properties_map = p.getproperties()
        rs_obj = RsaCrypt(properties_map.get("App").get("pubkey"), properties_map.get("App").get("prikey"))
        super(AlibabaLogin, self).__init__('https://login.1688.com/member/signin.htm', username,
                                           rs_obj.decrypt(password).decode())

    def fill_userinfo(self, username, password):
        """
            填充阿里巴巴登入的用户名密码信息
        :return:
        """
        ifm = self.browser.find_elements_by_tag_name("iframe")[0]
        self.browser.switch_to.frame(ifm)
        input_name = self.browser.find_element_by_id('fm-login-id')
        input_pd = self.browser.find_element_by_id('fm-login-password')
        input_name.clear()
        input_name.send_keys(self.username)
        input_pd.clear()
        input_pd.send_keys(self.password)

    def break_validation(self):
        """
            登入过程中出现的校验
        :return:
        """
        # 判断是否有特定标识的html块出现,并根据code 进行校验操作
        # c = Code(browser)  # 调用验证码识别模块
        # c.main
        pass

    def go_login(self):
        """
            点击提交按钮
        :return:
        """
        self.browser.find_element_by_css_selector('button.fm-submit').click()
        # 校验是否登入成功


if __name__ == '__main__':
    begin = time.time()
    # 隐藏浏览器
    b = AlibabaLogin('421361141@qq.com', 'bjb421361141')
    _cookies = b.login()
    end = time.time()
    print('总耗时：%d秒' % int(end - begin))
    # browser.close()

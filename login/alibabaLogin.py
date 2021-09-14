# -*- coding: utf-8 -*-

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from commUtil.propertiesUtil import Properties
from commUtil.rsacrypt import RsaCrypt
from login.defaultLogin import DefaultLogin


# 阿里巴巴登入
class AlibabaLogin(DefaultLogin):

    def __init__(self, username, password):
        p = Properties("../login/config.properties")
        properties_map = p.getproperties()
        rs_obj = RsaCrypt(properties_map.get("App").get("pubkey"), properties_map.get("App").get("prikey"))
        # https://login.1688.com/member/signin.htm
        super(AlibabaLogin, self).__init__('https://re.1688.com/?keywords={keywords}&cosite=baidujj_pz&location=re&trackid={trackid}&keywordid={keywordid}&format=normal', username,
                                           rs_obj.decrypt(password).decode())

    def fill_userinfo(self, username, password):
        """
            填充阿里巴巴登入的用户名密码信息
        :return:
        """
        self.browser.find_element_by_xpath("//*[@id='alibar']/div[1]/div[2]/ul/li[3]/a").click()
        element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
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
        time.sleep(5)  # 等待页面加载完成
        try:
            login_error = self.browser.find_element_by_xpath("//*[@id=\"login-error\"]/div")
            if login_error.text is not None:
                raise Exception(login_error.text)
        except Exception as e:
            print("没有发现错误提示模块信息")
        # 校验是否登入成功
        # login - error  id="nc_1__scale_text" 滑动  //*[@id="nocaptcha"]


if __name__ == '__main__':
    begin = time.time()
    # 隐藏浏览器
    b = AlibabaLogin('421361141@qq.com', 'bjb421361141')
    _cookies = b.login()
    end = time.time()
    print('总耗时：%d秒' % int(end - begin))
    # browser.close()

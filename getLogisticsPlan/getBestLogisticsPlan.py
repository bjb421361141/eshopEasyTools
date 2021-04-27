# -*- coding: utf-8 -*-

import requests
import json

# 根据克重 长宽高 和 国家生成最佳物流方案（调用速卖通物流查询接口）
# 将物流方案写入excel文件中
from getLogisticsPlan.MyExcelUtils import ExcelUtil

LOGIN_URL = r"https://login.aliexpress.com/?flag=1&return_url=http%3A%2F%2Filogistics.aliexpress.com%2Frecommendation_engine_internal.htm"
LOGISTICS_URL = r"https://ilogistics.aliexpress.com/recommendationJsonPublic.do"

# 商品信息
PAGE_INFO = {
    "orderAmount": "8",  # 订单金额
    "packageWeight": "0.02",  # 包裹重量
    "packageLength": "10",  # 包裹长度
    "packageWidth": "10",  # 包裹宽度
    "packageHeight": "3",  # 包裹高度
    "logistics-express-item": {
        # 经济
        "4PX新邮经济小包": "CAINIAO#SGP_OMP#SGP_OMP#ECONOMY",
        "AliExpress 无忧物流-简易": "CAINIAO#CAINIAO_ECONOMY#CAINIAO_ECONOMY#ECONOMY",
        "中国邮政平常小包+": "CAINIAO#YANWEN_JYT#YANWEN_JYT#ECONOMY",
        "德胜特货经济": "STANDARD#BSC_ECONOMY_SG#BSC_ECONOMY_SG#ECONOMY",
        "燕文特货经济": "STANDARD#YANWEN_ECONOMY_SG#YANWEN_ECONOMY_SG#ECONOMY",
        "菜鸟专线经济": "CAINIAO#CAINIAO_EXPEDITED_ECONOMY#CAINIAO_EXPEDITED_ECONOMY#ECONOMY",
        "菜鸟特货专线－简易": "CAINIAO#CAINIAO_ECONOMY_SG#CAINIAO_ECONOMY_SG#ECONOMY",
        "菜鸟特货专线－超级经济": "CAINIAO#CAINIAO_SUPER_ECONOMY_SG#CAINIAO_SUPER_ECONOMY_SG#ECONOMY",
        "菜鸟超级经济": "CAINIAO#CAINIAO_SUPER_ECONOMY#CAINIAO_SUPER_ECONOMY#ECONOMY",
        "菜鸟超级经济-燕文": "CAINIAO#YANWEN_ECONOMY#YANWEN_ECONOMY#ECONOMY",
        "菜鸟超级经济-顺友": "CAINIAO#SUNYOU_ECONOMY#SUNYOU_ECONOMY#ECONOMY",
        "菜鸟超级经济Global": "CAINIAO#AE_CN_SUPER_ECONOMY_G#AE_CN_SUPER_ECONOMY_G#ECONOMY",
        "通邮特货经济": "STANDARD#TOPYOU_ECONOMY_SG#TOPYOU_ECONOMY_SG#ECONOMY",
        "顺丰国际经济小包": "CAINIAO#SF_EPARCEL_OM#SF_EPARCEL_OM#ECONOMY",
        "顺友特货经济": "STANDARD#SUNYOU_ECONOMY_SG#SUNYOU_ECONOMY_SG#ECONOMY",
        "飞特特货经济": "STANDARD#FLYT_ECONOMY_SG#FLYT_ECONOMY_SG#ECONOMY",
        # 标准
        "139俄罗斯专线": "STANDARD#ECONOMIC139#ECONOMIC139#STANDARD",
        "AliExpress 无忧物流-标准": "CAINIAO#CAINIAO_STANDARD#CAINIAO_STANDARD#STANDARD",
        "CNE": "STANDARD#CNE#CNE#STANDARD",
        "DHL e-commerce": "STANDARD#DHLECOM#DHLECOM#STANDARD",
        "DPD": "STANDARD#DPD#DPD#STANDARD",
        "HUAPT": "STANDARD#HUPOST#HUPOST#STANDARD",
        "J-NET捷网": "STANDARD#CTR_LAND_PICKUP#CTR_LAND_PICKUP#STANDARD",
        "Meest专线": "STANDARD#MEEST#MEEST#STANDARD",
        "UBI": "STANDARD#UBI#UBI#STANDARD",
        "eTotal": "STANDARD#ETOTAL#ETOTAL#STANDARD",
        "e邮宝": "AE#E_PACKET#EMS_ZX_ZX_US#STANDARD",
        "中东专线": "STANDARD#ARAMEX#ARAMEX#STANDARD",
        "中国邮政大包": "STANDARD#CPAP#CPAP#STANDARD",
        "中国邮政挂号小包": "CAINIAO#CPAM#CPAM#STANDARD",
        "佳成专线": "STANDARD#JCEX#JCEX#STANDARD",
        "巴西邮政": "STANDARD#CORREIOS_BR#CORREIOS_BR#STANDARD",
        "希凯易专线": "STANDARD#CKE#CKE#STANDARD",
        "希杰物流": "STANDARD#CJ#CJ#STANDARD",
        "德胜特货挂号": "STANDARD#BSC_STANDARD_SG#BSC_STANDARD_SG#STANDARD",
        "新加坡邮政挂号小包": "CAINIAO#SGP#SGP#STANDARD",
        "无忧集运-巴西": "STANDARD#CAINIAO_CONSOLIDATION_BR#CAINIAO_CONSOLIDATION_BR#STANDARD",
        "无忧集运-沙特": "STANDARD#CAINIAO_CONSOLIDATION_SA#CAINIAO_CONSOLIDATION_SA#STANDARD",
        "无忧集运-阿联酋": "STANDARD#CAINIAO_CONSOLIDATION_AE#CAINIAO_CONSOLIDATION_AE#STANDARD",
        "燕文特货挂号": "STANDARD#YANWEN_STANDARD_SG#YANWEN_STANDARD_SG#STANDARD",
        "燕文航空挂号小包": "CAINIAO#YANWEN_AM#YANWEN_AM#STANDARD",
        "纬狮标准小包": "STANDARD#AE_360LION_STANDARD#AE_360LION_STANDARD#STANDARD",
        "翼速专线": "STANDARD#GES#GES#STANDARD",
        "芬兰邮政挂号小包": "CAINIAO#ITELLA#ITELLA#STANDARD",
        "菜鸟专线-标准": "STANDARD#AE_CAINIAO_STANDARD#AE_CAINIAO_STANDARD#STANDARD",
        "菜鸟保税出口-标准": "STANDARD#CAINIAO_BE_STANDARD#CAINIAO_BE_STANDARD#STANDARD",
        "菜鸟列日TS90标准配送": "STANDARD#CAINIAO_TS90_STANDARD#CAINIAO_TS90_STANDARD#STANDARD",
        "菜鸟大包专线": "CAINIAO#CAINIAO_STANDARD_HEAVY#CAINIAO_STANDARD_HEAVY#STANDARD",
        "菜鸟急速达": "STANDARD#AE_4PL_STANDARD_CFD_AE#AE_4PL_STANDARD_CFD_AE#STANDARD",
        "菜鸟特货专线－标准": "CAINIAO#CAINIAO_STANDARD_SG#CAINIAO_STANDARD_SG#STANDARD",
        "赛拾": "STANDARD#CHOICE#CHOICE#STANDARD",
        "递四方专线小包": "STANDARD#FOURPX_RM#FOURPX_RM#STANDARD",
        "通邮": "STANDARD#LAOPOST#LAOPOST#STANDARD",
        "韩国邮政": "STANDARD#POSTKR#POSTKR#STANDARD",
        "顺丰国际挂号小包": "STANDARD#SF_EPARCEL#SF_EPARCEL#STANDARD",
        "顺友": "STANDARD#SUNYOU_RM#SUNYOU_RM#STANDARD",
        "顺友特货专线": "STANDARD#SHUNYOU_STANDARD_SG#SHUNYOU_STANDARD_SG#STANDARD",
        "飞特物流": "STANDARD#FLYT#FLYT#STANDARD",
        # # 速运
        # "AliExpress 无忧物流-优先": "CAINIAO#CAINIAO_PREMIUM#CAINIAO_PREMIUM#EXPRESS",
        # "AliExpress 无忧物流-自提": "CAINIAO#CAINIAO_STATION#CAINIAO_STATION#EXPRESS",
        # "DHL": "WM#DHL#DHL#EXPRESS",
        # "DPEX": "WM#TOLL#TOLL#EXPRESS",
        # "EMS": "WM#EMS#EMS#EXPRESS",
        # "E特快": "WM#E_EMS#E_EMS#EXPRESS",
        # "Fedex IE": "STANDARD#FEDEX_IE#FEDEX_IE#EXPRESS",
        # "Fedex IP": "WM#FEDEX#FEDEX#EXPRESS",
        # "SMSA": "STANDARD#SMSA#SMSA#EXPRESS",
        # "UPS全球快捷": "STANDARD#UPSE#UPSE#EXPRESS",
        # "UPS全球速快": "WM#UPS#UPS#EXPRESS",
        # "顺丰速运": "STANDARD#SF#SF#EXPRESS"
    }
}

# 物流发送国
FORM_COUNTRY = "CN"

# 物流到达国家
COUNTRY_LIST = {
    # "IT": "意大利",
    # "CZ": "捷克",
    # "BG": "保加利亚",
    # "HU": "匈牙利",
    # "NL": "荷兰",
    # "KR": "韩国",
    "JP": "日本",
    # "PL": "波兰",
    # "FR": "法国",
    # "TH": "泰国",
    # "MX": "墨西哥",
    # "IL": "以色列",
    # "CH": "瑞士",
    # "BE": "比利时",
    # "GB": "英国",
    # "CL": "智利",
    # "DE": "德国",
    # "AU": "澳大利亚",
    # "IE": "爱尔兰",
    # "SK": "斯洛伐克",
    # "TR": "土耳其",
    # "SE": "瑞典",
    # "US": "美国",
    # "CA": "加拿大",
    "NZ": "新西兰"
}


def login():
    """
    fixme 登入情况比较复杂无法获取对应的cookies信息
    登录账户,获取登录cookie信息
    :return:
    """
    account = {"action": "user_login",
               "user_login": "liuzhijun",
               "user_pass": "**********",
               "remember_me": "1"}
    response = requests.post(LOGIN_URL, data=account)
    print(response.cookies)
    cookies = dict((name, value) for name, value in response.cookies.items())
    return cookies


def generate_http_header():
    # 获取cookies 调用
    """
        fixme 待定  可以循环创建请求头？
        需要从返回的response中获取 set-cookies 信息 然后设置相应的信息进行查询
        JSESSIONID=4E112E8EA3EC8564977FC7CCA7A15D87;
        xman_t=UnS3HkzePGPMxqbsykrvQdzc4Wb5DHJtmlVLDQerfMCtSkopYcfaXkS3v/p/HiYSP5g83v60TWZxXww1R8PSioTZHKxbTW8tNuh4W6Yc9DKiE1tCeUBWTREoIs2AWu2rcizopwVju0Z8eazGc30Imp5wkcxhLaMcCgxP7qHoi4BLKsyw/OXYAsyLr9w9Q+EY/+g5bFpJ8Kn6pewAG0G8tAm6viV2TA8P62HNnEM5cY/i/NeQUfWMsy+Y14K2TWpHlPZE3rASfM3hhvEQgPr+sAyJJjvwRblkRTz/2XTKRCtS1wyUaRToAnxAReyuzNavZac5ICCuIQmlaY1ox7l5HQYhTkBKtEQdOZOMRe7PWiefvsPSfhGX+qM4sGqFWeSpuTpt024FX2yM24SJ82PU2Z56mM9UzHjzBniLXnSOSCScKe5JSy7yCNxCULy3cmDxyTwV7XMMBujShgOzXhEU7hwQQEmHRw22ZAPFyYtuxrhZVIk24DjdRGu5l1JejOlEYGdtXn7kpd0XGmGc0ArcDz1WKmVEIamLfGba3tbRzsBCpbsNrC+h7dYSD5ZjS4o+J2c5WvkE65+I9UyvIN50+xaZe0l/jBDBQX04WGNf5drvnJ/fYzP8gC6nIXbpWJLazwPLBqDRxiRTCeTlulRtOi5BO6tHCe8zmEj6AjJl3zA=; Domain=.aliexpress.com; Path=/; HttpOnly
        intl_common_forever=iR3O1iz3NsbO6gS79s8GdatXt0sPILQbIgrIWO4quiSUH5NSMYtPEA==; Domain=.aliexpress.com; Expires=Sun, 27-Mar-2089 10:57:50
    """
    # cookie = r"ali_apache_id=11.180.122.26.1593845422944.438226.6; _ga=GA1.2.774632206.1595569462; cna=yxPrF3ab6WACAd9oBhMIXDEl; _fbp=fb.1.1612885881894.1749047478; __utmz=3375712.1613278127.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=3375712.774632206.1595569462.1613278127.1613519532.2; aep_common_f=TVNyuFr454ET3/uI3Eyqb4Ye6PX6X+OmLpW6xExC82VIYsRqm6piQw==; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094001313884215%091005001438522208%091005002154568572%091005001438132036%094000723099479%091005001438132036%091005002223337276%091005002223337276; _lang=zh_CN; UM_distinctid=177f63af0871b6-0c2902b63f744a-53e356a-15f900-177f63af0882e3; CNZZDATA1254571644=1636228813-1614739903-%7C1614739903; _hvn_login=13; aep_usuc_t=ber_l=A0; ali_apache_tracktmp=W_signed=Y; intl_locale=zh_CN; xlly_s=1; _m_h5_tk=0281590fd7360198d630fe42496351a0_1615301806949; _m_h5_tk_enc=fb2959046a154571708fcbb377532cda; acs_usuc_t=acs_rt=b1ebfdd1399a46e29af5227e289049a6&x_csrf=yxi54m5t6tt_; havana_tgc=eyJjcmVhdGVUaW1lIjoxNjE1Mjk0NjQ3MzY3LCJsYW5nIjoiemhfQ04iLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMTA2MjUyNTMwOTAsInRndElkIjoiMUZFczdPbVdWNnhRVEwxVlc4czUyMEEifX19fQ; xman_us_t=x_lid=cn1540298555lkrw&sign=y&rmb_pp=2048453046@qq.com&x_user=25R75Sycbb2mHUMJ6/yiwqnWH3ZSoDCvw0YtKlu0fBw=&ctoken=n7rbyz2ozbhr&need_popup=y&l_source=aliexpress; xman_f=7skTp3J8ON37cRJ5cM4kdYOVP/PUkuVC26lCkkfOukIED3JmdMqOcLpNtrz7fYhKKdMDLcV9DOiRCHsCE+irGgn/3Gy7Cwpn527lGeHL3UbUx8hsrFAwoPiQnbJBvAVDlktgc9+cPBFjvisArARcVgj05Y7nFGYmBHkLEwykZzNUkCYOsgijP52tN6V+JEFUc6zg2aF8bQoCnJiYmPkjzt29MFDksMxHrALAmmJDf4UpD5i1Aw6hXER/4kKkgcoN806D5fWOXMRvXpNgp3kJewGpFtuRNVCfYa40/jQ3zzsKKvIXU+ZJ8tzbU+wN0AItvGk8G9u1QddFcjYaO2PUKaHElZWvH2SRi44kmFF8eMA17jvZQCn8+LW5pJ5q35cJy//1j2/8jYgEbbBI2Z5PdUUZJwZSWGXBxjEv2MyJSPo=; ali_apache_track=ms=|mt=2|mid=cn1540298555lkrw; xman_us_f=zero_order=y&x_locale=zh_CN&x_l=1&last_popup_time=1614670454944&x_user=CN|Doris|Peng|cnfm|250464581&no_popup_today=n&x_lid=cn1540298555lkrw&x_c_chg=1&acs_rt=dfe05eec0d3745328c2b02be9a19c5ee; aep_usuc_f=isfm=y&site=glo&x_alimid=250464581&iss=y&s_locale=zh_CN&b_locale=en_US; JSESSIONID=D0E55C2C92F9DFE17C745457CD8F3A68; xman_t=zChx8zpegQBFc5nimzWWDCgg9F533/z+deSP5Gx87o4OqQ4CvE9D/U4EDiyvrDi6Us42n1pQOmQhedgSDbEsGotYzEhyp6MTZTv4+SIzFV3RjJ4hB6dPGppEYZ422ie2SFkuDcNSgAfZa9yc8CqGS8FYFmf5Yo4EWgKd438MRjFA4mDxux9x0n+6UTRpa7VtyNpDq0wjlVZ9WEa2Daf4sSf+bNYm69lUyUQBVaPmNBcosz2HxpWSerYsAwcRe9gS3TN0OEZfZR0rLaWB3iT82HCMOKq/HhXXTKIOJ1BEV0d4AVvxw2sOyZ0VM4T9fLRr+WCkTacE/1yfACBQsbbLpp2RsbLbhCrrrKGOORO50PM/zhgr7mD6NC0nH5mSVk40Id3DU1a46Q3WWLtwXr86PeQ3MoGYfk+hiTRyjjEKG/gjID2v2lMbIHeb7nAfCMXopLCRTeFdm/APIZBPVEbCB3sEbKnqrA9BFghnS8rB32X/6sDmqOEqvz8cPSitsf+eZsVncD8emr9/Ojp053eVHkkYgy+k3bzEeEEVrajKIa2uD74sd11xj6Ncb2dw5qRncQod8tP/kztK26Hbe20NcZYEXlIS5BMB5eRFEg/4spydVfIS88+9uWWePJ0ce3D5+Ru11Or4BniD6Zou18KkIQmDurB6PZSujPiDTP6vLts=; intl_common_forever=bDRtUto9wwlA3kJZ9Tr3o7rXvsarWt8iw8JL18rukVweT8M+lWo/Ng==; tfstk=cuwABP97cabmiPi8YSCkfEcayoqAarC-7ig9BiFmkkwRhUpD3sDuKJBTRIiwkYIR.; l=eBP_DkieOQaQuOMABO5Cnurza77TEQRfcPVzaNbMiInca6tlwFjXaNCQZ4-Xkdtjgt5DSFxzPnnb5REk8-4U-x1KsF9RwR2tYvvw8e1..; isg=BBsbJ4b3_-VoWDxW2z0PuPVbqn-F8C_yIZH98A1aPZo_7DPOk8EnQ4wqgkziSYfq"
    cookie = r"ali_apache_id=11.180.122.26.1593845422944.438226.6; _ga=GA1.2.774632206.1595569462; cna=yxPrF3ab6WACAd9oBhMIXDEl; _fbp=fb.1.1612885881894.1749047478; __utmz=3375712.1613278127.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=3375712.774632206.1595569462.1613278127.1613519532.2; aep_common_f=TVNyuFr454ET3/uI3Eyqb4Ye6PX6X+OmLpW6xExC82VIYsRqm6piQw==; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%094001313884215%091005001438522208%091005002154568572%091005001438132036%094000723099479%091005001438132036%091005002223337276%091005002223337276; _lang=zh_CN; UM_distinctid=177f63af0871b6-0c2902b63f744a-53e356a-15f900-177f63af0882e3; CNZZDATA1254571644=1636228813-1614739903-%7C1614739903; _hvn_login=13; aep_usuc_t=ber_l=A0; ali_apache_tracktmp=W_signed=Y; intl_locale=zh_CN; _m_h5_tk=d2a1d21dc8f0721704aa18db1b4d6271_1615546519435; _m_h5_tk_enc=3903e20f16a000d3f99f7f587e056567; acs_usuc_t=acs_rt=b1ebfdd1399a46e29af5227e289049a6&x_csrf=q_d1wna7goch; havana_tgc=eyJjcmVhdGVUaW1lIjoxNjE1NTM5NTc1MzIwLCJsYW5nIjoiemhfQ04iLCJwYXRpYWxUZ2MiOnsiYWNjSW5mb3MiOnsiMTMiOnsiYWNjZXNzVHlwZSI6MSwibWVtYmVySWQiOjIyMTA2MjUyNTMwOTAsInRndElkIjoiMVdPeko2MGxxd3lWcGp1T1M4dHVzNlEifX19fQ; xman_us_t=x_lid=cn1540298555lkrw&sign=y&rmb_pp=2048453046@qq.com&x_user=z9WRDBsWprl67nLXi8tOAfv50i07RptEE8OrowvhawQ=&ctoken=b1oykygkugot&need_popup=y&l_source=aliexpress; xman_f=wx4/PBqiLm4igjbIQgjDAcCfWsvfwT5WdOoq6R8arOMZOSRAnzi79wari5V979EI4fNMLFQ77NCuPvhokUST0eH97pmVj7DBHO0FXTUW8mBOigkMYjolznAvPy6R3TDm+EksE4vAjQLfsST1+nqI+4vU6dMBPtG2AYEXWu7Nfws/x6mOC7haGA9SYUgUxgd2G5CM/qR6fHUx7gu4/rdhJKVcmQMroe/BdkVczzyrDGJoj1JDzvMU3mEkImvH7ZPlq+XZ6zXXyF057JKK3GqWcKJUkRuVL81WIP3NyJUfUJgfdbGqM9Z91uj49LVgBhmGWbHuGayNHL6UOT81UC57I7OGZSVvL3CUmwYvDeRyxenPFJRCRXYjwjT0ngObr6bRhXkzNugbt7dmD7ca8pcf73Vfa7O5Cm8TiLCl5mY7SrA=; ali_apache_track=ms=|mt=2|mid=cn1540298555lkrw; xman_us_f=zero_order=y&x_locale=zh_CN&x_l=1&last_popup_time=1614670454944&x_user=CN|Doris|Peng|cnfm|250464581&no_popup_today=n&x_lid=cn1540298555lkrw&x_c_chg=1&acs_rt=dfe05eec0d3745328c2b02be9a19c5ee; aep_usuc_f=isfm=y&site=glo&x_alimid=250464581&iss=y&s_locale=zh_CN&b_locale=en_US; JSESSIONID=0E2D23F775E022F84C17C27A441EC6DD; intl_common_forever=5VbUNwgYlRHKQ3MpNehm//6SkoJBSlJ/10BacuDMDQFySvrtFLCb0w==; xman_t=G49n7tq5+UyugWS5slg2GKkqGPKWYQfUu8wEkGAKJF+hKe1T3jEJ0TuWgyMbKvE/4417Ex6kMAhfBjjvXliOU/GQw3dWjJ4NquMBLXtAxM4dfNRfEjSgMSQ8Ng2dyk9aQ/yM7JBkeN4JAUVIhKMQFEnwcEf/+i8kXV3OBH69VQPvLEy15rxAtvrFs9HaOrtAHcUslzb5+bR6UQy+Ws05BKCBdyvg6Sne5W70/tYf/7nj5XmwWxygnYruRv55J/+d5QxFLB+2U61xDzMvh9hXRs7B5OoJd1r0XKpETpOL+fLNbfjHP7xZg/fcCZ9jJ4mtWg8TfkienzUxGIIMRJDJwMzcVOFsDVVrbVBe5Z6krX4dflVqRLJI9Mqc0SbLSYQzxmW/Tq4cvU2huCUdIUGs+BfbSs9kNv6L0UNjjgVNikYVMOLMbLuuMLi5UW8x8uwC99T0pRASJrwb7ZC1PdwLRo0Ds8OHQiBeE6IYbtd6GfokBdbiyfQP6TSvd3gcpTgitf5776u70smPGUD/sHcTRz8agtcOp+VphF0RMQ6UWmN2W74MaILftwor9gJI2dyyXRKgT3joV0ODEVLY2xX8iMiXWGd5budE+cTykh5DJB67svtKQ8WeNw2CqYI9tcEeXgimMKunmRQAbeJ4iqwPpwQwZY7j+a/lWgKqVG4iz0k=; tfstk=cKxfIsVRkSVjHN3a0KMzbPiKfQMRhO1UcTzfMKTQuCfp-5li3Kr1iaZFOVjOS7qRJT1..; l=eBP_DkieOQaQuwWEBO5aFurza77OrIRb4sPzaNbMiIncB6ujlhp_LJKQDcjYPuT5WhQNhsMXR3zWDma6BeYBqMsInxvTCoL8N7Mmn; isg=BKujwkK_T7kEiKymK-2faOWrOs-VwL9CMUGNoB0oR-pBvMsepZMhkklUEvzSnBc6"

    useragent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    post_header = {
        "accept": r"application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content - type": r"application/x-www-form-urlencoded; charset = UTF-8",
        "cookie": cookie,
        "userAgent": useragent
    }
    return post_header


def getLogisticsPlan(country_list, page_info, recommand_flag):
    """
        获取物流信息
    :param country_list:
    :param page_info: 包含包裹重量
    :param recommand_flag:
    :return:
    """

    logisticsinf_map = {}
    for country in country_list:
        post_data = {
            "_csrf_token_": "rf7iokvwo0l8",
            "logistics-services-set": r"/",
            "logistics-services-list-all": "[[Ljava.lang.String;@4d577287,",
            "logistics-class-filter": "ALL",
            "sort-by-recommend-points": "0",
            "sort-by-logistics-freight": "1",  # 按价格升序排列
            "toCountry": country,
            "fromCountry": FORM_COUNTRY,
            "logistics-express-item": list(page_info["logistics-express-item"].values()),
            "limitedGoods": "general",  # 商品类别
            "orderAmount": page_info["orderAmount"],  # 订单金额
            "packageWeight": page_info["packageWeight"],  # 包裹重量
            "packageLength": page_info["packageLength"],  # 包裹长度
            "packageWidth": page_info["packageWidth"],  # 包裹宽度
            "packageHeight": page_info["packageHeight"]  # 包裹高度
        }

        respons = requests.post(LOGISTICS_URL, headers=generate_http_header(), data=post_data)
        logistics_inf = json.loads(respons.text)
        logisticsinf_map[country] = logistics_inf
    return logisticsinf_map


def handelDateToExcel(logisticsinf_map, file_target_path):
    """
        处理物流json数据并生成excel文件
    :param logisticsinf_list: 物流信息
    :return:
    """
    field_map = {
        "服务名称": "serviceName",
        "类型": "logisticsClassForDisplay",
        "推荐指数": "recommendPoints",
        "时效": "deliveryPeriod",
        "纠纷率": "dispute",
        "DSR物流": "dsr",
        "试算运费": "freight",
        "更多信息": "extInfo",
        "是否推荐": "isRec",
        "线上发货": "isOnlineShipping"
    }
    # 处理数据 每个对象单独存为一个sheet页
    key_list = list(field_map.keys())
    val_list = list(field_map.values())
    excel = ExcelUtil(key_list, file_target_path)
    for key, logistics_inf in logisticsinf_map.items():
        # 二维数组
        sheet_data = []
        for tmp in logistics_inf["logisticsServices"]:
            row_data = []
            # 循环获取对应数据
            for i in range(0, len(val_list)):
                row_data.append(tmp[val_list[i]])
            sheet_data.append(row_data)
        # 向Excel 中写数据
        excel.write_excel(COUNTRY_LIST.get(key), sheet_data)
    # 保存excel 文件
    excel.save()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tmpList = getLogisticsPlan(COUNTRY_LIST.keys(), PAGE_INFO, True)
    save_path = "C:\\Users\\Baijb\\Desktop\\物流信息_weight(_%s)lwh(%s_%s_%s).xls" % (PAGE_INFO["packageWeight"], PAGE_INFO["packageLength"], PAGE_INFO["packageWidth"], PAGE_INFO["packageHeight"])
    handelDateToExcel(tmpList, save_path)

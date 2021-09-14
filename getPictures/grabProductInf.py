# -*- coding: utf-8 -*-

import os
import re
import shutil

import requests
import json
import demjson

from PIL import Image
from openpyxl import load_workbook
from pyquery import PyQuery as pq

from commUtil.propertiesUtil import Properties
from login.alibabaLogin import AlibabaLogin

URL = "https://detail.1688.com/offer/641691867854.html?spm=a262uh.11734178.favorite-offers-offer-list-offer12.2.6d392ef60dvg4z"
# URL = "https://item.taobao.com/item.htm?spm=a1z10.5-c-s.w4002-22271431933.60.556e23c4mVJ9TB&id=646063149217"

# 静态参数
MAIN_PIC = "mainPic"
DESC_PIC = "descPic"
STOCK_INF = "stockInf"
OTHER_INF = "otherInf"
# COOKIES = "t=04d720a58dd60183eeed327c416278bc; cna=ubEuGbm+4RwCAbf7XQleDKYV; lgc=tb925976948; tracknick=tb925976948; thw=cn; _m_h5_tk=1559500873e2e3a70bd5c42cea344870_1622816735116; _m_h5_tk_enc=39e6f65b4a22eadadd6d1ce9a8dcf39f; xlly_s=1; cookie2=15fa6734c0091b1135352597f5df4813; _samesite_flag_=true; sgcookie=E1007JyNfWAKL5GEl+Wo2cLOuVkKTH7us08bo0jio1ErVWoH+5wXIjdcPCdZfdWdsiPnNQkZptHMwYcuZ7h960EwZA==; unb=2210611464742; uc3=id2=UUpgRsIuDUi3Gn4YgA==&lg2=Vq8l+KCLz3/65A==&nk2=F5RMGyZRZ93Ox8g=&vt3=F8dCuw77pVaA5+6WkEo=; csg=547eac52; cookie17=UUpgRsIuDUi3Gn4YgA==; dnk=tb925976948; skt=66360880cecf4e5b; existShop=MTYyMjgwNzUyMQ==; uc4=id4=0@U2gqyZJ/Ix2UNf+IxUaq4GdAxkyKTd8p&nk4=0@FY4HXgw1vlNQNbVDYN1lTsREnUPRKA==; _cc_=UtASsssmfA==; _l_g_=Ug==; sg=824; _nk_=tb925976948; cookie1=BYECxSBpVqRK3D7hRVJlJXfItlB4EbVOmGhKwpY/iY4=; enc=Ja11bdTMN2do7kZoQ6skj8Ja8Dllxqdl/16a8f79aCE2DUzNiaLQzaz4lNqo9sVqKqyiRXkS8lMZn7Zy+muGScMVqZPHW16+BDkwd6IRxOY=; mt=ci=0_1; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw==&cookie14=Uoe2z+ti9RyBtQ==&cookie21=URm48syIYn73&existShop=false&cookie15=V32FPkk/w0dUvg==&pas=0; hng=CN|zh-CN|CNY|156; v=0; _tb_token_=feae5361043b3; tfstk=cQ6FBgszxJeFZNv7Mp9rAVFfJQ3dZo6ceR-2t1z9WJpEt3Ahiq0JjQEVbg8YIBf..; l=eB_7LphHjl-06kOLBOfZourza77tsIRvjuPzaNbMiOCP_Lfw5CDhW6_NqB8eCnGVh6bDR3WWjis6BeYBq3xonxvte5DDwQHmn; isg=BNDQiLezhOmbLljtaVTHkVnMoR4imbTjPgOGYcqhmSv-BXCvcqr-csk32c3l_my7"
COOKIES = None
LOGIN_TOOL = None
properties_map = Properties("../login/config.properties").getproperties()

s = requests.Session()


def wrap_web_header():
    """
        可以使用simulation进行模拟登入 封装请求头信息
    :return: 请求头信息
    """
    global COOKIES
    global LOGIN_TOOL
    accept = r"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    if COOKIES is None:
        LOGIN_TOOL = AlibabaLogin(properties_map.get("Alibaba").get("username"),
                                  properties_map.get("Alibaba").get("password"))
        LOGIN_TOOL.login()
        cookies_map = LOGIN_TOOL.get_cookies()
        if cookies_map is not None and len(cookies_map) > 0:
            COOKIES = ''
            for tmp_obj in cookies_map:
                if tmp_obj["name"] is not None and tmp_obj["value"] is not None:
                    COOKIES += tmp_obj["name"] + "=" + tmp_obj["value"]
        else:
            raise Exception("缺少cookies信息")  # 抛出异常信息

    headers = {
        "accept": accept,
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "cookie": COOKIES,
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": user_agent
    }
    return headers


def dir_download_images(a_url, a_filename, a_save_dir="C:\\Users\\Baijb\\Desktop\\产品模板\\"):
    """
        直接下载文件信息
    :param a_url:  文件路径
    :param a_filename:
    :param a_save_dir:
    :return:
    """
    imgs_data = requests.get(a_url, headers=wrap_web_header())
    save_name = str(a_save_dir + a_filename)
    if not os.path.exists(a_save_dir):
        os.makedirs(a_save_dir)
    with open(save_name, 'wb') as f:
        f.write(imgs_data.content)


def resize_pic(pic_path, width, height, rtocut_flag=False):
    """
    缩放图片
    :param pic_path: 图片路径
    :param width: 宽
    :param height: 高
    :param rtocut_flag:按比例裁剪
    :return:
    """
    image = Image.open(pic_path)
    base_width = width
    h_size = height
    if rtocut_flag:
        w_percent = base_width / float(image.size[0])
        h_size = int(float(image.size[1]) * float(w_percent))

    # 默认情况下，PIL使用Image.NEAREST过滤器进行大小调整，从而获得良好的性能，但质量很差。
    im_resized = image.resize((base_width, h_size), Image.ANTIALIAS)
    im_resized.save(pic_path)


# def cv_resize

def grab_webpage(url):
    """
        获取指定的1688路径下的网页信息
    :param url:
    :return:  字典类 网页内容
    """
    webpage_info = {}
    resp_data = requests.get(url, headers=wrap_web_header()).content

    doc = pq(resp_data)
    pic_objs = doc(".tab-trigger").items()
    main_pic_urls = []
    for pic in pic_objs:
        json_obj = json.loads(pic.attr("data-imgs"))
        pic_url = json_obj["original"]
        pic_name = pic_url[json_obj["original"].rindex("/") + 1:]
        main_pic_urls.append({"pic_url": pic_url, "pic_name": pic_name})
    webpage_info[MAIN_PIC] = main_pic_urls

    # 详情信息是直接请求的
    desc_data_url = doc(".desc-lazyload-container").items()
    desc_pic_urls = []
    for tmp in desc_data_url:
        data_tfs_url = tmp.attr("data-tfs-url")
        desc_data_info = requests.get(data_tfs_url, headers=wrap_web_header()).content  # .decode('utf-8')
        img_lst = pq(desc_data_info)("img")
        for img_idx in range(0, img_lst.length):
            attr_src = pq(img_lst[img_idx]).attr('src')
            pic_url = pq(img_lst[img_idx]).attr('src')[attr_src.index("h"):attr_src.rindex("\\")]
            pic_name = pic_url[pic_url.rindex("/") + 1:]
            desc_pic_urls.append({"pic_url": pic_url, "pic_name": pic_name})
    webpage_info[DESC_PIC] = desc_pic_urls

    # 获取库存（尺码，价格信息）
    # stock_inf_tr = doc(".obj-sku table tr")
    # stock_inf = []
    # for tr in stock_inf_tr:
    #     name = pq(tr).find("td.name").text()
    #     price = pq(tr).find("td.price em.value").text()
    #     count = pq(tr).find("td.count").text()
    #     tmp = {"name": name, "price": price, "count": count, "weight": "0"}  # weight 克重暂时使用0来进行测算
    #     stock_inf.append(tmp)
    # webpage_info[STOCK_INF] = stock_inf
    config_str = ""
    data_str = ""
    stock_inf = []
    try:
        config_str = re.search(r"var iDetailConfig =([\s\S]*)var iDetailData = ([\s\S]*)iDetailData.allTagIds([\s\S]*)",
                               resp_data.decode()).group(1)
        data_str = re.search(r"var iDetailConfig =([\s\S]*)var iDetailData = ([\s\S]*)iDetailData.allTagIds([\s\S]*)",
                             resp_data.decode()).group(2)
    except UnicodeDecodeError:
        config_str = re.search(r"var iDetailConfig =([\s\S]*)var iDetailData = ([\s\S]*)iDetailData.allTagIds([\s\S]*)",
                               resp_data.decode('gbk')).group(1)
        data_str = re.search(r"var iDetailConfig =([\s\S]*)var iDetailData = ([\s\S]*)iDetailData.allTagIds([\s\S]*)",
                             resp_data.decode('gbk')).group(2)
    if data_str is not None:
        config_map = demjson.decode(config_str.replace(";", ""))
        sku_map = demjson.decode(data_str.replace(";", ""))
        price = config_map['refPrice']
        for key, val in sku_map["sku"]["skuMap"].items():
            if config_map['isRangePriceSku'] == 'false':
                price = val["price"]
            tmp = {"name": key, "price": price, "count": val["canBookCount"], "weight": "0"}
            stock_inf.append(tmp)
    webpage_info[STOCK_INF] = stock_inf
    return webpage_info


# Press the green button in the gutter to run the script.
def handel_pic_info(page_info, base_path="C:\\Users\\Baijb\\Desktop\\产品模板\\"):
    """
    处理图片信息
    :param page_info: 图片名称及下载路径
    :param base_path: 文件保存路径
    :return:
    """
    main_pic_inf = page_info[MAIN_PIC]
    main_pic_basepath = base_path + "01主图\\"
    for pic in main_pic_inf:
        dir_download_images(pic["pic_url"], pic["pic_name"], main_pic_basepath)
        if os.path.exists(main_pic_basepath + pic["pic_name"]):
            resize_pic(main_pic_basepath + pic["pic_name"], 800, 800)

    desc_pic_inf = page_info[DESC_PIC]
    desc_pic_basepath = base_path + "02详情\\"
    for pic in desc_pic_inf:
        dir_download_images(pic["pic_url"], pic["pic_name"], desc_pic_basepath)
        if os.path.exists(desc_pic_basepath + pic["pic_name"]):
            resize_pic(desc_pic_basepath + pic["pic_name"], 700, 700, True)

    return


def handel_stock_inf(stock_inf_lst, base_path="C:\\Users\\Baijb\\Desktop\\产品模板\\"):
    """
    复制成本信息模板，向指定位置设置库存信息并计算售卖价
        公式：
    :param stock_inf_lst: 库存信息列表
    :param base_path:文件保存路径
    :return:
    """
    shutil.copyfile("template.xlsx", base_path + "03成本计算.xlsx")
    wb = load_workbook(base_path + "03成本计算.xlsx")
    ws = wb.get_sheet_by_name('价格')
    # 从L13开始设置库存信息
    idx = 13
    for tk_inf in stock_inf_lst:
        # tmp = {"name": name, "price": price, "count": count, "weight": "0"}  # weight 克重暂时使用0来进行测算
        ws['L%s' % idx] = tk_inf["name"]
        ws['M%s' % idx] = tk_inf["count"]
        ws['N%s' % idx] = tk_inf["price"]
        ws['O%s' % idx] = tk_inf["weight"]
        ws['P%s' % idx] = "=((N%s + ($D$4 * O%s+$E$4)) / (1 -$G$5-$H$5-$I$5)) /$J$5" % (idx, idx)  # 计算最终成本价
        ws['Q%s' % idx] = "=P%s * (1 +$B$13)" % idx  # 售卖价
        ws['R%s' % idx] = "=Q%s / (1 -$D$13)" % idx  # 上货价
        idx = idx + 1

    ws = wb.get_sheet_by_name('产品链接')
    ws['B2'] = URL
    wb.save(base_path + "03成本计算.xlsx")


if __name__ == '__main__':
    """
        实现目标：
            1、下载主图图片、详情页图片到指定目录  **处理图片大小
            2、生成成本模板并填入相关数据（尺码信息）
    """
    # 获取阿里巴巴指定路径下的商品信息
    page_info = grab_webpage(URL)
    # 根据下载图片并根据图片类型裁剪  pil 处理
    handel_pic_info(page_info)
    # 处理库存信息
    handel_stock_inf(page_info[STOCK_INF])

    # cookiesStr = r"ali_apache_id=10.147.120.78.1568860040119.356581.5; cna=yxPrF3ab6WACAd9oBhMIXDEl; ali_ab=120.41.158.97.1612615929870.6; UM_distinctid=177776d64bc21f-0f09bab047943d-53e3566-15f900-177776d64bd2d3; taklid=8c9fe98a450643d5b1ce8a6d273b3143; hng=CN%7Czh-CN%7CCNY%7C156; CNZZDATA1261052687=696041790-1612615281-https%253A%252F%252Fdetail.1688.com%252F%7C1613477845; ad_prefer=\"2021/03/03 12:45:24\"; h_keys=\"ebaerr#32385161394#%u72d7%u72d7%u7275%u5f15%u7ef3%u5361%u901a%u72d7%u94fe%u5ba0%u7269#%u5361%u901a%u72d7%u94fe%u5ba0%u7269#%u4e50%u5ba0%u7535%u5b50%u6e90%u5934%u5382%u5bb6#%u6d94%u612c%u7587%u9422%u975b%u74d9%u5a67%u612c%u3054%u9358%u509a%ue18d#%u7ae5%u8da3%u7eaf%u68c9%u56db%u811a%u8863#%u9ec4%u91d1%u8c82%u72d7%u8863%u670d#%u5984%u5578#%u5efa%u5fb7%u5e02%u4e0b%u6daf%u9547%u58a9%u6cca%u8d38%u6613%u5546%u884c\"; lid=%E5%BF%83%E6%AE%87%E6%97%A7%E7%97%9B; ali_apache_track=c_mid=b2b-808862444|c_lid=%E5%BF%83%E6%AE%87%E6%97%A7%E7%97%9B|c_ms=1; _bl_uid=26k7wnUv91moj2gXX233yXF92Fbs; alicnweb=touch_tb_at%3D1617945381138%7Clastlogonid%3D%25E5%25BF%2583%25E6%25AE%2587%25E6%2597%25A7%25E7%2597%259B; CNZZDATA1253659577=2036282685-1612613793-https%253A%252F%252Fpurchase.1688.com%252F%7C1619103965; _csrf_token=1619108265746; xlly_s=1; cookie2=116657782bc95045685d767c72b0744c; t=dc1a133d68b679b18965bbfb8f1e4b7c; _tb_token_=5560e8e66bb4b; __cn_logon__=false; JSESSIONID=9F0322831D1B1FF335A76DA76AF7E021; tfstk=c_jABQYiA7Vcrh9RLZUoCS_5FCrOZlUJ_-OtX-eFt6BQ6MmOi_jhvlCIldlv28C..; l=eBr8qlYmjPw3aJfSBOfwourza77tQIRxSuPzaNbMiOCPO0BXymMRW61jDVxWCnGVh686J3kEpCzgBeYBqBAnnxv9zUAs1fMmn; isg=BFZW4sSFKqC9HR6YkQeq9UNwpwxY95oxjzlnzcC_VDnKg_YdKYXtQY55Hx9vFpJJ"
    # arrays = re.split('[;,]', cookiesStr)
    # for _str in arrays:
    #     print(_str)
    # login_tool = AlibabaLogin(properties_map.get("Alibaba").get("username"),
    #                           properties_map.get("Alibaba").get("password"))
    # print("区别----------------")
    # login_tool.login()
    # cookies_map = login_tool.get_cookies()
    # if cookies_map is not None and len(cookies_map) > 0:
    #     COOKIES = ''
    #     for tmp_obj in cookies_map:
    #         if tmp_obj["name"] is not None and tmp_obj["value"] is not None:
    #             print(tmp_obj["name"] + "=" + tmp_obj["value"])

    # resp_data = requests.get(URL, headers=wrap_web_header()).content.decode("gbk")
    # doc = resp_data

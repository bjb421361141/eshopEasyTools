# -*- coding: utf-8 -*-

import requests
import json
import os
from lxml import etree
from pyquery import PyQuery as pq

import re

url = "https://detail.1688.com/offer/638083001260.html?spm=a261y.7663282.1998411376.1.3de92e2cmonftL&&scm=1007.19151.166235.00&ODitemId=641691867854&itemId=638083001260&pvid=38a1506d-3fb3-4db0-bc73-c1037ca6acd2&extStr=638083001260..641691867854..2206891670226..1.0..1.0..47.6526855272886..1.0..sim..121778003..no..odTab..192002_194498_213250_17282_17474_17026_16514_16834_18754_17922_16962_17538_17410_18114_18050_98306_91010..38a1506d-3fb3-4db0-bc73-c1037ca6acd2..0.0..1007.19151.166235.0"

# contentDetailUrl = r"https://img.alicdn.com/tfscom/TB1YK4WtqNj0u4jSZFyXXXgMVXa"

accept = r"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
cookie = r"ali_apache_id=10.147.120.78.1568860040119.356581.5; cna=yxPrF3ab6WACAd9oBhMIXDEl; ali_ab=120.41.158.97.1612615929870.6; UM_distinctid=177776d64bc21f-0f09bab047943d-53e3566-15f900-177776d64bd2d3; taklid=8c9fe98a450643d5b1ce8a6d273b3143; hng=CN%7Czh-CN%7CCNY%7C156; ad_prefer=\"2021/03/03 12:45:24\"; h_keys=\"ebaerr#32385161394#%u72d7%u72d7%u7275%u5f15%u7ef3%u5361%u901a%u72d7%u94fe%u5ba0%u7269#%u5361%u901a%u72d7%u94fe%u5ba0%u7269#%u4e50%u5ba0%u7535%u5b50%u6e90%u5934%u5382%u5bb6#%u6d94%u612c%u7587%u9422%u975b%u74d9%u5a67%u612c%u3054%u9358%u509a%ue18d#%u7ae5%u8da3%u7eaf%u68c9%u56db%u811a%u8863#%u9ec4%u91d1%u8c82%u72d7%u8863%u670d#%u5984%u5578#%u5efa%u5fb7%u5e02%u4e0b%u6daf%u9547%u58a9%u6cca%u8d38%u6613%u5546%u884c\"; _bl_uid=26k7wnUv91moj2gXX233yXF92Fbs; CNZZDATA1261052687=696041790-1612615281-https%253A%252F%252Fdetail.1688.com%252F%7C1619697037; xlly_s=1; cookie2=17142b16a4dc4e93dd721a53ad982225; t=85c841cae1fa7c0acf0aff1127c875f6; _tb_token_=5e73b38eb177e; __last_loginid__=tb925976948; last_mid=b2b-22106114647429571d; csg=4a94ba7f; lid=tb925976948; uc4=id4=0%40U2gqyZJ%2FIx2UNf%2BIxUaq4GdCBz4lpkVT&nk4=0%40FY4HXgw1vlNQNbVDYN1lTLdbPG06IQ%3D%3D; ali_apache_track=c_mid=b2b-22106114647429571d|c_lid=tb925976948|c_ms=1; ali_apache_tracktmp=c_w_signed=Y; _csrf_token=1620199427447; _is_show_loginId_change_block_=b2b-22106114647429571d_false; _show_force_unbind_div_=b2b-22106114647429571d_false; _show_sys_unbind_div_=b2b-22106114647429571d_false; _show_user_unbind_div_=b2b-22106114647429571d_false; __rn_alert__=false; _m_h5_tk=ea160e944e23010c1c0158b1d9e2de21_1620208433975; _m_h5_tk_enc=160fb2ce2c7cd94e1827f783af3e272a; alicnweb=touch_tb_at%3D1620199444953%7Clastlogonid%3Dtb925976948; CNZZDATA1253659577=2036282685-1612613793-https%253A%252F%252Fpurchase.1688.com%252F%7C1620197065; __cn_logon__=false; JSESSIONID=96144122BCA06CCF19F5EA3D55B478EA; tfstk=ccQfBgAZpxDfD2EZusNr0xeOd0tcZM0Xam9AGMh0WAknS_CfiQgedlY9jY0JvQ1..; isg=BEBAIf5JNJE6XsgaC-lkl9mmEc4SySSTVnDKIrrRkdv6NeBfYtr7IxYPSZ31g9xr; l=eBr8qlYmjPw3affBBO5BPurza77TuIRb4rVzaNbMiInca66fUELnKNCC3pPe0dtjgt1h2etyAqdWadLHR3AMeiQaGjoqRB5tnxf.."
userAgent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"

headers = {
    "accept": accept,
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": cookie,
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": userAgent
}


# resp=requests.get(url,headers=headers).content.decode('utf-8')
# 报错：UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb9 in position 423: invalid start byte
# 突破反扒，返回响应

def download_images(a_url, a_filename):
    """
        下载图片
    :param a_url: 下载路径
    :param a_filename: 文件名
    :return:
    """
    resp_dtl = requests.get(a_url, headers=headers).content  # .decode('gbk')
    doc = pq(resp_dtl)
    bigImgs = doc('.big_img p img').items()
    count = 1
    # print(bigImgs)
    for bigImg in bigImgs:
        bigImgSrc = bigImg.attr("src")
        imgs_data = requests.get(bigImgSrc, headers=headers)
        file_name = r"C:\Users\Baijb\Desktop\产品图片/" + a_filename
        save_name = str(file_name)
        # 若图片目录文件不存在，则重建
        if not os.path.exists(save_name):
            os.makedirs(file_name)
        else:
            with open(save_name + '/{}.jpg'.format(count), 'wb') as f:
                f.write(imgs_data.content)
            count += 1


def dir_downloadImages(a_url, a_filename):
    imgs_data = requests.get(a_url, headers=headers)
    file_name = "C:\\Users\\Baijb\\Desktop\\产品模板\\" + a_filename
    save_name = str(file_name)
    with open(save_name, 'wb') as f:
        f.write(imgs_data.content)


# 方法-取得图片并下载数据
def getPics(a_url):
    resp_data = requests.get(a_url, headers=headers).content # .decode('gbk')
    doc = pq(resp_data)
    # 通过类选择器获取数据
    html = resp_data.decode("gbk")
    # https: // blog.csdn.net / liu35937266 / article / details / 78354622
    print(html)
    m = re.search(r'iDetailData', html, re.M | re.I)
    if m:
        print(m.group())
    else:
        print("not match!")
    picObj = doc(".tab-trigger").items()
    # print(pic)
    for pic in picObj:
        # 通过属性获取内容
        dataJson = pic.attr("data-imgs")
        jsonObj = json.loads(dataJson)
        picUrl = jsonObj["original"]
        picName = picUrl[jsonObj["original"].rindex("/") + 1:]
        # print(picUrl)
        # download_images(picUrl, picName)
        dir_downloadImages(picUrl, picName)
    descDataUrl = doc(".desc-lazyload-container").items()
    for tmp in descDataUrl:
        dataTfsUrl = tmp.attr("data-tfs-url")
        descDataInfo = requests.get(dataTfsUrl, headers=headers).content #.decode('utf-8')
        _element = etree.HTML(descDataInfo)
        _img = _element.xpath('//img')
        idx = 1
        for pic in _img:
            idx = idx + 1
            indx = pic.attrib.get('src').index("h")
            rindx = pic.attrib.get('src').rindex("\\")
            imgurl = pic.attrib.get('src')[indx:rindx]
            picName = imgurl[imgurl.rindex("/") + 1:]
            dir_downloadImages(imgurl, r"02详情/" + str(idx) + "_" + picName)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getPics(url)

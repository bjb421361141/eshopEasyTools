import os

import requests
import json
from pyquery import PyQuery as pq

URL = "https://detail.1688.com/offer/569380999718.html?spm=a2615.7691456.autotrace-offerGeneral.22.7fb13356ft1KPL"

# 静态参数
MAIN_PIC = "mainPic"
DESC_PIC = "descPic"
STOCK_INF = "stockInf"


def wrap_web_header():
    """
        可以使用simulation进行模拟登入 封装请求头信息
    :return: 请求头信息
    """
    accept = r"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    cookie = r"ali_apache_id=10.147.120.78.1568860040119.356581.5; cna=yxPrF3ab6WACAd9oBhMIXDEl; ali_ab=120.41.158.97.1612615929870.6; UM_distinctid=177776d64bc21f-0f09bab047943d-53e3566-15f900-177776d64bd2d3; taklid=8c9fe98a450643d5b1ce8a6d273b3143; hng=CN%7Czh-CN%7CCNY%7C156; __last_loginid__=tb69481656; CNZZDATA1261052687=696041790-1612615281-https%253A%252F%252Fdetail.1688.com%252F%7C1613477845; _m_h5_tk=b1e5de1fe6f5cffa57099c55b2f4a4bc_1614178568878; _m_h5_tk_enc=3d6cbfea17dca68ad265eedde28a766e; lid=tb69481656; ali_apache_track=c_mid=b2b-1888131324|c_lid=tb69481656|c_ms=1; xlly_s=1; _csrf_token=1614746489739; cookie2=14c3cc861c0178712f8e65a58d29a348; t=c924bdc6eeacc0becd416483c5b16c0b; _tb_token_=5ea37ea373a34; uc4=id4=0%40UOE5CegbctGyXq3V%2BPqnkbCFM7Gd&nk4=0%40FY4I5qbfZuXB6s%2FclX%2FMckWpVspP; __cn_logon__=false; alicnweb=touch_tb_at%3D1614746505232%7Clastlogonid%3Dtb69481656; ad_prefer=\"2021/03/03 12:45:24\"; h_keys=\"ebaerr#32385161394#%u72d7%u72d7%u7275%u5f15%u7ef3%u5361%u901a%u72d7%u94fe%u5ba0%u7269#%u5361%u901a%u72d7%u94fe%u5ba0%u7269#%u4e50%u5ba0%u7535%u5b50%u6e90%u5934%u5382%u5bb6#%u6d94%u612c%u7587%u9422%u975b%u74d9%u5a67%u612c%u3054%u9358%u509a%ue18d#%u7ae5%u8da3%u7eaf%u68c9%u56db%u811a%u8863#%u9ec4%u91d1%u8c82%u72d7%u8863%u670d#%u5984%u5578#%u5efa%u5fb7%u5e02%u4e0b%u6daf%u9547%u58a9%u6cca%u8d38%u6613%u5546%u884c\"; CNZZDATA1253659577=2036282685-1612613793-https%253A%252F%252Fpurchase.1688.com%252F%7C1614746977; JSESSIONID=1DED0C8440C06EF5C010D148516853D9; tfstk=cSRhBPZ2spWCXUBMhX1BurBRqY4ha5zNv_5w_CE69H560rJC8s0_Q-7xbPjpxQe5.; l=eBr8qlYmjPw3a0eoBO5Zourza779qCAfh1PzaNbMiInca61lHdTFiNCI-cLH2dtjgtfAietzPnnb5dFyl8zLRFZ7hHCkXHZLF9J6-; isg=BFxc9K32UFAlGyQuh2XA653yLXoO1QD_iuwalTZZK8e3gfoLXuPpj2J75el5DjhX"
    user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"

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
    imgs_data = requests.get(a_url, headers=wrap_web_header)
    save_name = str(a_save_dir + a_filename)
    if not os.path.exists(a_save_dir):
        os.makedirs(a_save_dir)
    with open(save_name, 'wb') as f:
        f.write(imgs_data.content)


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
            attr_src = img_lst.attr('src')
            pic_url = img_lst.attr('src')[attr_src.index("h"):attr_src.rindex("\\")]
            pic_name = pic_url[pic_url.rindex("/") + 1:]
            desc_pic_urls.append({"pic_url": pic_url, "pic_name": pic_name})
    webpage_info[DESC_PIC] = desc_pic_urls

    # 获取库存（尺码，价格信息）
    stock_inf_tr = doc(".obj-sku table tr")
    stock_inf = []
    for tr in stock_inf_tr:
        name = pq(tr).find("td.name").text()
        price = pq(tr).find("td.price").text()
        count = pq(tr).find("td.count").text()
        tmp = {"name": name, "price": price, "count": count}
        stock_inf.append(tmp)
    webpage_info[STOCK_INF] = stock_inf
    return webpage_info


# Press the green button in the gutter to run the script.
def handel_pic_info(page_info):
    # dir_download_images(pic_url, r"2详情/" + str(img_idx) + "_" + pic_name)
    pass


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

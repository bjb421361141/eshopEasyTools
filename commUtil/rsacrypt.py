# -*- coding: utf-8 -*-
# @Time: 2021/4/7 12:45
import base64

import rsa
from binascii import b2a_hex, a2b_hex

# 封装rsa工具类
from commUtil.propertiesUtil import Properties


class RsaCrypt:
    __slots__ = ("__pubkey", "__prikey")
    PUBKEY_HEAD = "-----BEGIN RSA PUBLIC KEY-----\n"
    PUBKEY_END = "-----END RSA PUBLIC KEY-----\n"
    PRIKEY_HEAD = "-----BEGIN RSA PRIVATE KEY-----\n"
    PRIKEY_END = "-----END RSA PRIVATE KEY-----\n"

    def __init__(self, pubkey, prikey):
        """
            字符串中的换行符置换成 “-”  生成的公钥和私钥不能含有 “-”
        :param pubkey: 公钥字符串 或pubkey对象
        :param prikey: 私钥字符串 或prikey对象
        """
        if isinstance(pubkey, rsa.PublicKey) and isinstance(prikey, rsa.PrivateKey):
            self.__pubkey = pubkey
            self.__prikey = prikey
        elif isinstance(pubkey, str) and isinstance(prikey, str):
            new_pub = str(self.PUBKEY_HEAD + pubkey.replace("-", "\n") + self.PUBKEY_END)
            new_pri = str(self.PRIKEY_HEAD + prikey.replace("-", "\n") + self.PRIKEY_END)
            try:
                self.__pubkey = rsa.PublicKey.load_pkcs1(new_pub.encode('UTF-8'))
                self.__prikey = rsa.PrivateKey.load_pkcs1(new_pri.encode('UTF-8'))
            except Exception as err:
                print(err)
                raise Exception("字符串构造公钥私钥对象异常！")
        else:
            raise Exception("构造参数类型不对！")

    def encrypt(self, text):
        """
            # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串
        :param text: 需要加密的数据
        :return:  返回加密字符串
        """
        ciphertext = rsa.encrypt(text.encode(), self.__pubkey)
        hex_str = b2a_hex(ciphertext)

        return base64.b64encode(hex_str)

    def decrypt(self, text):
        hex_str = base64.b64decode(text)
        decrypt_text = rsa.decrypt(a2b_hex(hex_str), self.__prikey)
        return decrypt_text


if __name__ == '__main__':
    # pubkey, prikey = rsa.newkeys(256)
    # pub = pubkey.save_pkcs1()
    # print(pub)
    # # pubfile = open('public.pem', 'w+')
    # # pubfile.write(pub)
    # # pubfile.close()
    #
    # pri = prikey.save_pkcs1()
    # print(pri)
    # # prifile = open('private.pem', 'w+')
    # # prifile.write(pub)
    # # prifile.close()

    p = Properties("../login/config.properties")
    properties_map = p.getproperties()

    rs_obj = RsaCrypt(properties_map.get("App").get("pubkey"), properties_map.get("App").get("prikey"))

    text = 'bjb421361'
    ency_text = rs_obj.encrypt(text)
    cipher_text = base64.b64encode(ency_text)

    encrypted_bytes = base64.b64decode(cipher_text)
    decode_text = rs_obj.decrypt(encrypted_bytes)
    print(ency_text, decode_text.decode())

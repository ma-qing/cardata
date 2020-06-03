import base64
import hashlib
import os
import time

import rsa
from django.http import JsonResponse

from cardata.settings import BASE_DIR


def render_json(code=200, msg=None, **kwargs):
    result = {
        'errorCode': code,
        'errorMsg': msg,
    }
    for k, v in kwargs.items():
        result[k] = v
    return JsonResponse(result)


def create_keys():  # 生成公钥和私钥
    (pubkey, privkey) = rsa.newkeys(1024)
    pub = pubkey.save_pkcs1()
    with open(os.path.join(BASE_DIR, 'lib/public.pem'), 'wb+') as f:
        f.write(pub)

    pri = privkey.save_pkcs1()
    with open(os.path.join(BASE_DIR, 'lib/private.pem'), 'wb+')as f:
        f.write(pri)


def md5Encode(strs):
    # 创建md5对象
    m = hashlib.md5()
    m.update(strs)  # 传入需要加密的字符串进行MD5加密
    return m.hexdigest()  # 获取到经过MD5加密的字符串并返回


def sign_data(data):
    md5data = md5Encode(data.encode('utf8'))
    print(md5data)

    with open(os.path.join(BASE_DIR, 'lib/private.pem'), "r") as f:
        pem = f.read()
    pri_key = rsa.PrivateKey.load_pkcs1(pem)
    signature = rsa.sign(md5data.encode('utf8'), pri_key, 'SHA-1')
    return base64.b64encode(signature)


def signtime2(signtime):
    '''签名时间转为时间戳'''
    timeArray = time.strptime(signtime, "%Y%m%d%H%M%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp



if __name__ == '__main__':
    # U = ""
    # code = "043HEEAP1eawQ41QWJxP1S8HAP1HEEA4"
    # sign = "b3b5be836fd02f37a56803c9eb3b9cef"
    # t = "1591000338"
    # version = "v1.0"
    # wxsession = "50bd5863d8b1066bb1777cc6ae33f90e"
    #
    # encode_code = "U=''&code={}&sign={}&t={}&version={}&wxsession={}".format(code,sign, t, version, wxsession)
    pass
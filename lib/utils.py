import base64
import datetime
import hashlib
import os
import time

import redis
import rsa
from django.http import JsonResponse

from cardata.settings import BASE_DIR


def render_json(code=1000, msg=None, **kwargs):
    result = {
        'errorCode': code,
        'errorMsg': msg,
    }
    if code == 1000:
        for k, v in kwargs.items():
            result[k] = v

        jsonResponseData = result
        merchantNo = 100001
        signTime = time.strftime("%Y%m%d%H%M%s", time.localtime(int(time.time())))
        strToSign = str(jsonResponseData) + "&&merchantNo={}&signTime={}&marchantKey={}".format(merchantNo, signTime,
                                                                                              merchantNo)
        md5strToSign = md5Encode(strToSign.encode("utf8"))
        sign = sign_data(md5strToSign).decode()
        data = {
            "jsonResponseData": jsonResponseData,
            "merchantNo": merchantNo,
            "signTime": signTime,
            "sign": sign
        }
        return JsonResponse(data)
    else:
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

# 获取昨天零点
def getYesterDate():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zero_yesterday = zero_today-datetime.timedelta(hours=24)
    zero_yesterday_str = zero_yesterday.strftime("%Y-%m-%d")
    return zero_yesterday_str

# redis
def set_redis(db=0):
    host = '127.0.0.1'
    port = 6379

    pool = redis.ConnectionPool(host=host, port=port, db=db)

    r = redis.StrictRedis(connection_pool=pool)
    return r


# 判断指定时间内只能访问指定次数
def limitVisit(ip, limitime=60, count=10):
    visit_redis = set_redis(4)
    visittimelist = visit_redis.lrange(ip, 0, -1)
    print(visittimelist)
    time_now = int(time.time())
    if not visittimelist:
        visit_redis.rpush(ip, time_now)
        visittimelist = [time_now]
    else:
        visit_redis.rpush(ip, time_now)
        visittimelist = [int(i.decode()) for i in visittimelist]
    while visittimelist and time_now - visittimelist[0] > limitime:
        visit_redis.lpop(ip)
    if visit_redis.llen(ip) > count:
        visit_redis.set(ip+"black", "black", ex=60)



if __name__ == '__main__':
    # U = ""
    # code = "043HEEAP1eawQ41QWJxP1S8HAP1HEEA4"
    # sign = "b3b5be836fd02f37a56803c9eb3b9cef"
    # t = "1591000338"
    # version = "v1.0"
    # wxsession = "50bd5863d8b1066bb1777cc6ae33f90e"
    #
    # encode_code = "U=''&code={}&sign={}&t={}&version={}&wxsession={}".format(code,sign, t, version, wxsession)
    strToSign = '{"a": "1", "b": "2"}&merchantNo=100004&signTime=20180809163120&marchantKey=E52Yrh2D2YUk'
    print(sign_data(md5Encode(strToSign.encode("utf8"))))
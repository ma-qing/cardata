#
import os
import time

from django.utils.deprecation import MiddlewareMixin

from cardata.settings import BASE_DIR
from lib.utils import render_json, md5Encode, signtime2, sign_data


class Verification(MiddlewareMixin):
    white_list = [
        '192.168.1.44',
        "127.0.0.1",

    ]

    def process_request(self, request):
        if request.method != "POST":
            code = None
            return render_json(code=code, msg="请求方法错误")
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.META.get("REMOTE_ADDR")
        # 检查当前请求IP是否在白名单内
        if ip in self.white_list:
            requestbody = request.body
            # 请求json
            jsonRequestData = request.POST.get('jsonRequestData')
            # 商户号
            merchantNo = request.POST.get('merchantNo')
            # 签名时间
            timestamp = request.POST.get("timestamp")
            sign = request.POST.get('sign')
            if not (sign and timestamp and jsonRequestData and merchantNo):
                code = None
                msg = "参数信息不全"
                return render_json(code=code, msg=msg)
            marchantKey_path = os.path.join(BASE_DIR, 'lib/public.pem')
            if os.path.exists(marchantKey_path):
                with open(marchantKey_path, "r") as f:
                    marchantKey = f.read()
            else:
                msg = "密钥不存在"
                code = None
                return render_json(data=msg, code=code)
            time_now = int(time.time())
            signtime_num = signtime2(timestamp)
            if time_now - signtime_num > 3600:
                msg = "超时"
                code = None
                return render_json(data=msg, code=code)

            strToSign = str(jsonRequestData) + "&&merchantNo={}&signTime={}&marchantKey={}".format(merchantNo, timestamp,marchantKey)
            local_sign = sign_data(strToSign).decode()
            print(local_sign)
            if local_sign != sign:
                msg = "sign 不正确"
                code = None
                return render_json(data=msg, code=code)
            else:
                return
        else:
            code = None
            msg = "不通过验证"
            return render_json(data=msg, code=code)



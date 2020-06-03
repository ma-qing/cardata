import hashlib
import os

from django.test import TestCase

# Create your tests here.
from cardata.settings import BASE_DIR

data = {"sign":"Si/Dak+Tk+DhxLe6lwssrzOpgsFTpn0yVCkcTGg9QHqsXp3Mn8Kqe6SSElPvbsAWhbkA+/YHE21CefGDxUZ1b39T0DV/TjYlarglf5HX3JyaURYJRX3dliiL5Y/RrNf7qnRSbSeh8YT80lVpcAGBbVTsY02xGgZhzsybbBopW+dbBakiILt70/UeDZpG3D97+kjVVvqUd+Uq/sN9EMJ3yk+SvqthXpfXr9NkGK3oBQHqPVskFO8Jzbwx9UxUJ2ZKJWMpbX6a4tVrC8uqP81uy5NCb+kraFl7cjTaQyz5OL7Ok6p8yEkVx/U2qPP0sagd3o+fpT94jInIzDv9oyTXsA==",
        "signTime":"20180809163728",
        "jsonRequestData":"{\"a\":\"1\",\"b\":\"2\"}",
        "merchantNo":"100004"}

vd = '{"a":"1","b":"2"}&merchantNo=100004&signTime=20180809163120&marchantKey=E52Yrh2D2YUk'
import base64
import rsa


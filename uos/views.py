import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from lib.utils import render_json
from uos.models import Platform, CarStyle, CarDetail
from uos.serializers import PlatformSerializers, CarTypeSerializers, CarDetailSerializers


def platform(request):

    if request.method == "GET":
        return render(request, 'test_param.html')
    if request.method == "POST":
        platforms = Platform.objects.all()
        platform_ser = PlatformSerializers(platforms, many=True)
        return render_json(autoPlatformList=platform_ser.data)


def cartypeinfo(request):
    if request.method == "POST":
        cartypes = CarStyle.objects.all()
        cartype_ser = CarTypeSerializers(cartypes, many=True)
        return render_json(autoPriceList=cartype_ser.data)


# 价格信息
def cardetail(request):
    if request.method == "POST":
        jsonRequestData = request.POST.get('jsonRequestData ')
        jsonRequestData_dict = json.loads(jsonRequestData)
        page = jsonRequestData_dict.get("page")
        pageSize = jsonRequestData_dict.get("pageSize")
        date = jsonRequestData_dict.get("date")

        carprices = CarDetail.objects.all()
        carprice_ser = CarDetailSerializers(carprices, many=True)
        return render_json(autoPriceList=carprice_ser.data)


from django.conf.urls import url

from uos import views

urlpatterns = [
    url('^openapi/autoplatform/type$', views.platform),
    url('^openapi/autoplatform/autoInfo$', views.cartypeinfo),
    url('^openapi/autoplatform/price$', views.cardetail),
]
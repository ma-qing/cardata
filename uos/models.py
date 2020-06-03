from django.db import models

# Create your models here.


# 平台表
class Platform(models.Model):
    name = models.CharField(max_length=16, verbose_name="平台名称")
    class Meta:
        db_table = "car_platform"


# 汽车类型表
class CarStyle(models.Model):
    brand = models.CharField(max_length=16, verbose_name="品牌名")
    type = models.CharField(max_length=256, verbose_name="车型")
    year = models.CharField(max_length=16, verbose_name="年款")
    style = models.CharField(max_length=256, verbose_name="车型详情描述")
    guide_price = models.CharField(max_length=32, verbose_name="指导价格")
    displacement = models.CharField(max_length=16, verbose_name="排量")
    configuration = models.CharField(max_length=1024, verbose_name="配置")
    version = models.CharField(max_length=8, verbose_name="进口类型")
    status = models.CharField(max_length=11, verbose_name="在售状态")

    class Meta:
        db_table = "car_style"


# 汽车详情表
class CarDetail(models.Model):
    platform = models.IntegerField(verbose_name="平台id")
    vehicleType = models.IntegerField(verbose_name="车型id")
    price = models.CharField(max_length=16, verbose_name="成交价")
    volume = models.CharField(max_length=8, verbose_name="成交量")
    detail_url = models.CharField(max_length=1024, verbose_name="详情页url")
    updatetime = models.CharField(max_length=64, verbose_name="更新时间")

    class Meta:
        db_table = "car_detail"

from rest_framework import serializers

from uos.models import Platform, CarStyle, CarDetail


class PlatformSerializers(serializers.ModelSerializer):
    # operatime = serializers.SerializerMethodField()
    class Meta:
        model = Platform
        fields = "id", "name"


# 类型表
class CarTypeSerializers(serializers.ModelSerializer):
    vehicleName = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_vehicleName(self, obj):
        return obj.style

    def get_price(self, obj):
        return obj.guide_price

    class Meta:
        model = CarStyle
        fields = "id", "brand", "vehicleName", "year", "price", "displacement", "configuration", "version", "status",


# 详情表
class CarDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = CarDetail
        fields = "platform", "vehicleType", "price", "volume", "updatetime"

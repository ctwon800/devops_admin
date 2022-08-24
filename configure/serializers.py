from rest_framework import serializers
from django.conf import settings
from .models import keyconfigure



class KeyconfigureSerializer(serializers.ModelSerializer):
    """
    密钥列化类
    """

    name        = serializers.CharField(required=True, read_only=False, label="密钥名称", help_text="密钥名称")
    platform   = serializers.CharField(required=True, read_only=False, label="云平台", help_text="云平台")
    appid = serializers.CharField(required=True, read_only=False, label="appid", help_text="appid")
    appkey = serializers.CharField(required=True, read_only=False, label="appkey", help_text="appkey")

    class Meta:
        model = keyconfigure
        fields = "__all__"

    def create(self, validated_data):
        instance = super(KeyconfigureSerializer, self).create(validated_data=validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.platform = validated_data.get("platform", instance.platform)
        instance.appid = validated_data.get("appid", instance.appid)
        instance.appkey = validated_data.get("appkey", instance.appkey)
        instance.save()
        return instance

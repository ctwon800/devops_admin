from rest_framework import serializers

from .models import AliyunInstance


class AliyunInstanceSerializer(serializers.ModelSerializer):
    """
    前端视图菜单序列化类
    """
    class Meta:
        model = AliyunInstance
        fields = "__all__"


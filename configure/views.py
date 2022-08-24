from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import keyconfigure
from .serializers import KeyconfigureSerializer
from rest_framework.permissions import DjangoModelPermissions

class KeyConfigureViewset(viewsets.ModelViewSet):
    """
    retrieve:
    获取用户信息

    list:
    获取用户列表

    update:
    更新用户信息

    delete:
    删除用户
    """

    queryset = keyconfigure.objects.all()
    serializer_class = KeyconfigureSerializer
    # permission_classes = [DjangoModelPermissions]

    # def get_queryset(self):
    #     queryset = super(KeyConfigureViewset, self).get_queryset()
    #     queryset = queryset.order_by("id")
    #     return queryset
"""devops_auto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from cmdb.views import GetAliyunInstance

route = DefaultRouter()

from users.router import user_router
from permissions.router import permission_router
from menu.router import menu_router
from configure.router import configure_router
from cmdb.router import cmdb_router

route.registry.extend(user_router.registry)
route.registry.extend(permission_router.registry)
route.registry.extend(menu_router.registry)
route.registry.extend(configure_router.registry)
route.registry.extend(cmdb_router.registry)


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', include(route.urls)),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('docs/', include_docs_urls("运维平台接口文档")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/updatealiyuninstance/', GetAliyunInstance, name='updatealiyuninstance'),
]

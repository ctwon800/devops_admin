from rest_framework.routers import DefaultRouter
from .views import AliyunInstanceViewset, GetAliyunInstance



cmdb_router = DefaultRouter()
cmdb_router.register(r'aliyuninstance', AliyunInstanceViewset, basename="aliyuninstance")
# cmdb_router.register(r'updatealiyuninstance', GetAliyunInstance, basename="updatealiyuninstance")



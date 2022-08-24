from rest_framework.routers import DefaultRouter
from .views import KeyConfigureViewset



configure_router = DefaultRouter()
configure_router.register(r'keyconfigure', KeyConfigureViewset, basename="keyconfigure")



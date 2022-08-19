from rest_framework.routers import DefaultRouter
from .views import UsersViewset, UserRegViewset, UserInfoViewset, GroupViewset, GroupMembersViewset, UserGroupsViewset


user_router = DefaultRouter()
user_router.register(r'userreg', UserRegViewset, basename="userreg")
user_router.register(r'users', UsersViewset, basename="users")
user_router.register(r'userinfo', UserInfoViewset, basename="userinfo")
user_router.register(r'groups', GroupViewset, basename="groups")
user_router.register(r'usergroups', UserGroupsViewset, basename="usergroups")
user_router.register(r'groupmembers', GroupMembersViewset, basename="groupmembers")



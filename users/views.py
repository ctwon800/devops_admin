from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import filters, status
from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
# Create your views here.
from .serializers import UserSerializer, UserRegSerializer, GroupSerializer
from django.contrib.auth.models import Group
from django.db.models import Q
from users.common import get_user_obj
from menu.common import get_menu_tree

User = get_user_model()

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class UserRegViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    create:
    创建用户

    update:
    修改密码
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer


class UserInfoViewset(viewsets.ViewSet):
    """
    获取当前登陆的用户信息
    """
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [DjangoModelPermissions]

    def list(self, request, *args, **kwargs):
        data = {
            "username": self.request.user.username,
            "name": self.request.user.name,
            "menus": get_menu_tree(self.request.user.get_view_permissions())
        }
        return Response(data)


class UsersViewset(viewsets.ModelViewSet):
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
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # # filter_class = UserFilter
    # sfilter_fields = ("username",)
    # extra_perms_map = {
    #     "GET": ["users.show_user_list"]
    # }

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['$username', '$email']

    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = super(UsersViewset, self).get_queryset()
        queryset = queryset.order_by("id")
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class GroupViewset(viewsets.ModelViewSet):
    """
    list:
    返回用户组（角色）列表

    destroy:
    删除角色
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name']

    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = super(GroupViewset, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset

class UserGroupsViewset(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
    返回指定用户的所有角色

    update:
    修改当前用户的角色
    """
    queryset = User.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [DjangoModelPermissions]

    def retrieve(self, request, *args, **kwargs):
        user_obj = self.get_object()
        queryset = user_obj.groups.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        gids = request.data.get("gid", [])
        user_obj.groups = Group.objects.filter(id__in=gids)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super(UserGroupsViewset, self).get_queryset()
        return queryset.order_by("id")


class GroupMembersViewset(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    角色成员管理

    retrieve:
    返回指定组的成员列表

    update:
    往指定组里添加成员

    destroy:
    从指定组里删除成员
    """
    queryset = Group.objects.all()
    serializer_class = UserSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.user_set.all()
        username=request.GET.get("username", None)
        if username is not None:
            queryset = queryset.filter(Q(name__icontains=username)|Q(username__icontains=username))
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        ret = {"status":0}
        group_obj = self.get_object()
        userobj = get_user_obj(request.data.get(request.data.get("uid", 0)))
        if userobj is None:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        else:
            group_obj.user_set.add(userobj)
        return Response(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        group_obj = self.get_object()
        userobj = get_user_obj(request.data.get("uid", 0))
        if userobj is None:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        else:
            group_obj.user_set.remove(userobj)
        return Response(ret, status=status.HTTP_200_OK)


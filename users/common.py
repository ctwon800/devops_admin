from django.contrib.auth.models import Group

def get_group_obj(gid):
    try:
        return Group.objects.get(pk=gid)
    except Group.DoesNotExist:
        return None


from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_obj(uid):
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        return None
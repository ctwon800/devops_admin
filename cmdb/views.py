import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import AliyunInstance
from .serializers import AliyunInstanceSerializer
from configure.models import keyconfigure
from rest_framework.permissions import DjangoModelPermissions
# 阿里云实例
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

class AliyunInstanceViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    获取用户信息

    list:
    获取用户列表
    """

    queryset = AliyunInstance.objects.all()
    serializer_class = AliyunInstanceSerializer




def GetAliyunInstance(self):
    queryset = keyconfigure.objects.get(pk=4)
    appid = queryset.appid
    appkey = queryset.appkey
    regionid =  queryset.regionid

    #  阿里云代码获取对应的instance信息
    credentials = AccessKeyCredential(appid, appkey)
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
    client = AcsClient(region_id=regionid, credential=credentials)
    request = DescribeInstancesRequest()
    request.set_accept_format('json')

    response = client.do_action_with_exception(request)


    data = json.loads(response)
    base_data = data['Instances']['Instance']
    print(base_data)
    print("123")
    for data in base_data:
        instanceid = data['InstanceId']
        instancename = data['InstanceName']
        instancetype = data["InstanceType"]
        hostname = data["HostName"]
        regionid = data["RegionId"]
        zoneid = data["ZoneId"]
        osname = data["OSName"]
        ostype = data["OSType"]
        cpu = data["Cpu"]
        memory = data["Memory"]
        public_ip = data['PublicIpAddress']['IpAddress'][0]
        primary_ip = data["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]
        status = data["Status"]
        create_time = data["CreationTime"]
        exprire_time = data["ExpiredTime"]
        start_time = data["StartTime"]

        oo = AliyunInstance.objects.filter(instanceid=instanceid)

        if not oo:
            aliyun = AliyunInstance(instanceid=instanceid, instancename=instancename, instancetype=instancetype,
                                    hostname=hostname, regionid=regionid, zoneid=zoneid, osname=osname, ostype=ostype,
                                    cpu=cpu, memory=memory, public_ip=public_ip, primary_ip=primary_ip, status=status,
                                    create_time=create_time, exprire_time=exprire_time, start_time=start_time)

            aliyun.save()
        else:
            print("有记录")
            AliyunInstance.objects.get(instanceid=instanceid).delete()
            aliyun = AliyunInstance(instanceid=instanceid, instancename=instancename, instancetype=instancetype,
                                    hostname=hostname, regionid=regionid, zoneid=zoneid, osname=osname, ostype=ostype,
                                    cpu=cpu, memory=memory, public_ip=public_ip, primary_ip=primary_ip, status=status,
                                    create_time=create_time, exprire_time=exprire_time, start_time=start_time)

            aliyun.save()
    return HttpResponse("ok")

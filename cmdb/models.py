from django.db import models

# Create your models here.

class AliyunInstance(models.Model):
    instanceid    = models.CharField("实例id",max_length=100, unique=True, help_text="实例id")
    instancename    = models.CharField("实例名称", max_length=32, null=True, help_text="实例名称")
    instancetype = models.CharField("实例类型", max_length=255, help_text="实例类型")
    hostname = models.CharField("主机名称", max_length=255, help_text="主机名称")
    regionid   = models.CharField("区域", max_length=255, help_text="区域")
    zoneid  = models.CharField("实例可用区", max_length=255, help_text="实例可用区")
    osname = models.CharField("OS", max_length=255, help_text="OS")
    ostype = models.CharField("os类型", max_length=255, help_text="os类型")
    cpu = models.CharField("cpu", max_length=255, help_text="cpu")
    memory = models.CharField("内存", max_length=255, help_text="内存")
    public_ip = models.CharField("公网ip", max_length=255, help_text="公网ip")
    primary_ip = models.CharField("内网ip", max_length=255, help_text="内网ip")
    status = models.CharField("运行状态", max_length=255, help_text="运行状态")
    create_time = models.DateTimeField("创建时间", null=True, help_text="创建时间")
    exprire_time = models.DateTimeField("过期时间", null=True, help_text="过期时间")
    start_time = models.DateTimeField("启动时间", null=True, help_text="启动时间")

    def __str__(self):
        return self.instanceid


    class Meta:
        ordering = ["id"]
        db_table = "instance_aliyun"
from django.db import models

# Create your models here.

class keyconfigure(models.Model):
    name = models.CharField("密钥名称", max_length=32, null=True, help_text="密钥名称", unique=True)
    platform = models.CharField("云平台", max_length=32, null=True, help_text="云平台")
    regionid = models.CharField("实例所属地域", max_length=32, null=True, help_text="实例所属地域")
    appid = models.CharField("appid", max_length=32, null=True, help_text="appid")
    appkey = models.CharField("appkey", max_length=64, null=True, help_text="appkey")

    class Meta:
        verbose_name = "密钥名称"
        ordering = ["id"]
        db_table = 'key_configure'


    def __str__(self):
        return self.name
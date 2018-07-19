from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=50, verbose_name='密码')
    email = models.CharField(max_length=50, null=True, verbose_name='邮箱')
    phone = models.CharField(max_length=12, null=True, verbose_name='电话')
    image = models.ImageField(verbose_name='头像', null=True,upload_to='user/images')
    state = models.BooleanField(default=True, verbose_name='状态')
    token = models.CharField(max_length=100, verbose_name='token')

    class Meta:
        verbose_name = '用户列表'
from django.db import models

# Create your models here.

#创建用户表
class Users(models.Model):
    sex_choices = (
        (1,"男"),
        (2,"女"),
        (3,"保密"),
    )
    mobile = models.CharField(max_length=20) #电话
    username = models.CharField(max_length=50) #昵称
    password = models.CharField(max_length=40) #密码
    sex = models.SmallIntegerField(choices=sex_choices,default=1) #性别
    school = models.CharField(max_length=20) #学校
    home = models.CharField(max_length=50) #老家
    add_time = models.DateTimeField(auto_now_add=True) #添加时间
    update_time = models.DateTimeField(auto_now=True) #修改时间
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = "Users"
    def __str__(self):
        return self.username


from django.db import models
from django.utils import timezone
# Create your models here.

class Student(models.Model):
    openid = models.CharField(max_length=50, unique=True)
    truename = models.CharField(max_length=30, blank=True, null=True)
    college = models.CharField(max_length=30, blank=True, null=True)
    cardNumber = models.CharField(max_length=30, blank=True, null=True)
    phoneNumber = models.CharField(max_length=30, blank=True, null=True)
    qqNumber = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'student'


class Event(models.Model):
    openid = models.CharField(max_length=50, blank=True, null=True)
    truename = models.CharField(max_length=30, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    photo = models.CharField(max_length=500, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    phoneNumber = models.CharField(max_length=30, blank=True, null=True)
    qqNumber = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    # 1-丢失，2-丢失已找回，3-待招领，4-已经招领，12放到丢失模块，34放到招领模块
    type = models.CharField(max_length=10, blank=True, null=True)
    iscard = models.CharField(max_length=10, blank=True, null=True)
    avatarURL = models.CharField(max_length=500, blank=True, null=True)

    # 搜索分类y
    class Meta:
        db_table = 'event'
        ordering = ('-id',)

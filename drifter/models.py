from django.db import models
from djangoProject8.settings import *


class drifter_user(models.Model):
    nicheng = models.CharField(u'nicheng',max_length=50,default='lubenwei',)
    username = models.CharField(u'username',max_length=12,)
    password = models.CharField(u'password',max_length=12)
    choice = (
        (0,'male'),
        (1,'female')
    )
    sex = models.IntegerField(u'性别',choices=choice,null=True)
    date = models.CharField(u'出生日期',max_length=50,null=True)

    hobby = models.TextField(u'爱好',null=True)
    email = models.CharField(u'电子邮箱',max_length=50)
    state = models.CharField(u'登陆状态',max_length=4,null=True)



class drifter_ocean(models.Model):
    owner = models.CharField(u'owner',max_length=50,null=True)
    content = models.TextField(u'content',max_length=100,null=True)
    choice = (
        (0,'unfound'),
        (1,"found")
    )
    state = models.IntegerField(u"state",choices=choice,null=True)
    finder = models.CharField(u"finder",max_length=50,null=True)
    reply = models.TextField(u"reply",max_length=100,null=True)



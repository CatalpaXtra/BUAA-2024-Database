from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now=True)


class UserDetail(models.Model):
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=16, default='不明')
    major = models.CharField(max_length=16, default='不明')
    grade = models.CharField(max_length=16, default='不明')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=256, default='kobe.png')
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,AbstractUser

from django.core.validators import MinLengthValidator, RegexValidator

class CustomUser(AbstractUser):
    userimage = models.ImageField(verbose_name='プロフィール画像', upload_to="media/", blank=True, null=True) #プロフ画像を管理
    exp = models.IntegerField(verbose_name='経験値', blank=True, null=True) #ユーザーの経験値を管理
    rank = models.IntegerField(verbose_name='ランク', blank=True, null=True) #ユーザーのランクを管理
    nickname = models.CharField(verbose_name='ニックネーム', max_length=10, blank=False, null=False)

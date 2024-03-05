from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,AbstractUser

from django.core.validators import MinLengthValidator, RegexValidator

# class GameUserManager(BaseUserManager):
#     def _create_user(self, username, email, nickname, password, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, nickname=nickname, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_user(self, username, email, nickname, password=None, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(
#             username=username,
#             email=email,
#             nickname=nickname,
#             password=password,
#             **extra_fields,
#         )

#     def create_superuser(self, username, email, nickname, password=None, **extra_fields):
#         extra_fields['is_active'] = True
#         extra_fields['is_staff'] = True
#         extra_fields['is_superuser'] = True
#         return self._create_user(
#             username=username,
#             email=email,
#             nickname=nickname,
#             password=password,
#             **extra_fields,
#         )



# class GameUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(verbose_name='username', max_length=10, unique=True, validators=[MinLengthValidator(5,), RegexValidator(r'^[a-zA-Z0-9]*$',)])
#     email = models.EmailField(verbose_name='Email', max_length=50, unique=True)
#     nickname = models.CharField(verbose_name='ニックネーム', max_length=10, blank=False, null=False)
#     userimage = models.ImageField(verbose_name='プロフィール画像', upload_to="media/", blank=True, null=True) #プロフ画像を管理
#     introduction = models.TextField(verbose_name='自己紹介', max_length=3000, blank=True, null=True) #自己紹介、３０００字まで

#     exp = models.IntegerField(verbose_name='経験値', blank=True, null=True) #ユーザーの経験値を管理
#     rank = models.IntegerField(verbose_name='ランク', blank=True, null=True) #ユーザーのランクを管理

#     is_active = models.BooleanField(default=True) #ログイン可
#     is_staff = models.BooleanField(default=False) #is_staffではない
#     is_admin = models.BooleanField(default=False) #is_adminではない

#     objects = GameUserManager() #AbstractBaseUserにはUserManagerが必要

#     USERNAME_FIELD = 'username' # ログイン時、ユーザー名の代わりにusernameを一意の識別子として使用
#     REQUIRED_FIELDS = ['username'] #ユーザーを作成するときにプロンプ​​トに表示されるフィールド名のリスト。

#     def __str__(self):
#         return self.nickname

class CustomUser(AbstractUser):
    userimage = models.ImageField(verbose_name='プロフィール画像', upload_to="media/", blank=True, null=True) #プロフ画像を管理
    exp = models.IntegerField(verbose_name='経験値', blank=True, null=True) #ユーザーの経験値を管理
    rank = models.IntegerField(verbose_name='ランク', blank=True, null=True) #ユーザーのランクを管理
    nickname = models.CharField(verbose_name='ニックネーム', max_length=10, blank=False, null=False)

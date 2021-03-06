from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User


class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, uid, nickname, password):
        if not uid:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        user = self.model(
            uid=self.normalize_email(uid),
            nickname=nickname,
        )
        user.set_password(password)
        #user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, uid, nickname, password):
        user = self.create_user(
            uid =uid,
            nickname=nickname,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    uid = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True, primary_key=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(default='', max_length=100, null=False, blank=False)
    birth = models.DateField(verbose_name="Birth", null=True)
    tot_concent_hour = models.IntegerField(verbose_name="Total Study Hour", default=0, null=True)
    SEX = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
        ('N', '설정안함(None)'),
    )
    sex = models.CharField(max_length=1, choices=SEX, null=True)
    BADGE = (
        ('N', 'NULL'),
        ('B', 'BRONZE'),
        ('S', 'SILVER'),
        ('G', 'GOLD'),
        ('P', 'PLATINUM'),
        ('D', 'DIAMOND'),
    )
    image = models.ImageField(null=True, blank=True)
    badge = models.CharField(max_length=2, choices=BADGE, default='N', null=True)
    # User 모델의 필수 field
    like_category=models.CharField(max_length=100,null=True, blank=True)   # "-"로 항목 구분해 저장
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 uid로 설정
    USERNAME_FIELD = 'uid'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['uid']

    def __str__(self):
       return self.uid


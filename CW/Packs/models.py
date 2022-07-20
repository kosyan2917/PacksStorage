from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = None
    last_name = None
    rating = models.IntegerField(default=True)
    pic = models.ImageField(null=True, default=None, upload_to="pics")
    #is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PacksModel(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    pack = models.FileField(upload_to='packs')
    logo = models.ImageField(upload_to='logos', null=True, default=None)
    av_mana = models.FloatField(default=0)
    description = models.CharField(max_length=255, default='')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username")
    

class CardsModel(models.Model):
    Title = models.CharField(max_length=255)
    pack = models.ForeignKey(PacksModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    ManaCost = models.IntegerField()
    Attack = models.IntegerField()
    Defence = models.IntegerField()
    DefaultBuff = models.JSONField(null=True, default=None)
    Rare = models.IntegerField(default=0)

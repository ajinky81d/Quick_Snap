from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MyUser(models.Model):
    userid = models.CharField(max_length=50, default='user123')
    name = models.CharField(max_length=255,default='user')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default='default_password')
    date = models.DateTimeField(auto_now_add=True)
     
class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    img = models.ImageField(max_length=120) 
    detail = models.CharField(max_length=23, default='detail')
    date = models.DateField(auto_now_add=True)

 

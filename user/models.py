from django.db import models

from django.contrib.auth.models import AbstractUser #extends AbstractUser model

class User(AbstractUser):
#     nickname = models.CharField(max_length=50, blank=True)
#     gender = models.CharField(max_length=10)
#     introduction = models.TextField(max_length=200,null=True)
#     userid = models.CharField(max_length=50,null=True)
#     prefer = models.CharField(max_length=50,null=True)
#     birth = models.CharField(max_length=10,null=True)
    class Meta(AbstractUser.Meta):
        pass

class Users_detail(models.Model):
    userid = models.CharField(max_length=50,null=True)
    nickname = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10)
    #introduction = models.TextField(max_length=200,null=True)
    prefer = models.CharField(max_length=50,null=True)
    birthyear = models.CharField(max_length=10,null=True)

class Resulttable(models.Model):
    """Model definition for Result."""
    userid = models.CharField(max_length=50)
    rating_Movieid = models.CharField(max_length=20,null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

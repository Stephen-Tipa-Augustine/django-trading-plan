from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    starting_balance = models.FloatField(default=0)
    growth = models.FloatField(default=0)


class ActualReturns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='associated user')
    value = models.FloatField(default=0)
    day = models.IntegerField(default=1)

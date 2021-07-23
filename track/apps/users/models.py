from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower
from django.db import models


class User(AbstractUser):
    tag = models.CharField(max_length=20,default="")
    amount = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=20, default="+254712833708")

    class Meta:
        ordering = [
            Lower('username'),
        ]


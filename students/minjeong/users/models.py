from django.db import models


class User(models.Model):
    name        = models.CharField(max_length=45)
    email       = models.CharField(max_length=45, unique=True)
    password    = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=45, blank=True)
    personal    = models.CharField(max_length=45, blank=True)

    class Meta:
        db_table='user'

from django.db import models

# Create your models here
class User(models.Model):
  name       = models.CharField(max_length=45)
  email      = models.CharField(max_length=300, unique=True)
  password   = models.CharField(max_length=100)
  phone      = models.CharField(max_length=200, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "users"



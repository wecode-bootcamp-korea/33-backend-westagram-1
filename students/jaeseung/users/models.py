from django.db import models

class User(models.Model): 
    name        = models.CharField(max_length=45, unique=True)
    email       = models.EmailField(max_length=100, unique=True)
    password    = models.CharField(max_length=300, unique=True)
    contact     = models.CharField(max_length=45, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta: 
        db_table = "users"


    
from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=50)
    email         = models.CharField(max_length=50, unique=True)
    password      = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    created_at    = models.DateTimeField(auto_now_add=True)
    modified_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name
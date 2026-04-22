from django.db import models

# Create your models here.
class UserSignup(models.Model):
    fullname=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=12)
    dob=models.DateField()
    mobile=models.BigIntegerField()
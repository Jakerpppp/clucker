from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser) :
    username = models.CharField(
        max_length=30,
        unique = True,
        validators = [RegexValidator(
            regex = r"^@\w{3,}$", #any string that has a @ followed by at least 3 numbers or letters
            message = "Username must be @ followed by at least 3 alphanumericals"
        )]
    )
    first_name = models.CharField(max_length=50,unique= False,blank= False)
    last_name = models.CharField(max_length=50,unique=False,blank=False)
    email = models.EmailField(unique=True,blank=False)
    bio = models.CharField(max_length=520, blank=True)


class Post(models.Model):
    #author = 
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField()


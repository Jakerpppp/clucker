from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from libgravatar import Gravatar

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

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    """Return a URL to the user's gravatar."""
    def gravatar(self, size=120):
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url
    
    """Return a URL to a miniature version of the user's gravatar."""
    def mini_gravatar(self):
        return self.gravatar(size=60)

"""Posts by users in their microblogs."""
class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        """Model options."""

        ordering = ['-created_at']


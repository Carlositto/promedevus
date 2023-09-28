import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from martor_markdown_plus.models import MartorField

def image_file_validator(image): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    max_height = 2160
    max_width = 3840
    height = image.height
    width = image.width
    if width > max_width or height > max_height:
        raise ValidationError("Height or Width is larger than what is allowed. Max dimensions are 2160x3840")
    if image.size > limit:
        raise ValidationError('File too large. Size should not exceed 10 MB.')

class BlogUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/profile_images', blank=True, validators=[image_file_validator])
    first_name = models.CharField(max_length=32, verbose_name='First name', blank=True)
    last_name = models.CharField(max_length=64, verbose_name='Last name', blank=True)
    email = models.EmailField(verbose_name='E-mail', blank=True)
    description = models.TextField(max_length=264, verbose_name="Description", blank=True)

    def __str__(self):
        return self.user.username

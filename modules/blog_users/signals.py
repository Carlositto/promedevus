from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import BlogUser

@receiver(post_save, sender=User)
def create_blog_user(sender, instance, created, **kwargs):
    if created:
        apps.get_model('blog_users.BlogUser').objects.create(
                user=instance,
        )

@receiver(post_save, sender=BlogUser)
def update_user(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.email = instance.email
        user.save()

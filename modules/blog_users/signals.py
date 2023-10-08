from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import BlogUser

@receiver(post_save, sender=User)
def create_blog_user(sender, instance, created, **kwargs):
    if created:
        blog_user = apps.get_model('blog_users.BlogUser').objects.create(
                user=instance,
        )
        if instance.socialaccount_set.exists():
            social_account = instance.socialaccount_set.get()
            blog_user.profile_image = social_account.extra_data['picture']
            blog_user.save()

@receiver(post_save, sender='socialaccount.SocialAccount')
def copy_picture(sender, instance, created, **kwargs):
    user = instance.user
    blog_user = user.bloguser
    picture_url = instance.extra_data['picture'].replace('s96-c', 's192-c')
    blog_user.save_image_from_url(picture_url)
    blog_user.save()

@receiver(post_save, sender=BlogUser)
def update_user(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.email = instance.email
        user.save()



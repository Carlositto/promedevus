from django import template
from django.apps import apps

register = template.Library()

@register.filter
def is_comment_liked(comment,user_id):
    content_type = apps.get_model('contenttypes.ContentType').objects.get(model='comment', app_label='django_comments')
    return apps.get_model('devblog.Like').objects.filter(target_type=content_type, target_id=comment.id, user__id=user_id).exists()
